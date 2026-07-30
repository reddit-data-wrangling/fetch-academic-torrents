# Reddit domain collections

This repository contains research plans and command-line tools for building
topic-based Reddit datasets. It currently covers open-source software, Linux,
movies, science fiction, music, comics, TV series, beer, and tabletop games.

The project is a data-collection workspace, not a Python package. It keeps four
different concepts separate:

1. candidate communities in `subreddits.txt`;
2. verified metadata in `catalog.json`;
3. reviewed acquisition targets in `targets.txt`; and
4. acquired holdings in `inventory.json`.

Start with the [collection catalogue](collections/README.md) and
[collection workflow](collections/WORKFLOW.md). For historical fetches,
destinations, and recovery notes, see the
[operations log](docs/operations/collection-log.md).

## Repository map

| Path | Purpose |
| --- | --- |
| [`collections/`](collections/README.md) | Domain scopes, catalogues, selections, targets, and inventories |
| [`COLLECTION_PROGRESS.md`](COLLECTION_PROGRESS.md) | Collection progress for VS Code Markdown Preview |
| [`collections/schemas/`](collections/schemas/) | JSON Schema references for catalogue and inventory files |
| [`scripts/`](scripts/) | Catalogue, acquisition, inspection, loading, and reporting commands |
| [`docs/`](docs/README.md) | Cross-collection documentation and operational history |
| `data/` | Local raw and derived data; ignored by Git |

Raw captures use a shared flat layout:

```text
data/raw/<subreddit>_submissions.zst
data/raw/<subreddit>_comments.zst
```

A subreddit can belong to several domain collections without duplicating its
raw files.

## Requirements and installation

- Python 3.11 or newer (`tomllib` is used by the collection tooling)
- `pip`
- MongoDB only when using the loader
- `aria2c` only for the legacy torrent script

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The Python dependencies are `zstandard` and `pymongo`. There is no package
installation step, test suite, linter configuration, or build step.

## Safe first steps

These commands make no network requests and do not connect to MongoDB:

```bash
# Show collection states and list sizes.
python scripts/collect.py list

# Show selected targets and local raw-file coverage.
python scripts/collect.py status linux

# Audit a collection's local structure and selection gates.
python scripts/audit_collection.py movies

# Render a catalogue to standard output.
python scripts/report_catalog.py movies
```

All current `targets.txt` files may be empty while collection design is in
progress. That is intentional: candidate lists are not download queues.

## Progress dashboard

Refresh the Markdown dashboard from the repository root:

```bash
python scripts/report_progress.py
```

Open `COLLECTION_PROGRESS.md` in VS Code and run **Markdown: Open Preview**
(`Ctrl+Shift+V` on Windows/Linux or `Cmd+Shift+V` on macOS). No server, open
port, or browser process is required. The report groups progress by collection
theme and subreddit using the collection manifests, catalogues, optional
`progress.md` logs, and local raw files.

## Collection workflow

The full procedure, file roles, and review rules are in
[collections/WORKFLOW.md](collections/WORKFLOW.md). The operational sequence is:

### 1. Define and catalogue candidates

Write the research boundary in `scope.md`, then add candidate names to
`subreddits.txt`, one name per line without the `r/` prefix.

```bash
# Networked: query Arctic Shift and update factual catalogue fields.
python scripts/catalog_subreddits.py movies

# Local only: remove catalogue rows no longer present in subreddits.txt.
python scripts/catalog_subreddits.py movies --prune-only

# Generate a reviewable Markdown snapshot.
python scripts/report_catalog.py movies \
  --output collections/movies/report.md
```

The catalogue command preserves manual classification and selection fields.
Metadata such as subscriber and archive counts is a dated snapshot, not a
guarantee of current state or download completeness.

### 2. Review and select a panel

Document the sampling rationale in `selection.md`. For each target:

- add the canonical name to `targets.txt`;
- set `selection.selected` to `true` in its `catalog.json` entry; and
- ensure `verification.status` is `verified`.

Then run:

```bash
python scripts/audit_collection.py movies
```

The audit checks the catalogue envelope, duplicate name-list entries, target
presence, verification state, selection flags, active-without-targets errors,
and local raw-file coverage. It is not a full JSON Schema validator.

### 3. Acquire reviewed targets

Only `collect.py fetch` is state-gated. It requires a non-empty reviewed target
list and `state = "active"` in `collection.toml`; it also runs the audit before
making API requests.

