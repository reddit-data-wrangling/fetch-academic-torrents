# Comics and movies collection dashboard

_Refreshed 2026-08-07 13:45 UTC from MongoDB, the two reviewed catalogues, `targets.txt`, worker state, and `data/raw/`._

> Open with **Markdown: Open Preview** (`Ctrl+Shift+V` / `Cmd+Shift+V`). The shared tmux worker refreshes this file at every fetch, validation, and load transition.

## Shared programme

| Targets | Complete | Active | Partial raw | Remaining | Expected records | Raw data |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 78 | 77 | 1 | 0 | 1 | 210,323,633 | 23.4 GiB |

**MongoDB completion:** `████████████████████████` 99%

- worker: `fetching` — movies `r/movies` (78/78)
- tmux session: `reddit_comics_movies`
- runtime log: `data/logs/comics-movies-collection.log`
- destination: MongoDB `localhost:27019`, database `reddit`
- payload: submissions and comments
- queue policy: one low-priority worker, globally smallest expected capture first
- completion gate: both MongoDB collections and two decodable raw files per target

## Track status

| Track | Panel | Complete | Active | Partial | Remaining | Expected records | Raw data | Workflow |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Comics | 36 | 36 | 0 | 0 | 0 | 74,329,560 | 9.0 GiB | `active` |
| Movies | 42 | 41 | 1 | 0 | 1 | 135,994,073 | 14.3 GiB | `active` |

## Next in shared queue

| # | Track | Subreddit | Stratum | Status | Expected records | Existing raw |
| ---: | --- | --- | --- | --- | ---: | ---: |
| 1 | Movies | `r/movies` | General discussion, criticism, and recommendations | 🟠 Fetching | 70,561,597 | 2/2 files |

## Comics by stratum

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

### All comics targets

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


## Movies by stratum

| Stratum | Complete | Tracked | Progress | Expected records | Raw data |
| --- | ---: | ---: | --- | ---: | ---: |
| General discussion, criticism, and recommendations | 6 | 7 | `█████████░` 86% | 88,085,743 | 8.4 GiB |
| Genre and form | 8 | 8 | `██████████` 100% | 17,194,024 | 2.0 GiB |
| Home viewing, physical media, and preservation | 6 | 6 | `██████████` 100% | 8,091,783 | 1.0 GiB |
| Industry, exhibition, awards, and festivals | 5 | 5 | `██████████` 100% | 10,565,600 | 1.2 GiB |
| International and national cinemas | 7 | 7 | `██████████` 100% | 3,401,612 | 409 MiB |
| Production and filmmaking crafts | 7 | 7 | `██████████` 100% | 7,642,147 | 1.2 GiB |
| Studios and film labels | 2 | 2 | `██████████` 100% | 1,013,164 | 126 MiB |

### All movies targets

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
