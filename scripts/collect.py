"""Operate on domain collection plans.

Candidate seeds live in ``subreddits.txt`` and reviewed acquisition allowlists
live in ``targets.txt``. This wrapper keeps the existing fetch and
Mongo-loading implementations as the single source of truth while making
multi-subreddit runs reproducible.

Examples:
    python scripts/collect.py list
    python scripts/collect.py status linux
    python scripts/collect.py fetch beer --kind both
    python scripts/collect.py load oss --mongo-uri mongodb://localhost:27017
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from collection_common import (
    ROOT,
    available_collections,
    collection_config,
    read_names,
)


def show_status(name: str, outdir: Path) -> None:
    config = collection_config(name)
    candidates = read_names(name, "subreddits.txt")
    subreddits = read_names(name, "targets.txt")
    print(
        f"{name}: state={config.get('state', 'unspecified')}; "
        f"{len(candidates)} candidate seeds; {len(subreddits)} reviewed targets"
    )
    if not subreddits:
        print("No acquisition targets selected.")
        return

    complete = 0
    partial = 0
    missing = 0
    for subreddit in subreddits:
        present = [
            (outdir / f"{subreddit}_{kind}.zst").is_file()
            for kind in ("submissions", "comments")
        ]
        if all(present):
            state = "complete"
            complete += 1
        elif any(present):
            state = "partial"
            partial += 1
        else:
            state = "missing"
            missing += 1
        print(f"{state:8}  r/{subreddit}")
    print(
        f"\nRaw coverage: {len(subreddits)} targets; "
        f"{complete} complete, {partial} partial, {missing} missing"
    )


def run_fetch(name: str, kind: str, outdir: Path) -> None:
    config = collection_config(name)
    state = config.get("state")
    if state != "active":
        raise SystemExit(
            f"{name!r} is {state!r}, not 'active'; review its catalogue and "
            "selection before changing collections/<name>/collection.toml"
        )
    targets = read_names(name, "targets.txt")
    if not targets:
        raise SystemExit(f"{name!r} has no reviewed targets")
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "audit_collection.py"),
            name,
            "--raw-dir",
            str(outdir),
        ],
        check=True,
        cwd=ROOT,
    )
    for subreddit in targets:
        cmd = [
            sys.executable,
            str(ROOT / "scripts" / "fetch_subreddit.py"),
            subreddit,
            "--kind",
            kind,
            "--outdir",
            str(outdir),
        ]
        print(f"==> fetching {name}: r/{subreddit}", file=sys.stderr)
        subprocess.run(cmd, check=True, cwd=ROOT)


def run_load(
    name: str,
    kind: str,
    indir: Path,
    mongo_uri: str | None,
    database: str,
) -> None:
    targets = read_names(name, "targets.txt")
    if not targets:
        raise SystemExit(f"{name!r} has no reviewed targets")
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "load_to_mongo.py"),
        *targets,
        "--kind",
        kind,
        "--indir",
        str(indir),
        "--db",
        database,
    ]
    if mongo_uri:
        cmd.extend(["--mongo-uri", mongo_uri])
    subprocess.run(cmd, check=True, cwd=ROOT)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)

    subparsers.add_parser("list", help="list collection names and target counts")

    status = subparsers.add_parser("status", help="show local raw-file coverage")
    status.add_argument("collection")
    status.add_argument("--outdir", type=Path, default=ROOT / "data" / "raw")

    fetch = subparsers.add_parser("fetch", help="fetch every target sequentially")
    fetch.add_argument("collection")
    fetch.add_argument(
        "--kind", choices=["submissions", "comments", "both"], default="both"
    )
    fetch.add_argument("--outdir", type=Path, default=ROOT / "data" / "raw")

    load = subparsers.add_parser("load", help="load a collection into MongoDB")
    load.add_argument("collection")
    load.add_argument(
        "--kind", choices=["submissions", "comments", "both"], default="both"
    )
    load.add_argument("--indir", type=Path, default=ROOT / "data" / "raw")
    load.add_argument("--mongo-uri", default=None)
    load.add_argument("--db", default="reddit")

    args = parser.parse_args()
    if args.action == "list":
        for name in available_collections():
            config = collection_config(name)
            candidates = len(read_names(name, "subreddits.txt"))
            targets = len(read_names(name, "targets.txt"))
            print(
                f"{name:10} {config.get('state', 'unspecified'):8} "
                f"{candidates:>3} candidates  {targets:>3} targets"
            )
    elif args.action == "status":
        show_status(args.collection, args.outdir)
    elif args.action == "fetch":
        run_fetch(args.collection, args.kind, args.outdir)
    elif args.action == "load":
        run_load(args.collection, args.kind, args.indir, args.mongo_uri, args.db)


if __name__ == "__main__":
    main()
