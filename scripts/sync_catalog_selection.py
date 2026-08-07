"""Apply a reviewed targets.txt decision to a collection catalogue.

This command does not select targets itself. It records an already-reviewed
allowlist by marking its catalogue rows true and all other rows false.
"""

from __future__ import annotations

import argparse

from collection_common import collection_dir, read_catalog, read_names, write_catalog


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("collection")
    args = parser.parse_args()

    path = collection_dir(args.collection) / "catalog.json"
    catalog = read_catalog(path)
    target_keys = {
        name.casefold() for name in read_names(args.collection, "targets.txt")
    }
    missing = sorted(target_keys - set(catalog))
    if missing:
        raise RuntimeError(
            "targets absent from catalogue: " + ", ".join(missing)
        )

    for key, row in catalog.items():
        row["selected"] = str(key in target_keys).lower()
    write_catalog(path, catalog.values())
    print(
        f"{args.collection}: recorded {len(target_keys)} selected and "
        f"{len(catalog) - len(target_keys)} excluded catalogue rows"
    )


if __name__ == "__main__":
    main()
