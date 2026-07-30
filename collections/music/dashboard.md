# Music subreddit collection dashboard

_Refreshed 2026-07-30 23:36 UTC from MongoDB, `progress.md`, and `data/raw/`._

> Open with **Markdown: Open Preview** (`Ctrl+Shift+V` / `Cmd+Shift+V`). The tmux job refreshes this file after every successful load.

## Status

| Programme | Complete | Remaining | Expected records | Raw data | Workflow |
| ---: | ---: | ---: | ---: | ---: | --- |
| 130 | 45 | 85 | 207,057,531 | 4.1 GiB | `active` |

**Subreddit completion:** `████████░░░░░░░░░░░░░░░░` 35%

- tmux session: `reddit_music_resume`
- runtime log: `data/logs/music-resume.log`
- destination: MongoDB `localhost:27019`, database `reddit`
- queue policy: one worker, smallest expected capture first

## Next in queue

| # | Subreddit | Category | Expected records | Existing raw |
| ---: | --- | --- | ---: | ---: |
| 1 | `r/JazzPiano` | jazz | 58,497 | 0/2 files |
| 2 | `r/housemusic` | electronic | 70,102 | 0/2 files |
| 3 | `r/plexamp` | streaming | 73,025 | 0/2 files |
| 4 | `r/Bachata` | latin | 87,195 | 0/2 files |
| 5 | `r/folk` | country | 97,346 | 0/2 files |
| 6 | `r/BedroomBands` | indie-artists | 105,406 | 0/2 files |
| 7 | `r/CountryMusic` | country | 106,174 | 0/2 files |
| 8 | `r/bandmembers` | producers | 111,624 | 0/2 files |
| 9 | `r/IDM` | electronic | 125,870 | 0/2 files |
| 10 | `r/1001AlbumsGenerator` | discovery | 129,266 | 0/2 files |
| 11 | `r/altcountry` | country | 130,094 | 0/2 files |
| 12 | `r/Salsa` | latin | 144,499 | 0/2 files |
| 13 | `r/Reggaeton` | latin | 152,925 | 0/2 files |
| 14 | `r/newmusic` | discovery | 193,998 | 0/2 files |
| 15 | `r/Bluegrass` | country | 227,112 | 0/2 files |

## Progress by category

| Category | Complete | Tracked | Progress | Expected records | Raw data |
| --- | ---: | ---: | --- | ---: | ---: |
| adjacent | 5 | 5 | `██████████` 100% | 5,290,131 | 805 MiB |
| audiophile | 0 | 4 | `░░░░░░░░░░` 0% | 10,853,554 | 0 B |
| classical | 0 | 5 | `░░░░░░░░░░` 0% | 5,700,478 | 0 B |
| core | 13 | 13 | `██████████` 100% | 1,352,605 | 205 MiB |
| country | 1 | 5 | `██░░░░░░░░` 20% | 575,118 | 4 MiB |
| discovery | 5 | 9 | `██████░░░░` 56% | 42,452,568 | 1.3 GiB |
| discussion | 3 | 5 | `██████░░░░` 60% | 17,869,063 | 1.1 GiB |
| electronic | 4 | 18 | `██░░░░░░░░` 22% | 14,412,154 | 345 MiB |
| hiphop | 0 | 10 | `░░░░░░░░░░` 0% | 48,989,048 | 0 B |
| indie-artists | 1 | 5 | `██░░░░░░░░` 20% | 1,753,125 | 11 MiB |
| jazz | 3 | 6 | `█████░░░░░` 50% | 1,806,484 | 13 MiB |
| latin | 1 | 4 | `██░░░░░░░░` 25% | 386,573 | 829 KiB |
| metal | 0 | 6 | `░░░░░░░░░░` 0% | 10,550,699 | 0 B |
| physical | 1 | 5 | `██░░░░░░░░` 20% | 9,477,654 | 3 MiB |
| platform | 2 | 3 | `███████░░░` 67% | 712,241 | 27 MiB |
| pop | 1 | 4 | `██░░░░░░░░` 25% | 13,111,162 | 5 MiB |
| producers | 2 | 5 | `████░░░░░░` 40% | 7,562,588 | 363 MiB |
| rock | 0 | 9 | `░░░░░░░░░░` 0% | 9,151,968 | 0 B |
| sampling | 2 | 2 | `██████████` 100% | 31,270 | 7 MiB |
| streaming | 1 | 7 | `█░░░░░░░░░` 14% | 5,019,048 | 7 MiB |

## All subreddits

Expand a category below. Use VS Code search to jump directly to a subreddit.

