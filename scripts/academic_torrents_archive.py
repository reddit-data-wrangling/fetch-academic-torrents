"""Wayback access and validation for the withdrawn Reddit torrents.

This module only retrieves the small Academic Torrents detail pages and
BitTorrent metadata files.  It does not download the multi-terabyte datasets.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


USER_AGENT = "fetch-academic-torrents/0.2 (archival research metadata)"
WAYBACK_AVAILABILITY_URL = "https://archive.org/wayback/available"


@dataclass(frozen=True)
class ArchivedDataset:
    """A known Academic Torrents dataset and its archived captures."""

    key: str
    title: str
    infohash: str
    details_timestamp: str
    torrent_timestamp: str

    @property
    def original_details_url(self) -> str:
        return f"https://academictorrents.com/details/{self.infohash}"

    @property
    def original_torrent_url(self) -> str:
        return f"https://academictorrents.com/download/{self.infohash}.torrent"

    @property
    def archived_details_url(self) -> str:
        return wayback_raw_url(
            self.details_timestamp, self.original_details_url
        )

    @property
    def archived_torrent_url(self) -> str:
        return wayback_raw_url(
            self.torrent_timestamp, self.original_torrent_url
        )


DATASETS = {
    "full-history": ArchivedDataset(
        key="full-history",
        title="Reddit comments/submissions 2005-06 to 2025-12",
        infohash="3d426c47c767d40f82c7ef0f47c3acacedd2bf44",
        details_timestamp="20260218065408",
        torrent_timestamp="20260724083416",
    ),
    "subreddits": ArchivedDataset(
        key="subreddits",
        title="Subreddit comments/submissions 2005-06 to 2025-12",
        infohash="3e3f64dee22dc304cdd2546254ca1f8e8ae542b4",
        details_timestamp="20260301075857",
        torrent_timestamp="20260312192858",
    ),
}


class ArchiveFetchError(RuntimeError):
    """Raised when no valid archived artifact can be retrieved."""


# ---------- minimal bencode codec ----------


class _Bencode:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0

    def parse(self):
        if self.pos >= len(self.data):
            raise ValueError("unexpected end of bencoded data")
        token = self.data[self.pos : self.pos + 1]
        if token == b"i":
            return self._int()
        if token == b"l":
            return self._list()
        if token == b"d":
            return self._dict()
        if token.isdigit():
            return self._bytes()
        raise ValueError(f"bad token at {self.pos}: {token!r}")

    def _int(self):
        self.pos += 1
        end = self.data.index(b"e", self.pos)
        value = int(self.data[self.pos : end])
        self.pos = end + 1
        return value

    def _bytes(self):
        colon = self.data.index(b":", self.pos)
        length = int(self.data[self.pos : colon])
        start = colon + 1
        self.pos = start + length
        if self.pos > len(self.data):
            raise ValueError("byte string extends past end of bencoded data")
        return self.data[start : self.pos]

    def _list(self):
        self.pos += 1
        out = []
        while self.data[self.pos : self.pos + 1] != b"e":
            out.append(self.parse())
        self.pos += 1
        return out

    def _dict(self):
        self.pos += 1
        out = {}
        while self.data[self.pos : self.pos + 1] != b"e":
            key = self._bytes().decode("utf-8", "replace")
            out[key] = self.parse()
        self.pos += 1
        return out


def bdecode(data: bytes):
    decoder = _Bencode(data)
    result = decoder.parse()
    if decoder.pos != len(data):
        raise ValueError("trailing bytes after bencoded value")
    return result


def bencode(obj) -> bytes:
    if isinstance(obj, int):
        return f"i{obj}e".encode()
    if isinstance(obj, bytes):
        return f"{len(obj)}:".encode() + obj
    if isinstance(obj, str):
        return bencode(obj.encode("utf-8"))
    if isinstance(obj, list):
        return b"l" + b"".join(bencode(item) for item in obj) + b"e"
    if isinstance(obj, dict):
        items = b"".join(
            bencode(key.encode() if isinstance(key, str) else key)
            + bencode(value)
            for key, value in sorted(obj.items())
        )
        return b"d" + items + b"e"
    raise TypeError(type(obj))


def decode_and_verify_torrent(data: bytes, expected_infohash: str) -> dict:
    """Decode a torrent and verify that its info dictionary has the given hash."""

    try:
        meta = bdecode(data)
        info = meta["info"]
    except (IndexError, KeyError, TypeError, ValueError) as exc:
        raise ArchiveFetchError(
            f"response is not valid torrent metadata: {exc}"
        ) from exc
    digest = hashlib.sha1(bencode(info)).hexdigest()
    if digest != expected_infohash:
        raise ArchiveFetchError(
            f"infohash mismatch: torrent={digest} expected={expected_infohash}"
        )
    return meta


# ---------- Wayback retrieval ----------


def wayback_raw_url(timestamp: str, original_url: str) -> str:
    if not re.fullmatch(r"\d{14}", timestamp):
        raise ValueError(f"invalid Wayback timestamp: {timestamp!r}")
    parsed = urllib.parse.urlsplit(original_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"invalid original URL: {original_url!r}")
    return f"https://web.archive.org/web/{timestamp}id_/{original_url}"


def _request_bytes(url: str, timeout: float) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read()
    if data.startswith(b"\x1f\x8b"):
        data = gzip.decompress(data)
    return data


def resolve_archived_url(
    original_url: str, near_timestamp: str, timeout: float = 60
) -> str:
    """Ask Wayback for the closest successful capture and return its raw URL."""

    query = urllib.parse.urlencode(
        {"url": original_url, "timestamp": near_timestamp}
    )
    data = _request_bytes(f"{WAYBACK_AVAILABILITY_URL}?{query}", timeout)
    try:
        closest = json.loads(data)["archived_snapshots"]["closest"]
        timestamp = str(closest["timestamp"])
        available = closest["available"]
        status = str(closest["status"])
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise ArchiveFetchError(
            f"unexpected Wayback availability response for {original_url}"
        ) from exc
    if available is not True or status != "200":
        raise ArchiveFetchError(f"no successful Wayback capture for {original_url}")
    return wayback_raw_url(timestamp, original_url)


def fetch_archived_torrent(
    dataset: ArchivedDataset, timeout: float = 60
) -> tuple[bytes, str]:
    """Retrieve and verify an archived .torrent, returning bytes and source URL."""

    errors = []
    try:
        data = _request_bytes(dataset.archived_torrent_url, timeout)
        decode_and_verify_torrent(data, dataset.infohash)
        return data, dataset.archived_torrent_url
    except (ArchiveFetchError, OSError, urllib.error.URLError) as exc:
        errors.append(f"{dataset.archived_torrent_url}: {exc}")

    try:
        resolved = resolve_archived_url(
            dataset.original_torrent_url, dataset.details_timestamp, timeout
        )
        data = _request_bytes(resolved, timeout)
        decode_and_verify_torrent(data, dataset.infohash)
        return data, resolved
    except (ArchiveFetchError, OSError, urllib.error.URLError) as exc:
        errors.append(f"availability fallback: {exc}")
    raise ArchiveFetchError("; ".join(errors))


def fetch_archived_details(
    dataset: ArchivedDataset, timeout: float = 60
) -> tuple[bytes, str]:
    """Retrieve a raw archived details page and confirm it names the dataset."""

    url = dataset.archived_details_url
    try:
        data = _request_bytes(url, timeout)
    except (OSError, urllib.error.URLError) as exc:
        raise ArchiveFetchError(f"could not retrieve {url}: {exc}") from exc
    if dataset.infohash.encode() not in data:
        raise ArchiveFetchError(
            f"archived details page does not contain {dataset.infohash}"
        )
    return data, url


def atomic_write(path: Path, data: bytes) -> None:
    """Write an artifact without leaving a partial cache file on interruption."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def ensure_archived_torrent(
    dataset: ArchivedDataset,
    cache_path: Path,
    *,
    refresh: bool = False,
    timeout: float = 60,
) -> tuple[bytes, str | None]:
    """Return verified cached metadata, fetching it from Wayback when needed."""

    if cache_path.exists() and not refresh:
        data = cache_path.read_bytes()
        decode_and_verify_torrent(data, dataset.infohash)
        return data, None
    data, source_url = fetch_archived_torrent(dataset, timeout)
    atomic_write(cache_path, data)
    return data, source_url
