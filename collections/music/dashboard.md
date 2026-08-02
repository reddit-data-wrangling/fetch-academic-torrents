# Music subreddit collection dashboard

_Refreshed 2026-08-02 16:21 UTC from MongoDB, `progress.md`, and `data/raw/`._

> Open with **Markdown: Open Preview** (`Ctrl+Shift+V` / `Cmd+Shift+V`). The tmux job refreshes this file after every successful load.

## Status

| Programme | Complete | Remaining | Expected records | Raw data | Workflow |
| ---: | ---: | ---: | ---: | ---: | --- |
| 130 | 121 | 9 | 207,057,531 | 14.8 GiB | `active` |

**Subreddit completion:** `██████████████████████░░` 93%

- tmux session: `reddit_music_resume`
- runtime log: `data/logs/music-resume.log`
- destination: MongoDB `localhost:27019`, database `reddit`
- queue policy: one worker, smallest expected capture first

## Next in queue

| # | Subreddit | Category | Expected records | Existing raw |
| ---: | --- | --- | ---: | ---: |
| 1 | `r/synthesizers` | electronic | 3,992,157 | 1/2 files |
| 2 | `r/KendrickLamar` | hiphop | 4,179,841 | 0/2 files |
| 3 | `r/headphones` | audiophile | 4,925,237 | 0/2 files |
| 4 | `r/Eminem` | hiphop | 5,327,799 | 0/2 files |
| 5 | `r/vinyl` | physical | 6,175,348 | 0/2 files |
| 6 | `r/kpop` | pop | 7,154,508 | 0/2 files |
| 7 | `r/popheads` | discussion | 7,569,395 | 0/2 files |
| 8 | `r/hiphopheads` | hiphop | 23,529,878 | 0/2 files |
| 9 | `r/Music` | discovery | 28,144,040 | 0/2 files |

## Pending candidates

These catalogue entries are outside the authorised 130-subreddit programme and are not in its acquisition queue.

| Subreddit | Category | Verification | Expected archive records | Selection |
| --- | --- | --- | ---: | --- |
| `r/billboard` | awards-and-charts | verified | 2,532 | Pending review |
| `r/grammys` | awards-and-charts | verified | 51,816 | Pending review |

## Progress by category

| Category | Scope | Complete | Tracked | Progress | Expected records | Raw data |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| adjacent | Programme | 5 | 5 | `██████████` 100% | 5,290,131 | 805 MiB |
| audiophile | Programme | 3 | 4 | `████████░░` 75% | 10,853,554 | 846 MiB |
| awards-and-charts | Candidate | 0 | 2 | `░░░░░░░░░░` 0% | 54,348 | 0 B |
| classical | Programme | 5 | 5 | `██████████` 100% | 5,700,478 | 904 MiB |
| core | Programme | 13 | 13 | `██████████` 100% | 1,352,605 | 205 MiB |
| country | Programme | 5 | 5 | `██████████` 100% | 575,118 | 96 MiB |
| discovery | Programme | 8 | 9 | `█████████░` 89% | 42,452,568 | 1.6 GiB |
| discussion | Programme | 4 | 5 | `████████░░` 80% | 17,869,063 | 1.2 GiB |
| electronic | Programme | 17 | 18 | `█████████░` 94% | 14,412,154 | 1.5 GiB |
| hiphop | Programme | 7 | 10 | `███████░░░` 70% | 48,989,048 | 1.6 GiB |
| indie-artists | Programme | 5 | 5 | `██████████` 100% | 1,753,125 | 381 MiB |
| jazz | Programme | 6 | 6 | `██████████` 100% | 1,806,484 | 259 MiB |
| latin | Programme | 4 | 4 | `██████████` 100% | 386,573 | 66 MiB |
| metal | Programme | 6 | 6 | `██████████` 100% | 10,550,699 | 1.2 GiB |
| physical | Programme | 4 | 5 | `████████░░` 80% | 9,477,654 | 502 MiB |
| platform | Programme | 3 | 3 | `██████████` 100% | 712,241 | 106 MiB |
| pop | Programme | 3 | 4 | `████████░░` 75% | 13,111,162 | 838 MiB |
| producers | Programme | 5 | 5 | `██████████` 100% | 7,562,588 | 1.1 GiB |
| rock | Programme | 9 | 9 | `██████████` 100% | 9,151,968 | 1.1 GiB |
| sampling | Programme | 2 | 2 | `██████████` 100% | 31,270 | 7 MiB |
| streaming | Programme | 7 | 7 | `██████████` 100% | 5,019,048 | 659 MiB |

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
<summary><strong>audiophile</strong> — 3/4 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/audio` | 🟢 Complete | 474,399 | 2/2 | 81 MiB |
| `r/BudgetAudiophile` | 🟢 Complete | 1,884,342 | 2/2 | 283 MiB |
| `r/audiophile` | 🟢 Complete | 3,569,576 | 2/2 | 483 MiB |
| `r/headphones` | ⚪ Pending | 4,925,237 | 0/2 | — |

</details>

<details>
<summary><strong>awards-and-charts</strong> — 0/2 complete · candidate</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/grammys` | ⚪ Pending review | 51,816 | 0/2 | — |
| `r/billboard` | ⚪ Pending review | 2,532 | 0/2 | — |

