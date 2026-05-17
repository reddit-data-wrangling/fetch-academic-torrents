# data-gathering

Planning and tooling for fetching Reddit data from Academic Torrents and complementary sources.

## Target dataset

**Subreddit comments/submissions 2005-06 to 2025-12**
Academic Torrents hash: `3e3f64dee22dc304cdd2546254ca1f8e8ae542b4`
URL: https://academictorrents.com/details/3e3f64dee22dc304cdd2546254ca1f8e8ae542b4

- Format: zstandard-compressed newline-delimited JSON (`.zst` of `.ndjson`), one object per line, separate files for `comments` and `submissions`, partitioned per-subreddit (the "Subreddit" variant) rather than per-month.
- Lineage: Originally seeded from Pushshift dumps; from 2024-04 onward maintained as `.zst` only by u/Watchful1 / Arthur Heitmann's Arctic Shift pipeline. Pushshift itself was shut down in mid-2023 after Reddit's API changes.
- Compression caveat: Files use a non-standard window size (`2^31`); naive `zstd`/`zstandard` decoders fail with *"Frame requires too much memory for decoding"*. Use `zstandard.ZstdDecompressor(max_window_size=2**31)` or the helpers in [Watchful1/PushshiftDumps](https://github.com/Watchful1/PushshiftDumps).
- Sibling torrents (useful as cross-checks / smaller scopes):
  - 2005-06 → 2024-12 (subreddit-partitioned): `1614740ac8c94505e4ecb9d88be8bed7b6afddd4`
  - 2005-06 → 2023-12 (full, comments+submissions): `9c263fc85366c1ef8f5bb9da0203f4c8c8db75f4`
  - Per-month single-period torrents (e.g. `2023-02`: `9971c68d2909843a100ae955c6ab6de3e09c04a1`).

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

- Which subreddits? (If <~200, the per-subreddit torrent variant is far cheaper.)
- Which time window?
- Comments, submissions, or both?
- Do we need post-ingest mutations (final score, current deletion state)?

### Phase 1 — Bulk acquisition

Primary path: **the subreddit-partitioned torrent** (this hash) when the subreddit list is known and comparatively small.

1. Install a headless BitTorrent client (`transmission-daemon`, `aria2c --enable-dht --bt-metadata-only-mode=false`, or `qbittorrent-nox`).
2. Fetch the `.torrent` from Academic Torrents; verify infohash equals `3e3f64dee22dc304cdd2546254ca1f8e8ae542b4`.
3. Use *selective download* to pull only the `.zst` files for target subreddits — the torrent's file structure is one pair (`comments`, `submissions`) per subreddit.
4. Seed back for ≥1× share ratio; this dataset depends on community seeders.
5. Verify each file: zstd frame check + line-count + `created_utc` min/max.

Fallback paths, in order:
1. Direct HTTPS mirror of the same files via Arctic Shift's [download links](https://github.com/ArthurHeitmann/arctic_shift/blob/master/download_links.md).
2. Arctic Shift API / web download tool (`arctic-shift.photon-reddit.com/download-tool`) for ad-hoc pulls.
3. PullPush API (`api.pullpush.io`) for full-text search across all of Reddit (slower, rate-limited).
4. Official Reddit API via PRAW for live state and post-2025 data.

**Single-subreddit fetch via the API (fallback path #2)** — appropriate for niche/small subs (up to roughly low millions of items) or a quick quality-assessment pull before committing to the torrent:

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

- Academic Torrents listing: https://academictorrents.com/details/3e3f64dee22dc304cdd2546254ca1f8e8ae542b4
- Watchful1, *PushshiftDumps* (helper scripts, decompression notes): https://github.com/Watchful1/PushshiftDumps
- ArthurHeitmann, *Arctic Shift* (Pushshift successor, dumps + API): https://github.com/ArthurHeitmann/arctic_shift
- Arctic Shift web UI: https://arctic-shift.photon-reddit.com/
- Baumgartner et al., *The Pushshift Reddit Dataset*, ICWSM 2020: https://arxiv.org/abs/2001.08435
- Gaffney & Matias, *Caveat emptor, computational social science: Large-scale missing data in a widely-published Reddit corpus*, PLOS ONE 2018: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6034852/
- Hessel, *Reddit Dataset Update* (gap analysis): https://www.cs.cornell.edu/~jhessel/reddit/gaps.html
- Wellformedness, *Streaming decompression for the Reddit dumps*: https://www.wellformedness.com/blog/streaming-decompression-reddit-dumps/
