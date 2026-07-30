"""Audit a collection plan without fetching or changing external state.

Checks configuration, catalogue schema, candidate/target uniqueness, target
verification, selection flags, and raw-file coverage.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from collection_common import (
    collection_config,
    collection_dir,
    read_catalog,
    read_names,
)

ROOT = Path(__file__).resolve().parent.parent


def duplicate_lines(path: Path) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip().removeprefix("r/")
        if not line or line.startswith("#"):
            continue
        key = line.casefold()
        if key in seen:
            duplicates.append(line)
        seen.add(key)
    return duplicates


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("collection")
    parser.add_argument("--raw-dir", type=Path, default=ROOT / "data" / "raw")
    args = parser.parse_args()

    directory = collection_dir(args.collection)
    config = collection_config(args.collection)
    candidates = read_names(args.collection, "subreddits.txt")
    targets = read_names(args.collection, "targets.txt")
    catalog_path = directory / "catalog.json"
    catalog = read_catalog(catalog_path)
    errors: list[str] = []
    warnings: list[str] = []

    payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1 or not isinstance(
        payload.get("communities"), list
    ):
        errors.append("catalog.json does not match the canonical envelope")

    for filename in ("subreddits.txt", "targets.txt"):
        duplicates = duplicate_lines(directory / filename)
        if duplicates:
            errors.append(f"{filename} has duplicates: {', '.join(duplicates)}")

    candidate_keys = {name.casefold() for name in candidates}
    for target in targets:
        key = target.casefold()
        row = catalog.get(key)
        if key not in candidate_keys:
            warnings.append(f"r/{target} is a target but not a candidate seed")
        if row is None:
            errors.append(f"r/{target} is absent from catalog.json")
            continue
        if row["verification_status"] != "verified":
            errors.append(
                f"r/{target} verification_status={row['verification_status']!r}"
            )
        if row["selected"].strip().casefold() not in {"true", "yes", "1"}:
            errors.append(f"r/{target} is not marked selected in catalog.json")

    if config.get("state") == "active" and not targets:
        errors.append("collection is active but targets.txt is empty")

    raw_complete = sum(
        all(
            (args.raw_dir / f"{target}_{kind}.zst").is_file()
            for kind in ("submissions", "comments")
        )
        for target in targets
    )
    print(
        f"{args.collection}: state={config.get('state', 'unspecified')}; "
        f"{len(candidates)} candidates; {len(catalog)} catalogued; "
        f"{len(targets)} selected; {raw_complete} raw-complete"
    )
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
