# Comics panel selection

Status: 36-community pilot approved for acquisition on 2026-08-04.

The pilot contains only communities verified in the 2026-07-30 Arctic Shift
catalogue snapshot. Its expected archive volume is approximately 74.3 million
records. This is a stratified research panel, not an exhaustive download of
all 107 discovery candidates.

## Panel design

- General discussion and criticism is the core stratum, with separate
  representation for graphic novels, art, and non-Marvel/DC discussion.
- Creation and collaboration, webcomics, international formats, independent
  publishing, historical periods, collecting, and conventions are sampled as
  distinct parts of the ecosystem.
- Manga/manhwa/manhua communities are included as comics traditions. Three
  series/creator communities form a deliberately separate fandom stratum.
- Marvel and DC are represented at publisher/universe level. Character-level
  communities are deferred so superhero fandom cannot dominate the pilot.
- Individual creators and non-Marvel/DC series are kept in separate strata
  rather than pooled with general comics discussion.

## Exclusions and expansion gate

Missing and restricted communities are ineligible. Generic illustration,
writing, self-publishing, and cosplay communities are excluded where comics
are incidental. Additional character, saga, creator, convention, and manga
series communities remain catalogue candidates; expansion requires archive
QA and a review of how much their discourse duplicates the pilot.

Acquisition runs globally smallest-first alongside the movies pilot and loads
both submissions and comments into MongoDB `reddit` at
`mongodb://localhost:27019`. Shared raw files and MongoDB ID upserts make
intentional overlap with movies and later collections safe.
