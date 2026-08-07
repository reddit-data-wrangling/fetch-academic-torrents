# Beer panel selection

Status: acquisition approved on 2026-08-03.

The reviewed panel contains 32 verified communities with approximately
941,265 archived submissions and 9,636,176 archived comments (10,577,441
records total in the 2026-07-30 catalogue snapshot). It is a broad,
stratified ecosystem panel rather than an exhaustive download of all 126
candidates.

## Strata

- **General discussion and culture (6):** broad consumer conversation,
  craft-beer culture, reviews, releases, and visual sharing.
- **Styles and alternatives (5):** Belgian and sour traditions, IPA,
  non-alcoholic beer, and gluten-free beer.
- **Brewing and production (6):** home and professional brewing, a UK-focused
  community, and equipment-oriented communities.
- **Platforms and material culture (2):** Untappd and breweriana.
- **Regional markets (11):** five US, three Canadian, and three
  international/language communities selected for geographic contrast and
  useful archive coverage.
- **Adjacent fermentation comparators (2):** cider and mead are retained as a
  separate analytical stratum, not treated as beer communities.

## Exclusions

Only communities verified by Arctic Shift are eligible. Missing and
restricted candidates are excluded from acquisition even when their
historical archives contain records. The remaining verified regional
directory entries are not selected because collecting every locality would
overweight North American geography and add many very small, overlapping
populations.

`r/beercirclejerk` is excluded despite its verified status because its current
catalogue description identifies a different topic (Yinlin), so its present
identity cannot be assumed to represent beer discourse. Individual brewery
communities and trading communities remain outside the scope. Cider and mead
must be reported separately in downstream analysis.

Acquisition runs smallest-first and loads into MongoDB `reddit` at
`mongodb://localhost:27019`. Beer API requests yield whenever the music
programme has an active fetch child.