</details>

<details>
<summary><strong>classical</strong> — 5/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/opera` | 🟢 Complete | 341,749 | 2/2 | 54 MiB |
| `r/composer` | 🟢 Complete | 393,049 | 2/2 | 74 MiB |
| `r/violinist` | 🟢 Complete | 725,771 | 2/2 | 119 MiB |
| `r/classicalmusic` | 🟢 Complete | 1,954,698 | 2/2 | 284 MiB |
| `r/piano` | 🟢 Complete | 2,285,211 | 2/2 | 373 MiB |

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
<summary><strong>country</strong> — 5/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/Americana` | 🟢 Complete | 14,392 | 2/2 | 4 MiB |
| `r/folk` | 🟢 Complete | 97,346 | 2/2 | 22 MiB |
| `r/CountryMusic` | 🟢 Complete | 106,174 | 2/2 | 19 MiB |
| `r/altcountry` | 🟢 Complete | 130,094 | 2/2 | 20 MiB |
| `r/Bluegrass` | 🟢 Complete | 227,112 | 2/2 | 31 MiB |

</details>

<details>
<summary><strong>discovery</strong> — 8/9 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/vintageobscura` | 🟢 Complete | 117,162 | 2/2 | 29 MiB |
| `r/ifyoulikeblank` | 🟢 Complete | 1,880,530 | 2/2 | 218 MiB |
| `r/listentothis` | 🟢 Complete | 3,302,579 | 2/2 | 494 MiB |
| `r/musicsuggestions` | 🟢 Complete | 5,816,228 | 2/2 | 569 MiB |
| `r/Music` | ⚪ Pending | 28,144,040 | 0/2 | — |
| `r/Albumoftheday` | 🟢 Complete | 2,390 | 2/2 | 710 KiB |
| `r/1001AlbumsGenerator` | 🟢 Complete | 129,266 | 2/2 | 18 MiB |
| `r/newmusic` | 🟢 Complete | 193,998 | 2/2 | 35 MiB |
| `r/MusicRecommendations` | 🟢 Complete | 2,866,375 | 2/2 | 278 MiB |

</details>

<details>
<summary><strong>discussion</strong> — 4/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/LetsTalkMusic` | 🟢 Complete | 1,180,999 | 2/2 | 207 MiB |
| `r/fantanoforever` | 🟢 Complete | 3,185,542 | 2/2 | 363 MiB |
| `r/indieheads` | 🟢 Complete | 4,466,705 | 2/2 | 544 MiB |
| `r/popheads` | ⚪ Pending | 7,569,395 | 0/2 | — |
| `r/Topster` | 🟢 Complete | 1,466,422 | 2/2 | 153 MiB |

</details>