```bash
python scripts/collect.py fetch movies --kind both --outdir data/raw
```

To fetch one subreddit outside collection orchestration:

```bash
# Full available history.
python scripts/fetch_subreddit.py wikipedia --kind both --outdir data/raw

# A bounded experiment. Use a scratch directory so its cursor and partial data
# cannot be mistaken for a full-history capture.
python scripts/fetch_subreddit.py wikipedia \
  --after 1577836800 \
  --before 1609459200 \
  --outdir data/scratch/wikipedia-2020
```

The fetcher appends zstd frames and stores a resume timestamp in
`<subreddit>_<kind>.cursor`. Keep each raw file and its cursor together. Do not
reuse an output directory for a different time window. If a process is killed
while writing, validate or replace the affected file before resuming; an
incomplete final zstd frame can make later reads fail.

The cursor advances by timestamp. When a page contains more same-second items
than the API returns, the current implementation may skip records at that
timestamp. Treat completeness as something to measure, not assume.

### 4. Inspect and assess raw captures

```bash
# Preview records without opening a MongoDB connection.
python scripts/smoke_load_to_mongo.py wikipedia \
  --kind submissions \
  --num 3

# Summarize observed fields and types.
python scripts/smoke_load_to_mongo.py wikipedia \
  --kind submissions \
  --schema \
  --num 100

# Fetch, then report counts, duplicate IDs, time range, field coverage,
# deleted-body share, and a simple monthly-gap heuristic.
python scripts/assess_subreddit.py linusrants

# Reassess existing files without a network request.
python scripts/assess_subreddit.py linusrants --skip-fetch
```

`assess_subreddit.py` normalizes its subreddit argument to lowercase, while the
fetcher preserves case in filenames. For mixed-case names, use the lowercase
filename convention or invoke the smoke test directly on the actual files.

### 5. Inventory and load

```bash
# Record paths and sizes using filesystem metadata only.
python scripts/inventory_raw.py linux --scope candidates

# Also stream every matching file for counts and time edges.
python scripts/inventory_raw.py linux --scope candidates --scan

# Load reviewed targets into MongoDB.
python scripts/collect.py load linux \
  --kind both \
  --mongo-uri mongodb://localhost:27017 \
  --db reddit
```

`--scan` fully decompresses each file and can take a long time. Inventory paths
are absolute local paths, so refresh the inventory after moving data. The
inventory command copies the manifest's intended MongoDB destination but does
not query MongoDB; destination fields alone do not prove that records were
loaded.

Unlike `fetch`, `collect.py load` is not gated by collection state and does not
automatically read `mongo_uri` or `mongo_database` from `collection.toml`.
Pass the destination explicitly. The underlying loader skips missing input
files with a warning and upserts by Reddit `id`, making repeated loads
idempotent.

## Command reference

| Command | Network or external state | Purpose |
| --- | --- | --- |
| `collect.py list` | None | List collections, states, candidates, and targets |
| `collect.py status` | Local filesystem only | Show raw coverage for targets |
| `report_progress.py` | Local files only; writes Markdown | Refresh `COLLECTION_PROGRESS.md` |
| `catalog_subreddits.py` | Arctic Shift, except `--prune-only` | Verify names and refresh metadata |
| `report_catalog.py` | Local filesystem only | Render a Markdown catalogue |
| `audit_collection.py` | Local filesystem only | Check selection gates and raw coverage |
| `collect.py fetch` | Arctic Shift; writes raw files | Fetch all reviewed targets sequentially |
| `fetch_subreddit.py` | Arctic Shift; writes raw files | Fetch one subreddit |
| `assess_subreddit.py` | Arctic Shift unless `--skip-fetch` | Fetch and/or print a quality report |
| `smoke_load_to_mongo.py` | Local filesystem only | Preview records or observed schema |
| `inventory_raw.py` | Local filesystem; writes inventory | Record local raw holdings |
| `collect.py load` | MongoDB | Load all reviewed targets |
| `load_to_mongo.py` | MongoDB | Load one or more named subreddits |
| `torrent_fetch.py` | Academic Torrents and BitTorrent | Legacy selective torrent client |

Every command supports `--help`.

## Source availability

Source availability is volatile. Recheck endpoints, torrent listings, peer
counts, data-use terms, and institutional requirements before starting a large
collection.

### Dated source snapshot: 2026-07-26