<details>
<summary><strong>adjacent</strong> — 5/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/Ticketmaster` | 🟢 Complete | 50,069 | 2/2 | 7 MiB |
| `r/BandCamp` | 🟢 Complete | 192,423 | 2/2 | 34 MiB |
| `r/truespotify` | 🟢 Complete | 478,709 | 2/2 | 67 MiB |
| `r/SpotifyPlaylists` | 🟢 Complete | 824,576 | 2/2 | 178 MiB |
| `r/WeAreTheMusicMakers` | 🟢 Complete | 3,744,354 | 2/2 | 519 MiB |

</details>

<details>
<summary><strong>audiophile</strong> — 0/4 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/audio` | ⚪ Pending | 474,399 | 0/2 | — |
| `r/BudgetAudiophile` | ⚪ Pending | 1,884,342 | 0/2 | — |
| `r/audiophile` | ⚪ Pending | 3,569,576 | 0/2 | — |
| `r/headphones` | ⚪ Pending | 4,925,237 | 0/2 | — |

</details>

<details>
<summary><strong>classical</strong> — 0/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/opera` | ⚪ Pending | 341,749 | 0/2 | — |
| `r/composer` | ⚪ Pending | 393,049 | 0/2 | — |
| `r/violinist` | ⚪ Pending | 725,771 | 0/2 | — |
| `r/classicalmusic` | ⚪ Pending | 1,954,698 | 0/2 | — |
| `r/piano` | ⚪ Pending | 2,285,211 | 0/2 | — |

</details>

<details>
<summary><strong>core</strong> — 13/13 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/musiclaw` | 🟢 Complete | 161 | 2/2 | 56 KiB |
| `r/SellingBeats` | 🟢 Complete | 95 | 2/2 | 26 KiB |
| `r/musicpublishing` | 🟢 Complete | 956 | 2/2 | 230 KiB |
| `r/synclicensing` | 🟢 Complete | 4,539 | 2/2 | 838 KiB |
| `r/recordlabels` | 🟢 Complete | 8,759 | 2/2 | 2 MiB |
| `r/MusicDistribution` | 🟢 Complete | 16,208 | 2/2 | 3 MiB |
| `r/UnitedMasters` | 🟢 Complete | 16,624 | 2/2 | 2 MiB |
| `r/TouringMusicians` | 🟢 Complete | 37,413 | 2/2 | 6 MiB |
| `r/musicbusiness` | 🟢 Complete | 51,945 | 2/2 | 10 MiB |
| `r/DistroKidHelpDesk` | 🟢 Complete | 78,734 | 2/2 | 11 MiB |
| `r/musicindustry` | 🟢 Complete | 138,213 | 2/2 | 24 MiB |
| `r/musicmarketing` | 🟢 Complete | 241,125 | 2/2 | 38 MiB |
| `r/MusicPromotion` | 🟢 Complete | 757,833 | 2/2 | 108 MiB |

</details>

<details>
<summary><strong>country</strong> — 1/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/Americana` | 🟢 Complete | 14,392 | 2/2 | 4 MiB |
| `r/folk` | ⚪ Pending | 97,346 | 0/2 | — |
| `r/CountryMusic` | ⚪ Pending | 106,174 | 0/2 | — |
| `r/altcountry` | ⚪ Pending | 130,094 | 0/2 | — |
| `r/Bluegrass` | ⚪ Pending | 227,112 | 0/2 | — |

</details>

<details>
<summary><strong>discovery</strong> — 5/9 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/vintageobscura` | 🟢 Complete | 117,162 | 2/2 | 29 MiB |
| `r/ifyoulikeblank` | 🟢 Complete | 1,880,530 | 2/2 | 218 MiB |
| `r/listentothis` | 🟢 Complete | 3,302,579 | 2/2 | 494 MiB |
| `r/musicsuggestions` | 🟢 Complete | 5,816,228 | 2/2 | 569 MiB |
| `r/Music` | ⚪ Pending | 28,144,040 | 0/2 | — |
| `r/Albumoftheday` | 🟢 Complete | 2,390 | 2/2 | 710 KiB |
| `r/1001AlbumsGenerator` | ⚪ Pending | 129,266 | 0/2 | — |
| `r/newmusic` | ⚪ Pending | 193,998 | 0/2 | — |
| `r/MusicRecommendations` | ⚪ Pending | 2,866,375 | 0/2 | — |

</details>