<details>
<summary><strong>electronic</strong> — 17/18 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/TheOverload` | 🟢 Complete | 203,109 | 2/2 | 37 MiB |
| `r/vaporwave` | 🟢 Complete | 553,397 | 2/2 | 81 MiB |
| `r/electronicmusic` | 🟢 Complete | 1,682,465 | 2/2 | 220 MiB |
| `r/synthwave` | 🟢 Complete | 31,880 | 2/2 | 7 MiB |
| `r/housemusic` | 🟢 Complete | 70,102 | 2/2 | 13 MiB |
| `r/IDM` | 🟢 Complete | 125,870 | 2/2 | 22 MiB |
| `r/realdubstep` | 🟢 Complete | 289,732 | 2/2 | 41 MiB |
| `r/psytrance` | 🟢 Complete | 301,434 | 2/2 | 46 MiB |
| `r/ambientmusic` | 🟢 Complete | 331,158 | 2/2 | 54 MiB |
| `r/futurebeats` | 🟢 Complete | 351,807 | 2/2 | 58 MiB |
| `r/outrun` | 🟢 Complete | 485,435 | 2/2 | 65 MiB |
| `r/techno` | 🟢 Complete | 839,519 | 2/2 | 122 MiB |
| `r/dnb` | 🟢 Complete | 1,008,284 | 2/2 | 151 MiB |
| `r/edm` | 🟢 Complete | 2,240,987 | 2/2 | 290 MiB |
| `r/House` | 🟢 Complete | 368,008 | 2/2 | 63 MiB |
| `r/trance` | 🟢 Complete | 691,677 | 2/2 | 95 MiB |
| `r/modular` | 🟢 Complete | 845,133 | 2/2 | 127 MiB |
| `r/synthesizers` | ⚪ Pending | 3,992,157 | 1/2 | 48 MiB |

</details>

<details>
<summary><strong>hiphop</strong> — 7/10 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/Jcole` | 🟢 Complete | 800,328 | 2/2 | 90 MiB |
| `r/trap` | 🟢 Complete | 1,111,508 | 2/2 | 133 MiB |
| `r/hiphop101` | 🟢 Complete | 2,075,706 | 2/2 | 203 MiB |
| `r/WestSubEver` | 🟢 Complete | 2,495,359 | 2/2 | 198 MiB |
| `r/makinghiphop` | 🟢 Complete | 2,946,542 | 2/2 | 316 MiB |
| `r/rap` | 🟢 Complete | 3,180,780 | 2/2 | 331 MiB |
| `r/Drizzy` | 🟢 Complete | 3,341,307 | 2/2 | 329 MiB |
| `r/KendrickLamar` | ⚪ Pending | 4,179,841 | 0/2 | — |
| `r/Eminem` | ⚪ Pending | 5,327,799 | 0/2 | — |
| `r/hiphopheads` | ⚪ Pending | 23,529,878 | 0/2 | — |

</details>

<details>
<summary><strong>indie-artists</strong> — 5/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/ratemysong` | 🟢 Complete | 44,617 | 2/2 | 11 MiB |
| `r/BedroomBands` | 🟢 Complete | 105,406 | 2/2 | 15 MiB |
| `r/ThisIsOurMusic` | 🟢 Complete | 426,816 | 2/2 | 86 MiB |
| `r/PromoteYourMusic` | 🟢 Complete | 472,968 | 2/2 | 131 MiB |
| `r/shareyourmusic` | 🟢 Complete | 703,318 | 2/2 | 139 MiB |

</details>

<details>
<summary><strong>jazz</strong> — 6/6 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/smoothjazz` | 🟢 Complete | 4,436 | 2/2 | 1 MiB |
| `r/jazztheory` | 🟢 Complete | 28,381 | 2/2 | 5 MiB |
| `r/JazzFusion` | 🟢 Complete | 35,417 | 2/2 | 7 MiB |
| `r/JazzPiano` | 🟢 Complete | 58,497 | 2/2 | 11 MiB |
| `r/jazzguitar` | 🟢 Complete | 259,948 | 2/2 | 41 MiB |
| `r/Jazz` | 🟢 Complete | 1,419,805 | 2/2 | 194 MiB |

</details>

<details>
<summary><strong>latin</strong> — 4/4 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/latinmusic` | 🟢 Complete | 1,954 | 2/2 | 829 KiB |
| `r/Bachata` | 🟢 Complete | 87,195 | 2/2 | 17 MiB |
| `r/Salsa` | 🟢 Complete | 144,499 | 2/2 | 26 MiB |
| `r/Reggaeton` | 🟢 Complete | 152,925 | 2/2 | 23 MiB |

</details>

<details>
<summary><strong>metal</strong> — 6/6 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/BlackMetal` | 🟢 Complete | 549,730 | 2/2 | 75 MiB |
| `r/doommetal` | 🟢 Complete | 766,553 | 2/2 | 95 MiB |
| `r/progmetal` | 🟢 Complete | 1,244,067 | 2/2 | 149 MiB |
| `r/Deathcore` | 🟢 Complete | 1,327,134 | 2/2 | 147 MiB |
| `r/Metal` | 🟢 Complete | 2,913,815 | 2/2 | 345 MiB |
| `r/Metalcore` | 🟢 Complete | 3,749,400 | 2/2 | 414 MiB |

