# Collection catalogue

This directory defines the project's research collections. Read
[`WORKFLOW.md`](WORKFLOW.md) first: `subreddits.txt` contains candidate seeds,
while only reviewed names in `targets.txt` are eligible for acquisition.
Shared metadata contracts live in [`schemas/`](schemas/).

| Collection | Scope |
| --- | --- |
| [`oss`](oss/subreddits.txt) | Open-source projects, communities, governance, and development |
| [`linux`](linux/subreddits.txt) | Kernel, distributions, desktop environments, and Linux support |
| [`movies`](movies/subreddits.txt) | Film discussion, criticism, production, and genres |
| [`sci-fi`](sci-fi/subreddits.txt) | Cross-media science fiction, creation, subgenres, and futures |
| [`music`](music/subreddits.txt) | Music business, creation, listening, genres, and formats |
| [`comics`](comics/subreddits.txt) | Comic books, creators, publishers, and collecting |
| [`tv-series`](tv-series/subreddits.txt) | Television discussion, production, and genres |
| [`beer`](beer/subreddits.txt) | Beer, brewing, styles, and the trade |
| [`tabletop-games`](tabletop-games/subreddits.txt) | Board games, TTRPGs, miniatures, card games, design, and publishing |
| [`wikipedia`](wikipedia/subreddits.txt) | Wikipedia, Wikimedia projects, editing, infrastructure, and reuse |

These are collection boundaries, not analytic labels. A subreddit may appear
in more than one collection when its content genuinely crosses domains.
Deduplication by Reddit `id` in MongoDB makes overlap safe.

## Name-list rules

- Use the canonical subreddit spelling without the `r/` prefix.
- Group entries with `#` comments.
- Keep one subreddit per non-comment line.
- Record exclusions and uncertain candidates in comments rather than silently
  dropping them.
- Never copy all candidates into `targets.txt` without catalogue review and a
  documented selection rationale.

Run `python scripts/collect.py list` to see collection states or
`python scripts/collect.py status <collection>` to inspect a plan. Fetching is
deliberately gated and works only for collections marked `active`:

```bash
python scripts/catalog_subreddits.py movies
python scripts/audit_collection.py movies
```

After catalogue review, document the selection, populate `targets.txt`, mark
the corresponding `catalog.json` entries as selected, and run the audit. Set
`state = "active"` only after the audit passes:

```bash
python scripts/collect.py fetch <collection> --kind both --outdir data/raw
python scripts/collect.py load <collection> --kind both \
  --mongo-uri mongodb://localhost:27017 \
  --db reddit
```

The raw-file layout remains flat (`data/raw/<subreddit>_<kind>.zst`) for
compatibility with the existing fetcher and loader. The collection name is
metadata and orchestration, not another copy of the raw data.

Only `collect.py fetch` enforces the active-state gate. `collect.py load` does
not read the destination fields from `collection.toml`, so always pass and
verify `--mongo-uri` and `--db` explicitly.