<details>
<summary><strong>discussion</strong> — 3/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/LetsTalkMusic` | 🟢 Complete | 1,180,999 | 2/2 | 207 MiB |
| `r/fantanoforever` | 🟢 Complete | 3,185,542 | 2/2 | 363 MiB |
| `r/indieheads` | 🟢 Complete | 4,466,705 | 2/2 | 544 MiB |
| `r/popheads` | ⚪ Pending | 7,569,395 | 0/2 | — |
| `r/Topster` | ⚪ Pending | 1,466,422 | 0/2 | — |

</details>

<details>
<summary><strong>electronic</strong> — 4/18 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/TheOverload` | 🟢 Complete | 203,109 | 2/2 | 37 MiB |
| `r/vaporwave` | 🟢 Complete | 553,397 | 2/2 | 81 MiB |
| `r/electronicmusic` | 🟢 Complete | 1,682,465 | 2/2 | 220 MiB |
| `r/synthwave` | 🟢 Complete | 31,880 | 2/2 | 7 MiB |
| `r/housemusic` | ⚪ Pending | 70,102 | 0/2 | — |
| `r/IDM` | ⚪ Pending | 125,870 | 0/2 | — |
| `r/realdubstep` | ⚪ Pending | 289,732 | 0/2 | — |
| `r/psytrance` | ⚪ Pending | 301,434 | 0/2 | — |
| `r/ambientmusic` | ⚪ Pending | 331,158 | 0/2 | — |
| `r/futurebeats` | ⚪ Pending | 351,807 | 0/2 | — |
| `r/outrun` | ⚪ Pending | 485,435 | 0/2 | — |
| `r/techno` | ⚪ Pending | 839,519 | 0/2 | — |
| `r/dnb` | ⚪ Pending | 1,008,284 | 0/2 | — |
| `r/edm` | ⚪ Pending | 2,240,987 | 0/2 | — |
| `r/House` | ⚪ Pending | 368,008 | 0/2 | — |
| `r/trance` | ⚪ Pending | 691,677 | 0/2 | — |
| `r/modular` | ⚪ Pending | 845,133 | 0/2 | — |
| `r/synthesizers` | ⚪ Pending | 3,992,157 | 0/2 | — |

</details>

<details>
<summary><strong>hiphop</strong> — 0/10 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/Jcole` | ⚪ Pending | 800,328 | 0/2 | — |
| `r/trap` | ⚪ Pending | 1,111,508 | 0/2 | — |
| `r/hiphop101` | ⚪ Pending | 2,075,706 | 0/2 | — |
| `r/WestSubEver` | ⚪ Pending | 2,495,359 | 0/2 | — |
| `r/makinghiphop` | ⚪ Pending | 2,946,542 | 0/2 | — |
| `r/rap` | ⚪ Pending | 3,180,780 | 0/2 | — |
| `r/Drizzy` | ⚪ Pending | 3,341,307 | 0/2 | — |
| `r/KendrickLamar` | ⚪ Pending | 4,179,841 | 0/2 | — |
| `r/Eminem` | ⚪ Pending | 5,327,799 | 0/2 | — |
| `r/hiphopheads` | ⚪ Pending | 23,529,878 | 0/2 | — |

</details>

<details>
<summary><strong>indie-artists</strong> — 1/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/ratemysong` | 🟢 Complete | 44,617 | 2/2 | 11 MiB |
| `r/BedroomBands` | ⚪ Pending | 105,406 | 0/2 | — |
| `r/ThisIsOurMusic` | ⚪ Pending | 426,816 | 0/2 | — |
| `r/PromoteYourMusic` | ⚪ Pending | 472,968 | 0/2 | — |
| `r/shareyourmusic` | ⚪ Pending | 703,318 | 0/2 | — |

</details>

<details>
<summary><strong>jazz</strong> — 3/6 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/smoothjazz` | 🟢 Complete | 4,436 | 2/2 | 1 MiB |
| `r/jazztheory` | 🟢 Complete | 28,381 | 2/2 | 5 MiB |
| `r/JazzFusion` | 🟢 Complete | 35,417 | 2/2 | 7 MiB |
| `r/JazzPiano` | ⚪ Pending | 58,497 | 0/2 | — |
| `r/jazzguitar` | ⚪ Pending | 259,948 | 0/2 | — |
| `r/Jazz` | ⚪ Pending | 1,419,805 | 0/2 | — |

</details>

<details>
<summary><strong>latin</strong> — 1/4 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/latinmusic` | 🟢 Complete | 1,954 | 2/2 | 829 KiB |
| `r/Bachata` | ⚪ Pending | 87,195 | 0/2 | — |
| `r/Salsa` | ⚪ Pending | 144,499 | 0/2 | — |
| `r/Reggaeton` | ⚪ Pending | 152,925 | 0/2 | — |

