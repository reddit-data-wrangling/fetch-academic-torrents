# Comics subreddit collection dashboard

_Refreshed 2026-08-07 13:45 UTC from MongoDB, the reviewed comics catalogue, `targets.txt`, shared-worker state, and `data/raw/`._

> Open with **Markdown: Open Preview** (`Ctrl+Shift+V` / `Cmd+Shift+V`). The shared tmux worker refreshes this file at every fetch, validation, and load transition.

## Status

| Panel | Complete | Active | Partial raw | Remaining | Expected records | Raw data | Workflow |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 36 | 36 | 0 | 0 | 0 | 74,329,560 | 9.0 GiB | `active` |

**MongoDB completion:** `████████████████████████` 100%

- shared worker: `fetching` — movies `r/movies` (78/78)
- tmux session: `reddit_comics_movies`
- runtime log: `data/logs/comics-movies-collection.log`
- destination: MongoDB `localhost:27019`, database `reddit`
- payload: submissions and comments
- queue policy: one low-priority worker, globally smallest expected capture first
- completion gate: both MongoDB collections and two decodable raw files per target
- combined view: [`COMICS_MOVIES_PROGRESS.md`](../../COMICS_MOVIES_PROGRESS.md)

## Next comics targets

The shared queue may interleave targets from the other collection.

| # | Subreddit | Stratum | Status | Expected records | Existing raw |
| ---: | --- | --- | --- | ---: | ---: |
| — | Queue complete | — | — | — | — |

## Progress by stratum

| Stratum | Complete | Tracked | Progress | Expected records | Raw data |
| --- | ---: | ---: | --- | ---: | ---: |
| Collecting, grading, speculation, and exchange | 3 | 3 | `██████████` 100% | 2,445,824 | 372 MiB |
| Comics creators | 1 | 1 | `██████████` 100% | 53,501 | 9 MiB |
| Conventions | 2 | 2 | `██████████` 100% | 391,114 | 56 MiB |
| Creation, critique, collaboration, and publishing | 3 | 3 | `██████████` 100% | 468,157 | 109 MiB |
| General discussion, criticism, reading, and recommendations | 5 | 5 | `██████████` 100% | 17,355,654 | 2.1 GiB |
| Genre, tradition, and historical periods | 3 | 3 | `██████████` 100% | 30,452 | 9 MiB |
| Independent, alternative, and small-press comics | 4 | 4 | `██████████` 100% | 328,349 | 54 MiB |
| Major manga series and creators | 3 | 3 | `██████████` 100% | 24,245,397 | 2.8 GiB |
| Major non-Marvel/DC series and universes | 3 | 3 | `██████████` 100% | 282,701 | 42 MiB |
| Manga, manhwa, manhua, and collecting | 4 | 4 | `██████████` 100% | 15,168,874 | 1.8 GiB |
| Marvel and DC publishing universes | 2 | 2 | `██████████` 100% | 12,658,105 | 1.5 GiB |
| Webcomics and digital platforms | 3 | 3 | `██████████` 100% | 901,432 | 179 MiB |

## Selection boundary

The acquisition panel contains 36 reviewed communities; 71 catalogue candidates are outside it.

| Excluded catalogue status | Communities |
| --- | ---: |
| missing | 11 |
| restricted | 6 |
| verified | 54 |

## All panel communities

Expand a stratum below. Use VS Code search to jump directly to a subreddit.

<details>
<summary><strong>Collecting, grading, speculation, and exchange</strong> — 3/3 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/comicbookcollecting` | 🟢 Complete | 1,389,740 | 2/2 | 221 MiB |
| `r/CGCComics` | 🟢 Complete | 100,308 | 2/2 | 16 MiB |
| `r/OmnibusCollectors` | 🟢 Complete | 955,776 | 2/2 | 134 MiB |

</details>

<details>
<summary><strong>Comics creators</strong> — 1/1 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/AlanMoore` | 🟢 Complete | 53,501 | 2/2 | 9 MiB |

</details>

