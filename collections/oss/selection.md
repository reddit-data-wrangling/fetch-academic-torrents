# Open-source software panel selection

Status: verified-community census approved for acquisition on 2026-08-07.

The acquisition panel contains all 120 communities marked `verified` in the
2026-07-30 Arctic Shift catalogue snapshot. The expected archive volume is
approximately 66.4 million submissions and comments. This is a census of the
verified candidate frame, not a size-ranked sample, so small contributor and
project communities remain represented alongside large general communities.

## Design

- Movement-level discussion, contribution and collaboration, foundations,
  languages, frameworks, data systems, infrastructure, developer tools,
  end-user applications, self-hosting, scientific computing, and gaming are
  retained as separate descriptive strata.
- Project-specific support communities are included because project use,
  maintenance, governance, and contributor experience are all within scope.
- Intentional overlap with Linux and other collections is retained. Shared raw
  captures are reused and MongoDB ID upserts provide record-level deduplication.
- `r/homebrew` is retained as an explicitly labelled adjacent comparator because
  the discovered community concerns console homebrew rather than the macOS/Linux
  package manager.

## Exclusions

The three missing and seven restricted candidates are ineligible for this
acquisition. They remain in `subreddits.txt` and `catalog.json` as discovery and
verification evidence but are not present in `targets.txt`.

Acquisition runs smallest-first and loads submissions and comments into MongoDB
`reddit` at `mongodb://localhost:27017`. The low-priority OSS API worker yields
while the comics/movies worker has an active fetch child.