</details>

<details>
<summary><strong>metal</strong> — 0/6 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/BlackMetal` | ⚪ Pending | 549,730 | 0/2 | — |
| `r/doommetal` | ⚪ Pending | 766,553 | 0/2 | — |
| `r/progmetal` | ⚪ Pending | 1,244,067 | 0/2 | — |
| `r/Deathcore` | ⚪ Pending | 1,327,134 | 0/2 | — |
| `r/Metal` | ⚪ Pending | 2,913,815 | 0/2 | — |
| `r/Metalcore` | ⚪ Pending | 3,749,400 | 0/2 | — |

</details>

<details>
<summary><strong>physical</strong> — 1/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/recordstore` | 🟢 Complete | 18,003 | 2/2 | 3 MiB |
| `r/cassetteculture` | ⚪ Pending | 841,844 | 0/2 | — |
| `r/turntables` | ⚪ Pending | 1,167,233 | 0/2 | — |
| `r/Cd_collectors` | ⚪ Pending | 1,275,226 | 0/2 | — |
| `r/vinyl` | ⚪ Pending | 6,175,348 | 0/2 | — |

</details>

<details>
<summary><strong>platform</strong> — 2/3 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/soundcloud` | ⚪ Pending | 597,578 | 0/2 | — |
| `r/SoundCloudMusic` | 🟢 Complete | 25,524 | 2/2 | 7 MiB |
| `r/SoundCloudHipHop` | 🟢 Complete | 89,139 | 2/2 | 20 MiB |

</details>

<details>
<summary><strong>pop</strong> — 1/4 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/popmusic` | 🟢 Complete | 31,208 | 2/2 | 5 MiB |
| `r/kpophelp` | ⚪ Pending | 2,033,911 | 0/2 | — |
| `r/kpopthoughts` | ⚪ Pending | 3,891,535 | 0/2 | — |
| `r/kpop` | ⚪ Pending | 7,154,508 | 0/2 | — |

</details>

<details>
<summary><strong>producers</strong> — 2/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/Songwriting` | 🟢 Complete | 997,098 | 2/2 | 161 MiB |
| `r/musicproduction` | 🟢 Complete | 1,453,070 | 2/2 | 203 MiB |
| `r/bandmembers` | ⚪ Pending | 111,624 | 0/2 | — |
| `r/edmproduction` | ⚪ Pending | 2,461,291 | 0/2 | — |
| `r/audioengineering` | ⚪ Pending | 2,539,505 | 0/2 | — |

</details>

<details>
<summary><strong>rock</strong> — 0/9 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/postrock` | ⚪ Pending | 312,483 | 0/2 | — |
| `r/indie` | ⚪ Pending | 392,338 | 0/2 | — |
| `r/rock` | ⚪ Pending | 418,951 | 0/2 | — |
| `r/shoegaze` | ⚪ Pending | 530,013 | 0/2 | — |
| `r/progrockmusic` | ⚪ Pending | 740,638 | 0/2 | — |
| `r/grunge` | ⚪ Pending | 1,076,885 | 0/2 | — |
| `r/Emo` | ⚪ Pending | 1,289,740 | 0/2 | — |
| `r/ClassicRock` | ⚪ Pending | 1,364,503 | 0/2 | — |
| `r/punk` | ⚪ Pending | 3,026,417 | 0/2 | — |

</details>

<details>
<summary><strong>sampling</strong> — 2/2 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/sampling` | 🟢 Complete | 6,166 | 2/2 | 1 MiB |
| `r/Samplehunters` | 🟢 Complete | 25,104 | 2/2 | 6 MiB |

</details>

<details>
<summary><strong>streaming</strong> — 1/7 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/qobuz` | 🟢 Complete | 44,098 | 2/2 | 7 MiB |
| `r/plexamp` | ⚪ Pending | 73,025 | 0/2 | — |
| `r/TIdaL` | ⚪ Pending | 263,672 | 0/2 | — |
| `r/YoutubeMusic` | ⚪ Pending | 415,026 | 0/2 | — |
| `r/lastfm` | ⚪ Pending | 976,292 | 0/2 | — |
| `r/AppleMusic` | ⚪ Pending | 1,051,589 | 0/2 | — |
| `r/spotify` | ⚪ Pending | 2,195,346 | 0/2 | — |

</details>

---

🟢 present in both MongoDB collections · 🟠 fetching/loading · 🟡 one raw file present · ⚪ pending
