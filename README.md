# data-gathering

Planning and tooling for fetching Reddit data from Academic Torrents and complementary sources.

## ⚠️ Source availability (verified 2026-07-26)

**The subreddit-partitioned bulk torrent this repo was built around has been withdrawn.** u/Watchful1 took down their Academic Torrents uploads at Reddit's request ([announcement](https://www.reddit.com/r/pushshift/comments/1v50ved/upon_reddits_request_i_am_taking_down_my_academic/)). Verified state of every known bulk torrent:

| Torrent | Infohash | Status |
|---|---|---|
| Subreddit 2005-06 → 2025-12 (**old primary**) | `3e3f64dee22dc304cdd2546254ca1f8e8ae542b4` | **dead** — page 404, tracker returns no peers |
| Subreddit 2005-06 → 2024-12 | `1614740ac8c94505e4ecb9d88be8bed7b6afddd4` | **dead** — 404, no peers |
| Subreddit 2005-06 → 2023-12 | `56aa49f9653ba545f48df2e33679f014d2829c10` | **dead** — 404, no peers |
| Reddit full 2005-06 → 2025-06 | `30dee5f0406da7a353aff6a8caa2d54fd01f2ca1` | **dead** — 404, no peers |
| Reddit full 2005-06 → 2023-12 | `9c263fc85366c1ef8f5bb9da0203f4c8c8db75f4` | **dead** — 404, no peers |
| **Reddit monthly 2025-06** | `bec5590bd3bc6c0f2d868f36ec92bec1aff4480e` | **alive** — ~13 seeders |
| **Reddit monthly 2025-07** | `b6a7ccf72368a7d39c018c423e01bc15aa551122` | **alive** — ~17 seeders |
| **Reddit monthly 2026-01** | `8412b89151101d88c915334c45d9c223169a1a60` | **alive** — ~23 seeders |

Note the `.torrent` *metadata* for the dead hashes still downloads (HTTP 200) and passes infohash verification, but the swarm is empty — `aria2c` will hang at 0%. Do not treat a successful `--dry-run` as proof the data is fetchable.

**What survives, and the acquisition strategy it implies:**

