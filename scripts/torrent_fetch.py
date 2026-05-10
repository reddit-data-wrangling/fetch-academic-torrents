"""Selectively torrent-download per-subreddit files from the Academic Torrents
subreddit-partitioned Reddit dump.

Pipeline:
  1. Fetch the .torrent metadata for infohash 3e3f64dee22dc304cdd2546254ca1f8e8ae542b4
     from academictorrents.com (cached locally).
  2. Bencode-parse it, enumerate files, and pick the indices that match
     ``<sub>_submissions.zst`` / ``<sub>_comments.zst`` for the requested
     subreddits.
  3. Invoke ``aria2c`` with ``--select-file=<indices>`` so only those files
     are pulled. Default seed-time is 60 minutes to give back to the swarm.

Requirements: aria2c on PATH. No Python dependencies beyond stdlib.

Caveats:
  * Subreddit names are case-sensitive in the dump (lowercase by convention).
  * Niche subs sometimes have only the original seeder; expect slow tails.
  * The torrent index is large — first ``aria2c`` startup can take a moment.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

INFOHASH = "3e3f64dee22dc304cdd2546254ca1f8e8ae542b4"
TORRENT_URL = f"https://academictorrents.com/download/{INFOHASH}.torrent"


# ---------- minimal bencode decoder ----------

class _Bencode:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0

    def parse(self):
        c = self.data[self.pos:self.pos + 1]
        if c == b"i":
            return self._int()
        if c == b"l":
            return self._list()
        if c == b"d":
            return self._dict()
        if c.isdigit():
            return self._bytes()
        raise ValueError(f"bad token at {self.pos}: {c!r}")

    def _int(self):
        self.pos += 1
        end = self.data.index(b"e", self.pos)
        n = int(self.data[self.pos:end])
        self.pos = end + 1
        return n

    def _bytes(self):
        colon = self.data.index(b":", self.pos)
        n = int(self.data[self.pos:colon])
        start = colon + 1
        self.pos = start + n
        return self.data[start:self.pos]

    def _list(self):
        self.pos += 1
        out = []
        while self.data[self.pos:self.pos + 1] != b"e":
            out.append(self.parse())
        self.pos += 1
        return out

    def _dict(self):
        self.pos += 1
        out = {}
        while self.data[self.pos:self.pos + 1] != b"e":
            key = self._bytes().decode("utf-8", "replace")
            out[key] = self.parse()
        self.pos += 1
        return out


def bdecode(data: bytes):
    return _Bencode(data).parse()


def bencode(obj) -> bytes:
    if isinstance(obj, int):
        return f"i{obj}e".encode()
    if isinstance(obj, bytes):
        return f"{len(obj)}:".encode() + obj
    if isinstance(obj, str):
        return bencode(obj.encode("utf-8"))
    if isinstance(obj, list):
        return b"l" + b"".join(bencode(x) for x in obj) + b"e"
    if isinstance(obj, dict):
        items = b"".join(
            bencode(k.encode() if isinstance(k, str) else k) + bencode(v)
            for k, v in sorted(obj.items())
        )
        return b"d" + items + b"e"
    raise TypeError(type(obj))


# ---------- torrent handling ----------

def fetch_torrent(cache_path: Path) -> bytes:
    if cache_path.exists():
        return cache_path.read_bytes()
    print(f"downloading {TORRENT_URL}", file=sys.stderr)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(
        TORRENT_URL, headers={"User-Agent": "data-gathering/0.1"}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    cache_path.write_bytes(data)
    return data


def verify_infohash(meta: dict) -> None:
    info = meta["info"]
    digest = hashlib.sha1(bencode(info)).hexdigest()
    if digest != INFOHASH:
        raise SystemExit(
            f"infohash mismatch: torrent={digest} expected={INFOHASH}"
        )


def enumerate_files(meta: dict) -> list[tuple[int, str]]:
    info = meta["info"]
    if "files" not in info:
        # single-file torrent — not what we expect here
        return [(1, info["name"].decode("utf-8"))]
    out = []
    for idx, entry in enumerate(info["files"], start=1):
        path_parts = [p.decode("utf-8") for p in entry["path"]]
        out.append((idx, "/".join(path_parts)))
    return out


def pick_indices(
    files: list[tuple[int, str]],
    subreddits: list[str],
    kinds: list[str],
) -> tuple[list[int], list[str]]:
    targets = set()
    for s in subreddits:
        for k in kinds:
            targets.add(f"{s}_{k}.zst")
    chosen: list[int] = []
    matched: list[str] = []
    for idx, path in files:
        leaf = path.rsplit("/", 1)[-1]
        if leaf in targets:
            chosen.append(idx)
            matched.append(path)
            targets.discard(leaf)
    if targets:
        print(
            f"warning: no file in torrent for: {sorted(targets)}",
            file=sys.stderr,
        )
    return chosen, matched


# ---------- aria2c driver ----------

def run_aria2c(
    torrent_path: Path,
    indices: list[int],
    outdir: Path,
    seed_minutes: int,
    extra: list[str],
) -> int:
    if not shutil.which("aria2c"):
        raise SystemExit("aria2c not found on PATH; install aria2 first")
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "aria2c",
        f"--dir={outdir}",
        f"--select-file={','.join(map(str, indices))}",
        "--enable-dht=true",
        "--bt-enable-lpd=true",
        "--seed-ratio=1.0",
        f"--seed-time={seed_minutes}",
        "--summary-interval=30",
        "--console-log-level=notice",
        str(torrent_path),
        *extra,
    ]
    print("$ " + " ".join(cmd), file=sys.stderr)
    return subprocess.call(cmd)


# ---------- CLI ----------

def read_subreddit_list(args) -> list[str]:
    subs: list[str] = list(args.subreddits)
    if args.subreddits_file:
        for line in Path(args.subreddits_file).read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                subs.append(line)
    if not subs:
        raise SystemExit("provide subreddit names as args or via --subreddits-file")
    # normalise: strip r/ prefix, lower-case
    return sorted({s.removeprefix("r/").lower() for s in subs})


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("subreddits", nargs="*", help="subreddit names (without r/)")
    p.add_argument("--subreddits-file", help="newline-separated list; # comments allowed")
    p.add_argument(
        "--kind",
        choices=["submissions", "comments", "both"],
        default="both",
    )
    p.add_argument("--outdir", type=Path, default=Path("data/raw"))
    p.add_argument(
        "--torrent-cache",
        type=Path,
        default=Path("data/torrent") / f"{INFOHASH}.torrent",
    )
    p.add_argument("--seed-minutes", type=int, default=60)
    p.add_argument("--dry-run", action="store_true", help="resolve indices and exit")
    p.add_argument(
        "aria2_args",
        nargs=argparse.REMAINDER,
        help="extra args passed through to aria2c after `--`",
    )
    args = p.parse_args()

    subs = read_subreddit_list(args)
    kinds = ["submissions", "comments"] if args.kind == "both" else [args.kind]

    raw = fetch_torrent(args.torrent_cache)
    meta = bdecode(raw)
    verify_infohash(meta)
    files = enumerate_files(meta)
    indices, matched = pick_indices(files, subs, kinds)
    if not indices:
        raise SystemExit("no matching files found in torrent")

    print(f"selected {len(indices)} files for {len(subs)} subreddit(s):", file=sys.stderr)
    for path in matched:
        print(f"  {path}", file=sys.stderr)

    if args.dry_run:
        return

    extra = list(args.aria2_args)
    if extra and extra[0] == "--":
        extra = extra[1:]
    rc = run_aria2c(
        args.torrent_cache, indices, args.outdir, args.seed_minutes, extra
    )
    sys.exit(rc)


if __name__ == "__main__":
    main()
