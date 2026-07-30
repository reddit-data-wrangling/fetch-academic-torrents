# Collection workflow

A subreddit name is not automatically a download target. Each domain moves
through six explicit stages:

1. **Scope** — define the research questions and boundaries. Decide whether
   adjacent communities, franchises, individual artists/shows, and inactive
   communities belong.
2. **Discover** — gather candidate names systematically from Reddit search,
   related-community links, directories, web search, and snowballing from
   verified communities. `subreddits.txt` is a candidate seed list only.
3. **Verify and catalogue** — confirm that each community exists and record
   its metadata in `catalog.json` using
   [`schemas/catalog.schema.json`](schemas/catalog.schema.json). Record the
   date and source because membership and activity change.
4. **Select** — choose a research panel from the catalogue. Only reviewed
   names go in `targets.txt`; this is the sole input accepted by the fetch
   command.
5. **Acquire and load** — fetch sequentially from Arctic Shift, retain raw
   `.zst`, run QA, then load into an explicitly confirmed MongoDB target.
6. **Inventory** — record what was actually acquired in `inventory.json`.
   Inventory is evidence, whereas cursors and planned targets are operational
   state.

## Why discovery and selection are separate

A complete domain catalogue may be much larger than a useful research panel.
For movies, general discussion, criticism, industry, production, genres,
national cinemas, directors, studios, and franchises could produce hundreds
of communities. Downloading all of them would mix several populations,
duplicate overlapping discussions, and spend substantial storage before the
research design is settled.

The catalogue supports deliberate panels, for example:

- a broad ecosystem panel stratified by category and activity;
- an industry/consumer-behaviour panel;
- matched communities across genres or countries;
- a core panel plus separately analysed franchise communities.

Selection decisions belong in `selection.md`, including exclusions and the
sampling logic. A target should not be selected merely because it is large.

## Files in each collection

| File | Role |
| --- | --- |
| `collection.toml` | Collection state and intended storage metadata |
| `scope.md` | Research scope, boundaries, and questions |
| `subreddits.txt` | Candidate seeds; never fetched directly |
| `catalog.json` | Candidate metadata, verification, classification, and selection |
| `selection.md` | Panel design and inclusion/exclusion rationale |
| `targets.txt` | Reviewed acquisition allowlist |
| `inventory.json` | Known raw holdings, recorded Mongo evidence, and QA state |
| `progress.md` | Optional narrative log for a large running collection |

## Catalogue fields

[`schemas/catalog.schema.json`](schemas/catalog.schema.json) defines the
portable nested schema. Important distinctions:

- `current_snapshot.subscribers` and
  `current_snapshot.activity.posts_per_week` are measured values, not
  impressions.
- `current_snapshot.activity.band` should follow a documented rule.
- `classification.research_domains` is an array and may contain several
  labels.
- `verification.status` distinguishes states such as verified, missing,
  private, restricted, banned, quarantined, renamed, and uncertain.
- `selection.selected` is a manual decision; it is not inferred from size or
  activity.
- `verification.verified_at` and `verification.source` make volatile metadata
  auditable.

Reusable commands:

```bash
# Verify candidates and refresh factual Arctic Shift metadata. Manual columns
# in an existing catalogue are preserved.
python scripts/catalog_subreddits.py movies

# After changing the candidate boundary, remove stale catalogue entries without
# making network requests.
python scripts/catalog_subreddits.py movies --prune-only

# Check the catalogue envelope, duplicates, target verification/selection,
# state, and raw coverage without making network requests.
python scripts/audit_collection.py movies

# Refresh raw paths/sizes cheaply; add --scan when counts and time edges are
# worth a full decompression pass.
python scripts/inventory_raw.py linux --scope candidates

# Produce a reviewable Markdown snapshot from any catalogue.
python scripts/report_catalog.py movies --output collections/movies/report.md
```

The catalogue command does not invent classifications. It fills the factual
fields available from Arctic Shift and leaves category, research domains,
measured recent activity, related communities, and selection for review.
When a catalogue category is blank, `report_catalog.py` uses the nearest `##`
group heading from `subreddits.txt` as a display-only fallback; it does not
write that category into `catalog.json`.

## Safety gates

`scripts/collect.py fetch` requires:

- a non-empty `targets.txt`;
- `state = "active"` in `collection.toml`;
- a matching `catalog.json` entry for every target;
- `verification.status = "verified"` for every target; and
- `selection.selected = true` for every target.

Planning and paused collections can still be listed and inspected, but cannot
be fetched accidentally. Change the state only after catalogue review,
selection, storage budgeting, and destination confirmation.

The state gate applies to `collect.py fetch`, not `collect.py load` or direct
invocation of `fetch_subreddit.py`. The load wrapper also does not read the
MongoDB destination from `collection.toml`; pass `--mongo-uri` and `--db`
explicitly and verify them before loading.

## State values

| State | Meaning |
| --- | --- |
| `planning` | Scope, catalogue, or selection is incomplete |
| `active` | The reviewed target panel is approved for collection |
| `paused` | Do not continue acquisition until the pause is reconciled |

## Resume safety

The API fetcher keeps a `.cursor` beside each `.zst` file and appends compressed
frames when it resumes. Keep the pair together and do not mix bounded and
full-history runs in the same output directory. After a forced termination,
decode the affected file before resuming; a partial final frame can be
corrupt. Use a scratch output directory for experiments with `--after` or
`--before`.

## Inventory semantics

`inventory_raw.py` records only files it finds; it preserves older inventory
rows for files no longer present. Its default pass records paths and sizes,
whereas `--scan` fully decompresses files to compute record counts and time
edges. The recorded paths are absolute and machine-specific. Inventory may
retain legacy or out-of-scope holdings that are no longer in the current
candidate list; document those rows rather than deleting historical evidence.
For newly discovered raw files, the command copies the manifest's intended
MongoDB destination into the inventory but does not query MongoDB. A populated
`mongo` object alone is therefore not proof that the file was loaded; preserve
or add record-count and provenance notes when load state has been verified.