<details>
<summary><strong>Conventions</strong> — 2/2 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/comiccon` | 🟢 Complete | 290,733 | 2/2 | 42 MiB |
| `r/SDCC` | 🟢 Complete | 100,381 | 2/2 | 14 MiB |

</details>

<details>
<summary><strong>Creation, critique, collaboration, and publishing</strong> — 3/3 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/ComicBookCollabs` | 🟢 Complete | 383,728 | 2/2 | 90 MiB |
| `r/comic_crits` | 🟢 Complete | 71,852 | 2/2 | 16 MiB |
| `r/Storyboarding` | 🟢 Complete | 12,577 | 2/2 | 3 MiB |

</details>

<details>
<summary><strong>General discussion, criticism, reading, and recommendations</strong> — 5/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/comicbooks` | 🟢 Complete | 8,098,044 | 2/2 | 981 MiB |
| `r/comics` | 🟢 Complete | 8,435,380 | 2/2 | 1.0 GiB |
| `r/graphicnovels` | 🟢 Complete | 602,320 | 2/2 | 89 MiB |
| `r/comicbookart` | 🟢 Complete | 208,169 | 2/2 | 37 MiB |
| `r/noDCnoMarvel` | 🟢 Complete | 11,741 | 2/2 | 4 MiB |

</details>

<details>
<summary><strong>Genre, tradition, and historical periods</strong> — 3/3 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/HorrorComics` | 🟢 Complete | 28,555 | 2/2 | 8 MiB |
| `r/scificomics` | 🟢 Complete | 1,216 | 2/2 | 733 KiB |
| `r/BronzeAgeComics` | 🟢 Complete | 681 | 2/2 | 191 KiB |

</details>

<details>
<summary><strong>Independent, alternative, and small-press comics</strong> — 4/4 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/indiecomics` | 🟢 Complete | 19,097 | 2/2 | 7 MiB |
| `r/altcomix` | 🟢 Complete | 58,300 | 2/2 | 13 MiB |
| `r/ImageComics` | 🟢 Complete | 240,486 | 2/2 | 32 MiB |
| `r/darkhorsecomics` | 🟢 Complete | 10,466 | 2/2 | 2 MiB |

</details>

<details>
<summary><strong>Major manga series and creators</strong> — 3/3 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/OnePiece` | 🟢 Complete | 21,014,758 | 2/2 | 2.4 GiB |
| `r/Berserk` | 🟢 Complete | 3,026,083 | 2/2 | 364 MiB |
| `r/junjiito` | 🟢 Complete | 204,556 | 2/2 | 28 MiB |

</details>

<details>
<summary><strong>Major non-Marvel/DC series and universes</strong> — 3/3 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/SAGAcomic` | 🟢 Complete | 41,807 | 2/2 | 5 MiB |
| `r/Spawn` | 🟢 Complete | 148,558 | 2/2 | 22 MiB |
| `r/HellBoy` | 🟢 Complete | 92,336 | 2/2 | 14 MiB |

</details>

<details>
<summary><strong>Manga, manhwa, manhua, and collecting</strong> — 4/4 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/manga` | 🟢 Complete | 11,134,154 | 2/2 | 1.3 GiB |
| `r/manhwa` | 🟢 Complete | 3,037,591 | 2/2 | 358 MiB |
| `r/Manhua` | 🟢 Complete | 592,426 | 2/2 | 75 MiB |
| `r/shoujo` | 🟢 Complete | 404,703 | 2/2 | 62 MiB |

</details>

<details>
<summary><strong>Marvel and DC publishing universes</strong> — 2/2 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/Marvel` | 🟢 Complete | 6,896,514 | 2/2 | 824 MiB |
| `r/DCcomics` | 🟢 Complete | 5,761,591 | 2/2 | 728 MiB |

</details>

<details>
<summary><strong>Webcomics and digital platforms</strong> — 3/3 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/webcomics` | 🟢 Complete | 870,737 | 2/2 | 170 MiB |
| `r/WebComic` | 🟢 Complete | 21,403 | 2/2 | 6 MiB |
| `r/GlobalComix` | 🟢 Complete | 9,292 | 2/2 | 3 MiB |

</details>

---

🟢 present in both MongoDB collections · 🟠 fetching/validating/loading · 🟡 one raw file present · ⚪ pending