</details>

<details>
<summary><strong>physical</strong> — 4/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/recordstore` | 🟢 Complete | 18,003 | 2/2 | 3 MiB |
| `r/cassetteculture` | 🟢 Complete | 841,844 | 2/2 | 132 MiB |
| `r/turntables` | 🟢 Complete | 1,167,233 | 2/2 | 183 MiB |
| `r/Cd_collectors` | 🟢 Complete | 1,275,226 | 2/2 | 184 MiB |
| `r/vinyl` | ⚪ Pending | 6,175,348 | 0/2 | — |

</details>

<details>
<summary><strong>platform</strong> — 3/3 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/soundcloud` | 🟢 Complete | 597,578 | 2/2 | 80 MiB |
| `r/SoundCloudMusic` | 🟢 Complete | 25,524 | 2/2 | 7 MiB |
| `r/SoundCloudHipHop` | 🟢 Complete | 89,139 | 2/2 | 20 MiB |

</details>

<details>
<summary><strong>pop</strong> — 3/4 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/popmusic` | 🟢 Complete | 31,208 | 2/2 | 5 MiB |
| `r/kpophelp` | 🟢 Complete | 2,033,911 | 2/2 | 280 MiB |
| `r/kpopthoughts` | 🟢 Complete | 3,891,535 | 2/2 | 553 MiB |
| `r/kpop` | ⚪ Pending | 7,154,508 | 0/2 | — |

</details>

<details>
<summary><strong>producers</strong> — 5/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/Songwriting` | 🟢 Complete | 997,098 | 2/2 | 161 MiB |
| `r/musicproduction` | 🟢 Complete | 1,453,070 | 2/2 | 203 MiB |
| `r/bandmembers` | 🟢 Complete | 111,624 | 2/2 | 19 MiB |
| `r/edmproduction` | 🟢 Complete | 2,461,291 | 2/2 | 316 MiB |
| `r/audioengineering` | 🟢 Complete | 2,539,505 | 2/2 | 378 MiB |

</details>

<details>
<summary><strong>rock</strong> — 9/9 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/postrock` | 🟢 Complete | 312,483 | 2/2 | 43 MiB |
| `r/indie` | 🟢 Complete | 392,338 | 2/2 | 75 MiB |
| `r/rock` | 🟢 Complete | 418,951 | 2/2 | 63 MiB |
| `r/shoegaze` | 🟢 Complete | 530,013 | 2/2 | 72 MiB |
| `r/progrockmusic` | 🟢 Complete | 740,638 | 2/2 | 97 MiB |
| `r/grunge` | 🟢 Complete | 1,076,885 | 2/2 | 121 MiB |
| `r/Emo` | 🟢 Complete | 1,289,740 | 2/2 | 160 MiB |
| `r/ClassicRock` | 🟢 Complete | 1,364,503 | 2/2 | 149 MiB |
| `r/punk` | 🟢 Complete | 3,026,417 | 2/2 | 367 MiB |

</details>

<details>
<summary><strong>sampling</strong> — 2/2 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/sampling` | 🟢 Complete | 6,166 | 2/2 | 1 MiB |
| `r/Samplehunters` | 🟢 Complete | 25,104 | 2/2 | 6 MiB |

</details>

<details>
<summary><strong>streaming</strong> — 7/7 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/qobuz` | 🟢 Complete | 44,098 | 2/2 | 7 MiB |
| `r/plexamp` | 🟢 Complete | 73,025 | 2/2 | 10 MiB |
| `r/TIdaL` | 🟢 Complete | 263,672 | 2/2 | 37 MiB |
| `r/YoutubeMusic` | 🟢 Complete | 415,026 | 2/2 | 57 MiB |
| `r/lastfm` | 🟢 Complete | 976,292 | 2/2 | 127 MiB |
| `r/AppleMusic` | 🟢 Complete | 1,051,589 | 2/2 | 138 MiB |
| `r/spotify` | 🟢 Complete | 2,195,346 | 2/2 | 284 MiB |

</details>

---

🟢 present in both MongoDB collections · 🟠 fetching/loading · 🟡 one raw file present · ⚪ pending