The maintainer of the Reddit dumps
[announced their withdrawal from Academic Torrents](https://www.reddit.com/r/pushshift/comments/1v50ved/upon_reddits_request_i_am_taking_down_my_academic/)
at Reddit's request. At the time of the repository's check:

- the full-history, subreddit-partitioned torrent hard-coded in
  `torrent_fetch.py` had no peers, even though its `.torrent` metadata remained
  downloadable;
- other full-history torrents checked by the project also had no peers;
- some month-partitioned, full-corpus torrents still had peers; and
- the Arctic Shift search API responded successfully.

Treat those as dated observations, not current guarantees. A successful
`torrent_fetch.py --dry-run` verifies metadata and file selection only; it does
not prove that peers can serve the data.

The repository currently implements per-subreddit acquisition through the
Arctic Shift API. Recent monthly torrents contain whole-month `RC_YYYY-MM.zst`
and `RS_YYYY-MM.zst` files for all subreddits. This repository does not yet
implement downloading or filtering those monthly files. The legacy
`torrent_fetch.py` only understands the withdrawn, subreddit-partitioned
torrent and should be considered archival code.

## Data format and storage

Raw files are zstandard-compressed newline-delimited JSON, with separate files
for submissions and comments. Reddit dump files can require a decoder window
of `2^31`; naive decoders may fail with “Frame requires too much memory for
decoding.” Repository readers use:

```python
zstandard.ZstdDecompressor(max_window_size=2**31)
```

The implemented layout is:

```text
data/
  raw/
    <subreddit>_comments.zst
    <subreddit>_comments.cursor
    <subreddit>_submissions.zst
    <subreddit>_submissions.cursor
  torrent/
    <infohash>.torrent
```

Parquet normalization, structured QA artefacts, and monthly-torrent filtering
are planned but not implemented.

## Data-quality limitations

Archived Reddit data is not a faithful final-state copy of Reddit:

- coverage varies by source and time period;
- scores, edit state, deletion state, and comment counts are snapshots;
- deleted or removed text is available only when captured before removal;
- schema and field semantics change over time;
- private, quarantined, banned, small, and new communities may be
  under-represented; and
- API pagination, interrupted writes, source outages, and merges can introduce
  gaps or duplicates.

The implemented assessment reports counts, unique IDs, time ranges, monthly
volume, common field types, and deleted-body share. It does not establish
completeness. Before publication, also consider:

1. comparing monthly volume with an independent source;
2. checking duplicate IDs and malformed records;
3. measuring unresolved `parent_id` and `link_id` references;
4. tracking deletion-state and schema drift over time;
5. documenting acquisition dates, source URLs or hashes, and exact target
   lists; and
6. creating a data card that records known gaps and transformations.

Do not interpret gaps between IDs inside a subreddit as missing records:
Reddit IDs are assigned across the platform, so such gaps are expected.

## Responsible use

Reddit data can contain personal, sensitive, deleted, or subsequently edited
material. Before collecting, analysing, or redistributing it:

- follow applicable law, platform terms, research-ethics review, and
  institutional policy;
- collect only what the research question requires;
- protect raw data and avoid publishing identifiable text unnecessarily;
- document retention and deletion procedures; and
- distinguish public availability from ethical permission to reuse data.

## Roadmap

- Download and filter recent monthly full-corpus torrents.
- Normalize raw NDJSON into a documented Parquet schema.
- Emit machine-readable QA reports rather than console-only summaries.
- Add automated tests, formatting, and JSON Schema validation.
- Produce a data card for each published derived dataset.

## References

- [Academic Torrents legacy subreddit dump](https://academictorrents.com/details/3e3f64dee22dc304cdd2546254ca1f8e8ae542b4)
- [Withdrawal announcement](https://www.reddit.com/r/pushshift/comments/1v50ved/upon_reddits_request_i_am_taking_down_my_academic/)
- [Watchful1/PushshiftDumps](https://github.com/Watchful1/PushshiftDumps)
- [ArthurHeitmann/arctic_shift](https://github.com/ArthurHeitmann/arctic_shift)
- [Arctic Shift web interface](https://arctic-shift.photon-reddit.com/)
- [Baumgartner et al., “The Pushshift Reddit Dataset”](https://arxiv.org/abs/2001.08435)
- [Gaffney and Matias, “Caveat emptor, computational social science”](https://pmc.ncbi.nlm.nih.gov/articles/PMC6034852/)
- [Hessel, “Reddit Dataset Update”](https://www.cs.cornell.edu/~jhessel/reddit/gaps.html)
