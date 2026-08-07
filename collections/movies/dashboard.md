# Movies subreddit collection dashboard

_Refreshed 2026-08-07 13:45 UTC from MongoDB, the reviewed movies catalogue, `targets.txt`, shared-worker state, and `data/raw/`._

> Open with **Markdown: Open Preview** (`Ctrl+Shift+V` / `Cmd+Shift+V`). The shared tmux worker refreshes this file at every fetch, validation, and load transition.

## Status

| Panel | Complete | Active | Partial raw | Remaining | Expected records | Raw data | Workflow |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 42 | 41 | 1 | 0 | 1 | 135,994,073 | 14.3 GiB | `active` |

**MongoDB completion:** `████████████████████████` 98%

- shared worker: `fetching` — movies `r/movies` (78/78)
- tmux session: `reddit_comics_movies`
- runtime log: `data/logs/comics-movies-collection.log`
- destination: MongoDB `localhost:27019`, database `reddit`
- payload: submissions and comments
- queue policy: one low-priority worker, globally smallest expected capture first
- completion gate: both MongoDB collections and two decodable raw files per target
- combined view: [`COMICS_MOVIES_PROGRESS.md`](../../COMICS_MOVIES_PROGRESS.md)

## Next movies targets

The shared queue may interleave targets from the other collection.

| # | Subreddit | Stratum | Status | Expected records | Existing raw |
| ---: | --- | --- | --- | ---: | ---: |
| 1 | `r/movies` | General discussion, criticism, and recommendations | 🟠 Fetching | 70,561,597 | 2/2 files |

## Progress by stratum

| Stratum | Complete | Tracked | Progress | Expected records | Raw data |
| --- | ---: | ---: | --- | ---: | ---: |
| General discussion, criticism, and recommendations | 6 | 7 | `█████████░` 86% | 88,085,743 | 8.4 GiB |
| Genre and form | 8 | 8 | `██████████` 100% | 17,194,024 | 2.0 GiB |
| Home viewing, physical media, and preservation | 6 | 6 | `██████████` 100% | 8,091,783 | 1.0 GiB |
| Industry, exhibition, awards, and festivals | 5 | 5 | `██████████` 100% | 10,565,600 | 1.2 GiB |
| International and national cinemas | 7 | 7 | `██████████` 100% | 3,401,612 | 409 MiB |
| Production and filmmaking crafts | 7 | 7 | `██████████` 100% | 7,642,147 | 1.2 GiB |
| Studios and film labels | 2 | 2 | `██████████` 100% | 1,013,164 | 126 MiB |

## Selection boundary

The acquisition panel contains 42 reviewed communities; 127 catalogue candidates are outside it.

| Excluded catalogue status | Communities |
| --- | ---: |
| missing | 18 |
| restricted | 13 |
| verified | 96 |

## All panel communities

Expand a stratum below. Use VS Code search to jump directly to a subreddit.

<details>
<summary><strong>General discussion, criticism, and recommendations</strong> — 6/7 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/movies` | 🟠 Fetching | 70,561,597 | 2/2 | 6.5 GiB |
| `r/TrueFilm` | 🟢 Complete | 1,207,670 | 2/2 | 251 MiB |
| `r/flicks` | 🟢 Complete | 1,126,292 | 2/2 | 145 MiB |
| `r/Cinema` | 🟢 Complete | 2,372,617 | 2/2 | 261 MiB |
| `r/MovieSuggestions` | 🟢 Complete | 6,929,703 | 2/2 | 614 MiB |
| `r/MovieReviews` | 🟢 Complete | 106,658 | 2/2 | 22 MiB |
| `r/Letterboxd` | 🟢 Complete | 5,781,206 | 2/2 | 723 MiB |

</details>

<details>
<summary><strong>Genre and form</strong> — 8/8 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/horror` | 🟢 Complete | 11,633,042 | 2/2 | 1.3 GiB |
| `r/ActionMovies` | 🟢 Complete | 100,988 | 2/2 | 14 MiB |
| `r/westerns` | 🟢 Complete | 395,655 | 2/2 | 46 MiB |
| `r/filmnoir` | 🟢 Complete | 65,703 | 2/2 | 9 MiB |
| `r/Documentaries` | 🟢 Complete | 4,634,421 | 2/2 | 547 MiB |
| `r/cultcinema` | 🟢 Complete | 41,221 | 2/2 | 9 MiB |
| `r/FoundFootage` | 🟢 Complete | 308,132 | 2/2 | 38 MiB |
| `r/ExperimentalFilm` | 🟢 Complete | 14,862 | 2/2 | 4 MiB |