1. **Arctic Shift API** (`arctic-shift.photon-reddit.com`) — live, full history, but per-subreddit and rate-limited. **This is now the only source for pre-2025-06 per-subreddit history**, and it is the *fragile* source: a live API Reddit can switch off at any time. Capture the subreddits you care about here **first**. → [scripts/fetch_subreddit.py](scripts/fetch_subreddit.py).
2. **Recent monthly full-corpus torrents** (2025-06 onward) — still seeded, ~15-20 GB compressed each, containing *every* subreddit for one month (single `RC_YYYY-MM.zst` / `RS_YYYY-MM.zst` files, **not** per-subreddit). Resilient once downloaded (bittorrent can't be clawed back), but seeders are dwindling — grab soon and **seed back**. These serve as both a recent-months archive and a superset backfill.

**Data format** (unchanged): zstandard-compressed newline-delimited JSON (`.zst` of `.ndjson`), one object per line, separate files for `comments` and `submissions`.
- Compression caveat: Files use a non-standard window size (`2^31`); naive `zstd`/`zstandard` decoders fail with *"Frame requires too much memory for decoding"*. Use `zstandard.ZstdDecompressor(max_window_size=2**31)` or the helpers in [Watchful1/PushshiftDumps](https://github.com/Watchful1/PushshiftDumps).
- Lineage: Originally seeded from Pushshift dumps; from 2024-04 onward maintained as `.zst` only by u/Watchful1 / Arthur Heitmann's Arctic Shift pipeline. Pushshift itself was shut down in mid-2023 after Reddit's API changes.

## Systematic data-quality assessment

The dataset is the most comprehensive Reddit corpus publicly available, but it is **not complete**. Quality varies by era; checks must be run before any analytic claim.

### 1. Known structural gaps

| Era | Source | Known issues |
|---|---|---|
| 2005-06 → ~2018 | Pushshift live-ingest | Dangling parent/link references; ~0.043% of comments and ~0.65% of submissions estimated missing; under-coverage during Pushshift outages. See Gaffney & Matias 2018 (*Caveat emptor*) and Hessel's [gap analysis](https://www.cs.cornell.edu/~jhessel/reddit/gaps.html). |
| ~2018 → 2022 | Pushshift mature | Higher fidelity, but score/edit fields reflect a snapshot near ingest time, not the final state. Deleted/removed content is captured pre-deletion only when ingested in time. |
| 2023-04 → 2023-06 | Reddit API blackout / Pushshift wind-down | Substantial degradation; many subreddits went private during the June 2023 protest. Treat this window as partially missing. |
| 2023-07 → 2024-03 | Reformatted by Arctic Shift, additional sources merged | Improved relative to raw Pushshift but methodology differs; field semantics may shift. |
| 2024-04 → 2025-12 | Arctic Shift only | Single-source; no longer cross-validated against Pushshift. Coverage of small/new/quarantined subreddits is the main risk. |

### 2. Field-level concerns

- **`score`, `ups`, `num_comments`** – snapshot at ingest, not final; useless for "final score" research without re-fetching via Reddit API.
- **`body`, `selftext`** – `[deleted]` / `[removed]` reflect status *at ingest*; original text is preserved only if Pushshift/Arctic Shift saw it before deletion.
- **`author`** – becomes `[deleted]` after account deletion; same caveat.
- **`edited`** – boolean/timestamp captures only the state seen at ingest; later edits are not tracked.
- **`subreddit`, `subreddit_id`** – consistent, but renamed/banned subreddits keep historical names.
- **NSFW / quarantined / private subreddits** – under-represented, especially post-2023.

### 3. Validation checklist

Before using any slice of this dataset, run:

1. **Volume sanity check** – count rows per month per subreddit; compare against published Pushshift monthly totals and Arctic Shift release notes. Flag months that deviate >10%.
2. **Sequential-id audit** – `id` fields are base-36 monotonically increasing per object type. Sort by id, look for gaps; quantify "unknown unknowns".
3. **Reference closure** – for a sample of comments, confirm `parent_id` / `link_id` resolve to a row in the same dump. Report dangling-reference rate.
4. **Deletion-state distribution** – fraction of `[deleted]` / `[removed]` per month; spikes indicate ingest issues.
5. **Schema drift** – diff JSON keys between e.g. 2012, 2018, 2022, 2024 samples; document fields that appear/disappear.
6. **Duplicate detection** – `(id, subreddit)` should be unique; duplicates indicate merge-pipeline bugs.
7. **Spot-check vs live API** – sample 1k IDs, fetch via official Reddit API or Arctic Shift API, compare `body`/`score`/`removed_by_category`. Quantifies post-ingest mutation.
8. **Time-zone and `created_utc`** – confirm monotone ordering per subreddit; epoch values.

Each check should emit a small JSON/Parquet report committed alongside the data so downstream users can see the quality envelope.

## Data-gathering plan

### Phase 0 — Decide what we actually need

Before downloading ~2+ TB of compressed data, narrow the scope:

- Which subreddits? (Drives the Track A allowlist; the per-subreddit torrent that once made large lists cheap is gone.)
- Which time window?
- Comments, submissions, or both?
- Do we need post-ingest mutations (final score, current deletion state)?

### Phase 1 — Acquisition (post-takedown strategy)

The per-subreddit bulk torrent is gone (see the **Source availability** section at the top). Acquisition is now a two-track capture, ordered by how fast each source can disappear.

**Track A — Arctic Shift API for target subreddits (do first; fragile source).**
The API is the only remaining source for full per-subreddit history, and Reddit can switch it off at any time — so pull the subreddits you care about before anything else.

1. Define the subreddit allowlist (`subs.txt`, one per line).
2. `python scripts/fetch_subreddit.py <sub> --kind both --outdir data/raw` for each, full history. Resumable via sidecar `.cursor` files.
3. Verify each file: zstd frame check + line-count + `created_utc` min/max. Optionally `scripts/assess_subreddit.py` for a quality report.

**Track B — recent monthly full-corpus torrents (resilient, but seeders dwindling).**
Grab the still-seeded monthly dumps (2025-06 onward) as a recent-months archive and superset backfill. These are month-partitioned full-corpus files — one `RC_YYYY-MM.zst` + `RS_YYYY-MM.zst` covering *all* subreddits — so selective per-subreddit download does **not** apply; you download whole months and filter locally.

1. Install a headless BitTorrent client (`aria2c --enable-dht`, `transmission-daemon`, or `qbittorrent-nox`).
2. Fetch each monthly `.torrent` from Academic Torrents (infohashes in the availability table above; re-scrape the tracker to confirm live seeders before committing).
3. Download whole months to disk (~15-20 GB compressed each; budget ~1 TB for a full 2025-06→present series).
4. **Seed back** — these swarms are thin and this data now survives only through community seeders.
5. Filter target subreddits out of the monthly megafiles into the repo's per-sub `<sub>_{comments,submissions}.zst` layout (streaming, `max_window_size=2**31`); `load_to_mongo.py` dedupes against Track A by Reddit `id`.

Further fallbacks:
1. Direct HTTPS mirror via Arctic Shift's [download links](https://github.com/ArthurHeitmann/arctic_shift/blob/master/download_links.md).
2. PullPush API (`api.pullpush.io`) for full-text search across all of Reddit (slower, rate-limited).
3. Official Reddit API via PRAW for live state and post-2025 data.

**Single-subreddit fetch via the API (Track A)** — the primary path now; also appropriate for niche/small subs (up to roughly low millions of items) or a quick quality-assessment pull:

```bash
# Full pull of one subreddit (both kinds) into data/raw/<sub>_{submissions,comments}.zst
python scripts/fetch_subreddit.py linusrants --kind both --outdir data/raw

# Bounded by epoch range, e.g. all of 2020 only
python scripts/fetch_subreddit.py linusrants --after 1577836800 --before 1609459200

# Fetch + emit a quality report (count, time range, deleted-body share, suspicious gaps)
python scripts/assess_subreddit.py linusrants

# Re-report on a previously-fetched dump without hitting the API again
python scripts/assess_subreddit.py linusrants --skip-fetch
```

Resumable: each fetch writes a sidecar `<sub>_<kind>.cursor` file every 1000 items; re-running picks up where it left off.

### Phase 2 — Storage layout

```
data/
  raw/                  # untouched .zst from torrent, never modified
    <subreddit>_comments.zst
    <subreddit>_submissions.zst
  parquet/              # columnar, partitioned by year-month
    comments/year=YYYY/month=MM/<subreddit>.parquet
    submissions/year=YYYY/month=MM/<subreddit>.parquet
  qa/                   # output of validation checklist above
    <subreddit>/<check>.json
```

`.zst` is kept for reproducibility; analytic code reads Parquet.

### Phase 3 — Decode and normalise

- Streaming decode with `zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(...)` → `io.TextIOWrapper` → line-by-line `orjson.loads`.
- Project to a stable schema (a documented subset of fields) before writing Parquet; keep raw JSON in an overflow column for forensic queries.
- Process in chunks (e.g. 100k rows) to bound memory; parallelise across files, not within a file.
- Code lives under `scripts/`; mirror the directory shape of [Watchful1/PushshiftDumps](https://github.com/Watchful1/PushshiftDumps) where useful (`filter_file.py`, `combine_folder_multiprocess.py`, `to_csv.py`).

### Phase 4 — Enrichment (optional, only if needed)

- Re-fetch a sample (or all) target IDs via Reddit API to capture final score and current deletion state. Store as a sidecar table joined on `id`.
- Cross-link with external corpora (e.g. Hessel's gap reports, prior research datasets) by `id`.

### Phase 5 — Quality-gate publication

No downstream artefact ships without:
- The QA checklist outputs from Phase 1/3.
- A `DATA_CARD.md` per derived dataset documenting source torrent hash, time range, subreddit list, schema, known gaps, and the date Reddit-API enrichment was run.

## Open questions

- Hard upper bound on disk and bandwidth budget?
- Subreddit allowlist (drives Phase 0 → Phase 1 scope)?
- Is post-ingest mutation (final score, current deletion state) in scope, or is ingest-time state acceptable?
- Storage target: local disk, S3/R2, or institutional NAS?
- Legal/IRB review needed before redistributing derived artefacts?

## References

- Academic Torrents listing (subreddit dump, now 404 — withdrawn): https://academictorrents.com/details/3e3f64dee22dc304cdd2546254ca1f8e8ae542b4
- Takedown announcement: https://www.reddit.com/r/pushshift/comments/1v50ved/upon_reddits_request_i_am_taking_down_my_academic/
- Watchful1, *PushshiftDumps* (helper scripts, decompression notes): https://github.com/Watchful1/PushshiftDumps
- ArthurHeitmann, *Arctic Shift* (Pushshift successor, dumps + API): https://github.com/ArthurHeitmann/arctic_shift
- Arctic Shift web UI: https://arctic-shift.photon-reddit.com/
- Baumgartner et al., *The Pushshift Reddit Dataset*, ICWSM 2020: https://arxiv.org/abs/2001.08435
- Gaffney & Matias, *Caveat emptor, computational social science: Large-scale missing data in a widely-published Reddit corpus*, PLOS ONE 2018: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6034852/
- Hessel, *Reddit Dataset Update* (gap analysis): https://www.cs.cornell.edu/~jhessel/reddit/gaps.html
- Wellformedness, *Streaming decompression for the Reddit dumps*: https://www.wellformedness.com/blog/streaming-decompression-reddit-dumps/
