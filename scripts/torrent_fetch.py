"""Selectively torrent-download per-subreddit files from the Academic Torrents
subreddit-partitioned Reddit dump.

Pipeline:
  1. Fetch the archived .torrent metadata for infohash
     3e3f64dee22dc304cdd2546254ca1f8e8ae542b4 from the Wayback Machine
     (cached locally and verified before use).
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
import shutil
import subprocess
import sys
from pathlib import Path

from academic_torrents_archive import (
    DATASETS,
    ArchiveFetchError,
    bdecode,
    bencode,
    decode_and_verify_torrent,
    ensure_archived_torrent,
)


DATASET = DATASETS["subreddits"]
INFOHASH = DATASET.infohash


# ---------- torrent handling ----------

def fetch_torrent(cache_path: Path, refresh: bool = False) -> bytes:
    try:
        data, source_url = ensure_archived_torrent(
            DATASET, cache_path, refresh=refresh
        )
    except ArchiveFetchError as exc:
        raise SystemExit(
            f"could not fetch archived torrent metadata: {exc}"
        ) from exc
    if source_url:
        print(f"downloaded verified metadata from {source_url}", file=sys.stderr)
    else:
        print(f"using verified torrent cache {cache_path}", file=sys.stderr)
    return data


def verify_infohash(meta: dict) -> None:
    # Retained as a small compatibility wrapper for callers of this script.
    decode_and_verify_torrent(bencode(meta), INFOHASH)


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
    cli_args = sys.argv[1:]
    aria2_args: list[str] = []
    if "--" in cli_args:
        separator = cli_args.index("--")
        aria2_args = cli_args[separator + 1 :]
        cli_args = cli_args[:separator]

    p = argparse.ArgumentParser(
        description=__doc__,
        epilog="Pass additional aria2c arguments after `--`.",
    )
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
    p.add_argument(
        "--refresh-torrent-metadata",
        action="store_true",
        help="replace the verified local .torrent cache from Wayback",
    )
    p.add_argument("--seed-minutes", type=int, default=60)
    p.add_argument("--dry-run", action="store_true", help="resolve indices and exit")
    args = p.parse_args(cli_args)

    subs = read_subreddit_list(args)
    kinds = ["submissions", "comments"] if args.kind == "both" else [args.kind]

    raw = fetch_torrent(
        args.torrent_cache, refresh=args.refresh_torrent_metadata
    )
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

    rc = run_aria2c(
        args.torrent_cache, indices, args.outdir, args.seed_minutes, aria2_args
    )
    sys.exit(rc)


if __name__ == "__main__":
    main()
