# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

Planning + tooling (not a library) for acquiring per-subreddit Reddit dumps from the Academic Torrents subreddit-partitioned corpus (`3e3f64dee22dc304cdd2546254ca1f8e8ae542b4`, 2005-06 → 2025-12) and from the Arctic Shift API as a fallback. The README is the canonical spec; the two scripts implement only Phases 0–1 of the data-gathering plan it describes (decode, normalise, QA are unimplemented).

## Setup and common commands

```bash
pip install -r requirements.txt          # deps: zstandard>=0.22, pymongo>=4.6 (aria2c also required for torrent path; mongod for loader)

# Bulk path (preferred when subreddit list is known): selectively pull per-subreddit .zst files
python scripts/torrent_fetch.py askreddit wikipedia --kind both --outdir data/raw
python scripts/torrent_fetch.py --subreddits-file subs.txt --dry-run     # resolve indices, don't download
python scripts/torrent_fetch.py askreddit -- --max-overall-download-limit=10M  # extra args after `--` go to aria2c

# API path (single subreddit, low-millions ceiling): paginate Arctic Shift, write .zst NDJSON
python scripts/fetch_subreddit.py wikipedia --kind both --outdir data/raw
python scripts/fetch_subreddit.py wikipedia --after 1577836800 --before 1609459200  # epoch range

# Load .zst NDJSON into MongoDB (idempotent upsert by Reddit id)
python scripts/load_to_mongo.py wikipedia --kind both           # mongodb://localhost:27017, db "reddit"
MONGO_URI=mongodb://host:27017 python scripts/load_to_mongo.py linux --db reddit_dev

# Smoke-test the loader without opening a Mongo connection
python scripts/smoke_load_to_mongo.py wikipedia --kind submissions -n 3
python scripts/smoke_load_to_mongo.py linux --kind submissions --schema -n 100
```

There is no test suite, linter config, or build step. [collection_log.md](collection_log.md) tracks what has actually been pulled (row counts, sizes, edge dates) — update it after each fetch so the next session knows the current state.

## Architecture notes

**Four standalone scripts in two layers**: acquisition (torrent or API) writes `<sub>_{submissions,comments}.zst` into `data/raw/`, then a loader streams those files into MongoDB. The two acquisition paths share no code but produce filenames that match the bulk-dump convention so downstream consumers can treat torrent-fetched and API-fetched files identically.

[scripts/torrent_fetch.py](scripts/torrent_fetch.py) — bencode parser is hand-rolled (stdlib only) so the torrent's file index can be enumerated and `aria2c --select-file=<indices>` can pull only the subreddits requested. The infohash `3e3f64dee22dc304cdd2546254ca1f8e8ae542b4` is hardcoded and verified after re-bencoding the `info` dict; mismatches abort. Subreddit names are normalised to lowercase to match the dump convention.

[scripts/fetch_subreddit.py](scripts/fetch_subreddit.py) — paginates `arctic-shift.photon-reddit.com/api/{posts,comments}/search` chronologically by advancing `after` past the last `created_utc` seen. Resumable via a sidecar `<output>.cursor` file written every 1000 items. Same-second timestamp ties are escaped by bumping the cursor by 1s and relying on `seen_last_id` dedup on the next page. Honors `X-RateLimit-Remaining`/`Reset` headers; retries with exponential backoff up to 5 attempts. Note: `after=0` is rejected by the API as "must be a valid date", so a 0 cursor is passed as `None` and `urlencode` drops the parameter.

[scripts/load_to_mongo.py](scripts/load_to_mongo.py) — streams `.zst` NDJSON into MongoDB via `zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(...)` wrapped in `TextIOWrapper`. One collection per kind (`submissions`, `comments`); bulk-upserts in batches of 1000 keyed on Reddit `id` so reruns are idempotent. `ensure_indexes` creates a unique index on `id` and a compound `(subreddit, created_utc)` index. Connection string comes from `--mongo-uri` or `MONGO_URI` env var; defaults to `mongodb://localhost:27017` db `reddit`.

[scripts/smoke_load_to_mongo.py](scripts/smoke_load_to_mongo.py) — imports `iter_ndjson` from `load_to_mongo` (so the decoder path stays in sync) and either previews N docs as pretty JSON or aggregates a field-name → type-set summary with `--schema`. No Mongo connection is opened; useful for inspecting a new dump before loading.

## Critical technical constraint

The Reddit `.zst` dumps use a non-standard window size of `2^31`. **Naive decoders fail** with *"Frame requires too much memory for decoding"*. Any decode code added to this repo must use `zstandard.ZstdDecompressor(max_window_size=2**31)`. See README §Target dataset.

## Storage layout (planned, see README Phase 2)

```
data/
  raw/         # untouched .zst, never modified — both fetchers write here by default
  parquet/     # year=YYYY/month=MM/<subreddit>.parquet (not yet implemented)
  qa/          # validation outputs (not yet implemented)
  torrent/     # cached .torrent metadata
```
