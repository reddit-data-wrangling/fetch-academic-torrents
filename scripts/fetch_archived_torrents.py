#!/usr/bin/env python3
"""Fetch verified metadata for the withdrawn Reddit datasets from Wayback.

By default this downloads the .torrent descriptors for both known datasets to
``data/torrent``.  These descriptors are only indexes; this command never
starts a BitTorrent payload download.  Use ``--include-details`` to retain the
two archived Academic Torrents HTML pages as provenance records.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from academic_torrents_archive import (
    DATASETS,
    ArchiveFetchError,
    atomic_write,
    decode_and_verify_torrent,
    ensure_archived_torrent,
    fetch_archived_details,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "datasets",
        nargs="*",
        choices=sorted(DATASETS),
        help="dataset keys; omit to fetch both",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/torrent"),
        help="artifact directory (default: data/torrent)",
    )
    parser.add_argument(
        "--include-details",
        action="store_true",
        help="also save the archived Academic Torrents HTML pages",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="retrieve and replace artifacts even if verified files exist",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60,
        help="timeout in seconds for each HTTP request (default: 60)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.timeout <= 0:
        raise SystemExit("--timeout must be greater than zero")

    keys = args.datasets or list(DATASETS)
    for key in keys:
        dataset = DATASETS[key]
        torrent_path = args.output_dir / f"{dataset.infohash}.torrent"
        try:
            torrent_data, source_url = ensure_archived_torrent(
                dataset,
                torrent_path,
                refresh=args.refresh,
                timeout=args.timeout,
            )
            meta = decode_and_verify_torrent(torrent_data, dataset.infohash)
            file_count = len(meta["info"].get("files", [])) or 1
            source = source_url or "verified local cache"
            print(
                f"{key}: {torrent_path} ({file_count:,} files; "
                f"infohash verified)\n  source: {source}"
            )

            if args.include_details:
                details_path = args.output_dir / f"{dataset.infohash}.html"
                if details_path.exists() and not args.refresh:
                    details_data = details_path.read_bytes()
                    if dataset.infohash.encode() not in details_data:
                        raise ArchiveFetchError(
                            f"cached details page failed validation: {details_path}"
                        )
                    details_source = "verified local cache"
                else:
                    details_data, details_source = fetch_archived_details(
                        dataset, args.timeout
                    )
                    atomic_write(details_path, details_data)
                print(f"  details: {details_path}\n  source: {details_source}")
        except ArchiveFetchError as exc:
            print(f"error: {key}: {exc}", file=sys.stderr)
            raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
