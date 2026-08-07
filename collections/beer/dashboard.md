# Beer subreddit collection dashboard

_Refreshed 2026-08-07 13:45 UTC from MongoDB, the beer catalogue, `targets.txt`, and `data/raw/`._

> Open with **Markdown: Open Preview** (`Ctrl+Shift+V` / `Cmd+Shift+V`). The tmux worker refreshes this file after every successful load.

## Status

| Panel | Complete | Active capture/load | Partial raw | Remaining | Expected records | Raw data | Workflow |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 32 | 32 | 0 | 0 | 0 | 10,577,441 | 1.3 GiB | `active` |

**MongoDB completion:** `████████████████████████` 100%

- tmux session: `reddit_beer_collection`
- runtime log: `data/logs/beer-collection.log`
- destination: MongoDB `localhost:27019`, database `reddit`
- queue policy: one low-priority worker, smallest expected capture first
- music protection: beer API requests pause while the music worker fetches
- completion gate: both MongoDB collections plus 64 decodable raw files

## Next in queue

| # | Subreddit | Stratum | Status | Expected records | Existing raw |
| ---: | --- | --- | --- | ---: | ---: |
| — | Queue complete | — | — | — | — |

## Progress by stratum

| Stratum | Complete | Tracked | Progress | Expected records | Raw data |
| --- | ---: | ---: | --- | ---: | ---: |
| Adjacent fermentation comparators | 2 | 2 | `██████████` 100% | 1,173,683 | 165 MiB |
| Brewing and production | 6 | 6 | `██████████` 100% | 4,430,725 | 585 MiB |
| General discussion and culture | 6 | 6 | `██████████` 100% | 4,113,819 | 483 MiB |
| Platforms and material culture | 2 | 2 | `██████████` 100% | 89,421 | 12 MiB |
| Regional markets — Canada | 3 | 3 | `██████████` 100% | 106,454 | 13 MiB |
| Regional markets — other countries and languages | 3 | 3 | `██████████` 100% | 97,331 | 14 MiB |
| Regional markets — United States | 5 | 5 | `██████████` 100% | 483,887 | 49 MiB |
| Styles and alternatives | 5 | 5 | `██████████` 100% | 82,121 | 11 MiB |

## Selection boundary

The acquisition panel contains 32 reviewed communities; 94 catalogue candidates are outside it.

| Excluded catalogue status | Communities |
| --- | ---: |
| missing | 6 |
| restricted | 13 |
| verified | 75 |

Cider and mead are included as an adjacent-fermentation comparator stratum and should remain separate in downstream analysis.

## All panel communities

Expand a stratum below. Use VS Code search to jump directly to a subreddit.

<details>
<summary><strong>Adjacent fermentation comparators</strong> — 2/2 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/cider` | 🟢 Complete | 175,966 | 2/2 | 25 MiB |
| `r/mead` | 🟢 Complete | 997,717 | 2/2 | 139 MiB |

</details>

<details>
<summary><strong>Brewing and production</strong> — 6/6 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/Homebrewing` | 🟢 Complete | 3,781,381 | 2/2 | 497 MiB |
| `r/homebrewingUK` | 🟢 Complete | 5,106 | 2/2 | 922 KiB |
| `r/brewing` | 🟢 Complete | 48,200 | 2/2 | 8 MiB |
| `r/TheBrewery` | 🟢 Complete | 563,715 | 2/2 | 75 MiB |
| `r/kegerators` | 🟢 Complete | 22,477 | 2/2 | 4 MiB |
| `r/grainfather` | 🟢 Complete | 9,846 | 2/2 | 2 MiB |

</details>

<details>
<summary><strong>General discussion and culture</strong> — 6/6 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/beer` | 🟢 Complete | 2,412,366 | 2/2 | 262 MiB |
| `r/CraftBeer` | 🟢 Complete | 714,904 | 2/2 | 95 MiB |
| `r/beerporn` | 🟢 Complete | 910,650 | 2/2 | 113 MiB |
| `r/beerreviews` | 🟢 Complete | 17,520 | 2/2 | 5 MiB |
| `r/beerwithaview` | 🟢 Complete | 57,907 | 2/2 | 8 MiB |
| `r/NewBeerFriday` | 🟢 Complete | 472 | 2/2 | 57 KiB |

</details>

<details>
<summary><strong>Platforms and material culture</strong> — 2/2 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/Untappd` | 🟢 Complete | 83,890 | 2/2 | 10 MiB |
| `r/breweriana` | 🟢 Complete | 5,531 | 2/2 | 1 MiB |

</details>

<details>
<summary><strong>Regional markets — Canada</strong> — 3/3 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/beercanada` | 🟢 Complete | 18,640 | 2/2 | 2 MiB |
| `r/torontocraftbeer` | 🟢 Complete | 64,212 | 2/2 | 8 MiB |
| `r/VancouverCraftBeer` | 🟢 Complete | 23,602 | 2/2 | 3 MiB |

</details>

<details>
<summary><strong>Regional markets — other countries and languages</strong> — 3/3 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/AusBeer` | 🟢 Complete | 28,469 | 2/2 | 4 MiB |
| `r/UK_beer` | 🟢 Complete | 53,479 | 2/2 | 7 MiB |
| `r/Bier` | 🟢 Complete | 15,383 | 2/2 | 3 MiB |

</details>

<details>
<summary><strong>Regional markets — United States</strong> — 5/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/atlbeer` | 🟢 Complete | 303,367 | 2/2 | 29 MiB |
| `r/chicagobeer` | 🟢 Complete | 82,664 | 2/2 | 9 MiB |
| `r/portlandbeer` | 🟢 Complete | 27,745 | 2/2 | 3 MiB |
| `r/AustinBeer` | 🟢 Complete | 55,705 | 2/2 | 6 MiB |
| `r/nycbeer` | 🟢 Complete | 14,406 | 2/2 | 2 MiB |

</details>

<details>
<summary><strong>Styles and alternatives</strong> — 5/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/BelgianBeer` | 🟢 Complete | 3,255 | 2/2 | 546 KiB |
| `r/sourbeer` | 🟢 Complete | 7,401 | 2/2 | 1 MiB |
| `r/IPA` | 🟢 Complete | 4,505 | 2/2 | 706 KiB |
| `r/NABEER` | 🟢 Complete | 66,455 | 2/2 | 9 MiB |
| `r/GlutenFreeBeer` | 🟢 Complete | 505 | 2/2 | 83 KiB |

</details>

---

🟢 present in both MongoDB collections · 🟠 two raw captures awaiting/under load · 🟡 one raw file present · ⚪ pending
