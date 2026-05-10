# Data collection log

Source: Arctic Shift API (`arctic-shift.photon-reddit.com`) via [scripts/fetch_subreddit.py](../scripts/fetch_subreddit.py).
Output: zstd-compressed NDJSON in [data/raw/](raw/), one file per `(subreddit, kind)`.

## 2026-05-10

| Subreddit     | Submissions |  Comments | Subm. size | Comm. size | Submissions edge | Comments edge |
| ------------- | ----------: | --------: | ---------: | ---------: | ---------------- | ------------- |
| wikipedia     |     116,628 | 1,061,855 |      27 MB |     123 MB | 2026-04-19       | 2026-04-08    |
| linux         |     294,236 | 5,354,162 |      66 MB |     649 MB | 2026-04-25       | 2026-05-10    |
| linusrants    |         210 |     1,595 |      48 KB |     205 KB | —                | 2021-10-22    |
| rust          |     137,847 | 1,580,400 |      48 MB |     241 MB | 2026-04-22       | 2026-04-09    |
| sampling      |       1,786 |     3,546 |     775 KB |     451 KB | 2024-05-03       | 2026-03-05    |
| Samplehunters |      13,809 |    11,030 |     4.4 MB |     1.1 MB | 2025-08-23       | 2026-03-30    |

Edges = last `created_utc` reached during paging (sidecar `.cursor` files). The Arctic Shift index normally lags real-time by a few weeks; gaps before today reflect that, not premature termination. Re-running the fetcher resumes from each cursor.

### Notes

- One bug fixed at the start: the API rejects `after=0` ("must be a valid date"), so [scripts/fetch_subreddit.py:67](../scripts/fetch_subreddit.py#L67) now passes `None` when the cursor is 0, letting `urlencode` drop the parameter.
- One transient HTTP 422 hit during r/linux comments around timestamp 1328745842 (Feb 2012); the script's exponential-backoff retry recovered without intervention.