</details>

<details>
<summary><strong>Home viewing, physical media, and preservation</strong> — 6/6 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/criterion` | 🟢 Complete | 2,384,919 | 2/2 | 282 MiB |
| `r/dvdcollection` | 🟢 Complete | 1,703,539 | 2/2 | 217 MiB |
| `r/Bluray` | 🟢 Complete | 499,636 | 2/2 | 74 MiB |
| `r/4kbluray` | 🟢 Complete | 1,736,485 | 2/2 | 222 MiB |
| `r/VHS` | 🟢 Complete | 920,649 | 2/2 | 138 MiB |
| `r/boutiquebluray` | 🟢 Complete | 846,555 | 2/2 | 114 MiB |

</details>

<details>
<summary><strong>Industry, exhibition, awards, and festivals</strong> — 5/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/boxoffice` | 🟢 Complete | 7,158,572 | 2/2 | 842 MiB |
| `r/OscarRace` | 🟢 Complete | 1,759,060 | 2/2 | 218 MiB |
| `r/Oscars` | 🟢 Complete | 1,280,315 | 2/2 | 152 MiB |
| `r/FilmFestivals` | 🟢 Complete | 120,908 | 2/2 | 15 MiB |
| `r/FilmIndustryLA` | 🟢 Complete | 246,745 | 2/2 | 37 MiB |

</details>

<details>
<summary><strong>International and national cinemas</strong> — 7/7 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/ForeignMovies` | 🟢 Complete | 27,371 | 2/2 | 6 MiB |
| `r/JapaneseMovies` | 🟢 Complete | 32,861 | 2/2 | 6 MiB |
| `r/Koreanfilm` | 🟢 Complete | 87,803 | 2/2 | 12 MiB |
| `r/bollywood` | 🟢 Complete | 2,137,683 | 2/2 | 250 MiB |
| `r/MalayalamMovies` | 🟢 Complete | 1,110,093 | 2/2 | 133 MiB |
| `r/AfricanCinema` | 🟢 Complete | 2,094 | 2/2 | 551 KiB |
| `r/IrishFilm` | 🟢 Complete | 3,707 | 2/2 | 888 KiB |

</details>

<details>
<summary><strong>Production and filmmaking crafts</strong> — 7/7 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/Filmmakers` | 🟢 Complete | 2,579,819 | 2/2 | 413 MiB |
| `r/Screenwriting` | 🟢 Complete | 2,356,816 | 2/2 | 368 MiB |
| `r/cinematography` | 🟢 Complete | 976,784 | 2/2 | 158 MiB |
| `r/editors` | 🟢 Complete | 853,968 | 2/2 | 130 MiB |
| `r/LocationSound` | 🟢 Complete | 169,906 | 2/2 | 27 MiB |
| `r/VFX` | 🟢 Complete | 678,982 | 2/2 | 107 MiB |
| `r/indiefilm` | 🟢 Complete | 25,872 | 2/2 | 8 MiB |

</details>

<details>
<summary><strong>Studios and film labels</strong> — 2/2 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/A24` | 🟢 Complete | 634,548 | 2/2 | 79 MiB |
| `r/Pixar` | 🟢 Complete | 378,616 | 2/2 | 47 MiB |

</details>

---

🟢 present in both MongoDB collections · 🟠 fetching/validating/loading · 🟡 one raw file present · ⚪ pending
