# CLAUDE.md

Guidance for coding agents working in this repository.

## Purpose and source of truth

This is a research-planning and data-collection workspace, not a Python
library. It supports nine domain collections: OSS, Linux, movies, science
fiction, music, comics, TV series, beer, and tabletop games.

Use these documents in order:

1. [`README.md`](README.md) for setup, implemented behavior, limitations, and
   roadmap;
2. [`collections/WORKFLOW.md`](collections/WORKFLOW.md) for collection
   lifecycle and safety gates;
3. a collection's `scope.md`, `selection.md`, and `collection.toml` for local
   research intent; and
4. [`docs/operations/collection-log.md`](docs/operations/collection-log.md) for
   historical acquisitions, destinations, interruptions, and recovery.

Do not treat `subreddits.txt`, `progress.md`, or the operations log as a fetch
queue. Only reviewed entries in `targets.txt` may be fetched through
`collect.py`, and every target must have a verified, selected catalogue row.

## Setup and local validation

Python 3.11 or newer is required because `collection_common.py` imports
`tomllib`.

```bash
python -m pip install -r requirements.txt

# Read-only/local checks
python scripts/collect.py list
python scripts/collect.py status linux
python scripts/audit_collection.py movies
python scripts/report_catalog.py movies
python -m compileall -q scripts

# Confirm every CLI still constructs successfully
for script in scripts/*.py; do python "$script" --help >/dev/null; done
```

There is currently no automated test suite, linter configuration, package
build, or full JSON Schema validator. Do not describe planned Parquet,
machine-readable QA, or monthly-torrent filtering as implemented.

## Operational commands

```bash
# Networked catalogue refresh; preserves manual catalogue fields
python scripts/catalog_subreddits.py movies

# Local-only catalogue boundary sync
python scripts/catalog_subreddits.py movies --prune-only

# Fetch is gated by targets, catalogue review, audit, and active state
python scripts/collect.py fetch movies --kind both --outdir data/raw

# Fetch one subreddit directly (not collection-state-gated)
python scripts/fetch_subreddit.py wikipedia --kind both --outdir data/raw

# Inspect or assess local raw files without MongoDB
python scripts/smoke_load_to_mongo.py wikipedia --kind submissions --num 3
python scripts/assess_subreddit.py linusrants --skip-fetch
python scripts/inventory_raw.py linux --scope candidates

# Load is not collection-state-gated; always state the destination explicitly
python scripts/collect.py load linux \
  --kind both \
  --mongo-uri mongodb://localhost:27017 \
  --db reddit
```

`collect.py load` currently ignores `mongo_uri` and `mongo_database` in
`collection.toml`. The underlying loader also skips missing files with a
warning. Verify the intended inputs and destination before loading.

## Architecture

- `collection_common.py` handles collection discovery, TOML configuration,
  name lists, and nested catalogue/inventory JSON conversion.
- `dashboard.py` serves the static `dashboard/` interface and derives a
  read-only snapshot from collection metadata, progress logs, and local raw
  files. It does not query MongoDB.
- `catalog_subreddits.py` queries Arctic Shift for factual metadata while
  preserving manual classification and selection values.
- `audit_collection.py` checks the canonical catalogue envelope, duplicates,
  target verification and selection, active-without-targets errors, and local
  raw coverage. It does not fully validate the JSON Schemas.
- `collect.py` orchestrates the single-subreddit fetcher and MongoDB loader
  over reviewed targets.
- `fetch_subreddit.py` writes appendable zstd NDJSON plus sidecar cursors.
- `assess_subreddit.py` optionally fetches, then prints a console-only quality
  summary.
- `smoke_load_to_mongo.py` reuses the real decoder to preview records or
  summarize observed fields without connecting to MongoDB.
- `inventory_raw.py` merges local file evidence into `inventory.json`;
  `--scan` fully decompresses files for counts and time edges. Manifest MongoDB
  fields copied into an inventory row describe the intended destination, not
  verified load state.
- `load_to_mongo.py` bulk-upserts by Reddit `id` into `submissions` and
  `comments` collections and creates the required indexes.
- `academic_torrents_archive.py` resolves fixed Wayback captures, falls back to
  the Wayback availability API, and validates torrent info hashes.
- `fetch_archived_torrents.py` retrieves the two withdrawn torrent descriptors
  and optionally their archived HTML detail pages. It never starts a payload
  download.
- `torrent_fetch.py` uses the archived descriptor for selective access to the
  withdrawn per-subreddit torrent. It does not support the full-history
  torrent's month-partitioned layout.

The scripts use sibling imports and are intended to run as
`python scripts/<name>.py` from the repository root.

## Data and resume invariants

Raw names are case-sensitive and shared across collections:

```text
data/raw/<subreddit>_submissions.zst
data/raw/<subreddit>_comments.zst
```

Preserve raw files and their `.cursor` sidecars together. The fetcher appends
zstd frames and checkpoints every 1,000 emitted items. A forced termination
can leave an incomplete final frame; decode the file before resuming. A rerun
after the last checkpoint may append duplicate IDs, which the MongoDB upsert
handles but raw-file QA should report.

Use a separate scratch directory for bounded `--after`/`--before` experiments.
Do not let a partial-range cursor masquerade as full-history progress.

The fetch cursor advances by `created_utc`. Pages with more same-second records
than the API returns can be skipped by the current tie-handling logic. Do not
claim complete capture without independent validation.

`assess_subreddit.py` lowercases its argument before choosing filenames;
`fetch_subreddit.py` preserves the supplied case. Take care with mixed-case
subreddit names.

## Decoder constraint

Readers for compatible Reddit dumps must allow a zstd window of `2^31`:

```python
zstandard.ZstdDecompressor(max_window_size=2**31)
```

Reuse `load_to_mongo.iter_ndjson` for new local readers so decompression and
NDJSON parsing stay consistent.

## Source status

Source status is volatile. The 2026-07-26 snapshot in the README records that
the full-history, subreddit-partitioned torrent used by `torrent_fetch.py` was
withdrawn and had no peers. Its metadata is now retrieved from a verified
Wayback capture, but a successful metadata download or `--dry-run` does not
prove data availability. Revalidate external sources before documenting or
starting a large acquisition.

## Documentation maintenance

- Keep implementation, limitations, and roadmap clearly separated.
- Update a collection's `selection.md`, `targets.txt`, and `inventory.json`
  rather than inferring current intent from historical logs.
- Put domain-only live notes in `collections/<domain>/progress.md`.
- Put cross-collection storage, recovery, and acquisition events in the
  operations log.
- Use relative Markdown links and check them after moving files.
