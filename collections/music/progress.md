# Music-market subreddit collection — progress

**Collection state: ACTIVE.** The project owner resumed the existing
130-subreddit programme on 2026-07-31. The remaining queue runs smallest-first
in tmux session `reddit_music_resume`; output is written to
`data/logs/music-resume.log`.

The table below is the last hand-maintained deployment snapshot. For current
Mongo-backed completion state, open [`dashboard.md`](dashboard.md) in VS Code
Markdown Preview; the resume job refreshes it after every successful load.

Last refreshed: 2026-07-30 15:43 UTC. Source: Arctic Shift API via `scripts/fetch_subreddit.py`;
target: MongoDB `reddit` db at `mongodb://localhost:27019` (collections `submissions`, `comments`).
Phase 1 (rows 1-18): music-market panel selected by a 5-lens agent panel
(industry, streaming economics, artist monetization, marketing, music commerce)
+ synthesizer. Phase 2 (rows 19-32): user-added discovery / discussion /
electronic / producer communities. Phase 3 (rows 33-43): user-added
electronic-genre communities. Rows 44-45 (sampling subs) were fetched
inline; row 46 (r/soundcloud) is phase 4. Phase 5 (rows 49-130):
user-added full music-market taxonomy — streaming platforms, audiophile /
physical media, jazz, hip-hop, rock/indie, remaining electronic, pop/kpop,
classical, country/folk, latin, metal, discovery, and independent-artist
communities (r/BlueNote requested but not indexed by Arctic Shift; skipped;
names use Arctic Shift canonical casing). Each phase starts automatically
when the previous one finishes and deploys smallest-first (phase-5 queue:
`deploy_music_p5.sh`, detached, session e0c58541's scratchpad).

| # | Subreddit | Tier | Status | Expected posts | Expected comments | Loaded posts | Loaded comments |
|--:|-----------|------|--------|---------------:|------------------:|-------------:|----------------:|
| 1 | r/musiclaw | core | ✅ done | 92 | 69 | 92 | 69 |
| 2 | r/SellingBeats | core | ✅ done | 57 | 38 | 57 | 38 |
| 3 | r/musicpublishing | core | ✅ done | 328 | 628 | 331 | 628 |
| 4 | r/synclicensing | core | ✅ done | 548 | 3,991 | 569 | 3,997 |
| 5 | r/recordlabels | core | ✅ done | 1,571 | 7,188 | 1,638 | 7,227 |
| 6 | r/MusicDistribution | core | ✅ done | 1,799 | 14,409 | 1,976 | 14,504 |
| 7 | r/UnitedMasters | core | ✅ done | 3,682 | 12,942 | 3,714 | 12,944 |
| 8 | r/TouringMusicians | core | ✅ done | 4,859 | 32,554 | 4,952 | 32,624 |
| 9 | r/Ticketmaster | adjacent | ✅ done | 22,517 | 27,552 | 23,327 | 27,774 |
| 10 | r/musicbusiness | core | ✅ done | 11,324 | 40,621 | 11,467 | 40,714 |
| 11 | r/DistroKidHelpDesk | core | ✅ done | 15,573 | 63,161 | 15,761 | 63,174 |
| 12 | r/musicindustry | core | ✅ done | 16,513 | 121,700 | 16,787 | 121,888 |
| 13 | r/BandCamp | adjacent | ✅ done | 42,902 | 149,521 | 43,206 | 149,679 |
| 14 | r/musicmarketing | core | ✅ done | 27,414 | 213,711 | 27,982 | 213,696 |
| 15 | r/truespotify | adjacent | ✅ done | 58,049 | 420,660 | 59,446 | 422,134 |
| 16 | r/MusicPromotion | core | ✅ done | 177,232 | 580,601 | 178,738 | 581,746 |
| 17 | r/SpotifyPlaylists | adjacent | ✅ done | 421,546 | 403,030 | 423,157 | 403,410 |
| 18 | r/WeAreTheMusicMakers | adjacent | ✅ done | 403,127 | 3,341,227 | 403,665 | 3,341,329 |
| 19 | r/vintageobscura | discovery | ✅ done | 54,752 | 62,410 | 54,861 | 62,403 |
| 20 | r/TheOverload | electronic | ✅ done | 48,917 | 154,192 | 49,623 | 154,710 |
| 21 | r/vaporwave | electronic | ✅ done | 123,359 | 430,038 | 123,765 | 430,262 |
| 22 | r/Songwriting | producers | ✅ done | 122,396 | 874,702 | 124,046 | 875,747 |
| 23 | r/LetsTalkMusic | discussion | ✅ done | 61,416 | 1,119,583 | 61,903 | 1,120,385 |
| 24 | r/musicproduction | producers | ✅ done | 224,525 | 1,228,545 | 226,151 | 1,229,349 |
| 25 | r/electronicmusic | electronic | ✅ done | 387,662 | 1,294,803 | 388,429 | 1,295,078 |
| 26 | r/ifyoulikeblank | discovery | ✅ done | 260,186 | 1,620,344 | 260,567 | 1,620,568 |
| 27 | r/fantanoforever | discussion | ✅ done | 104,976 | 3,080,566 | 106,644 | 3,089,284 |
| 28 | r/listentothis | discovery | ✅ done | 1,332,307 | 1,970,272 | 1,333,477 | 1,970,239 |
| 29 | r/indieheads | discussion | ✅ done | 346,801 | 4,119,904 | 349,033 | 4,121,204 |
| 30 | r/musicsuggestions | discovery | ⏳ loading | 215,650 | 5,600,578 | 220,255 | 2,115,482 |
| 31 | r/popheads | discussion | · pending | 298,447 | 7,270,948 | 0 | 0 |
| 32 | r/Music | discovery | · pending | 4,461,760 | 23,682,280 | 0 | 0 |
| 33 | r/synthwave | electronic | · pending | 24,223 | 7,657 | 0 | 0 |
| 34 | r/housemusic | electronic | · pending | 27,650 | 42,452 | 0 | 0 |
| 35 | r/IDM | electronic | · pending | 36,418 | 89,452 | 0 | 0 |
| 36 | r/realdubstep | electronic | · pending | 66,159 | 223,573 | 0 | 0 |
| 37 | r/psytrance | electronic | · pending | 48,477 | 252,957 | 0 | 0 |
| 38 | r/ambientmusic | electronic | · pending | 82,574 | 248,584 | 0 | 0 |
| 39 | r/futurebeats | electronic | · pending | 150,700 | 201,107 | 0 | 0 |
| 40 | r/outrun | electronic | · pending | 92,309 | 393,126 | 0 | 0 |
| 41 | r/techno | electronic | · pending | 179,924 | 659,595 | 0 | 0 |
| 42 | r/dnb | electronic | · pending | 191,743 | 816,541 | 0 | 0 |
| 43 | r/edm | electronic | · pending | 338,344 | 1,902,643 | 0 | 0 |
| 44 | r/sampling | sampling | ✅ done | 1,899 | 4,267 | 1,992 | 4,288 |
| 45 | r/Samplehunters | sampling | ✅ done | 13,945 | 11,159 | 14,096 | 11,151 |
| 46 | r/soundcloud | platform | · pending | 179,895 | 417,683 | 0 | 0 |
| 47 | r/SoundCloudMusic | platform | ✅ done | 16,484 | 9,040 | 16,829 | 9,044 |
| 48 | r/SoundCloudHipHop | platform | ✅ done | 49,802 | 39,337 | 49,970 | 39,340 |
| 49 | r/latinmusic | latin | ✅ done | 1,740 | 214 | 1,774 | 214 |
| 50 | r/Albumoftheday | discovery | ✅ done | 901 | 1,489 | 901 | 1,489 |
| 51 | r/smoothjazz | jazz | ✅ done | 3,221 | 1,215 | 3,273 | 1,221 |
| 52 | r/Americana | country | ⏳ fetching | 6,763 | 7,629 | 0 | 0 |
| 53 | r/recordstore | physical | · pending | 3,025 | 14,978 | 0 | 0 |
| 54 | r/jazztheory | jazz | · pending | 5,781 | 22,600 | 0 | 0 |
| 55 | r/popmusic | pop | · pending | 5,399 | 25,809 | 0 | 0 |
| 56 | r/JazzFusion | jazz | · pending | 9,570 | 25,847 | 0 | 0 |
| 57 | r/qobuz | streaming | · pending | 4,451 | 39,647 | 0 | 0 |
| 58 | r/ratemysong | indie-artists | · pending | 27,176 | 17,441 | 0 | 0 |
| 59 | r/JazzPiano | jazz | · pending | 9,777 | 48,720 | 0 | 0 |
| 60 | r/plexamp | streaming | · pending | 6,347 | 66,678 | 0 | 0 |
| 61 | r/Bachata | latin | · pending | 7,599 | 79,596 | 0 | 0 |
| 62 | r/folk | country | · pending | 42,697 | 54,649 | 0 | 0 |
| 63 | r/BedroomBands | indie-artists | · pending | 29,692 | 75,714 | 0 | 0 |
| 64 | r/CountryMusic | country | · pending | 29,326 | 76,848 | 0 | 0 |
| 65 | r/bandmembers | producers | · pending | 9,312 | 102,312 | 0 | 0 |
| 66 | r/1001AlbumsGenerator | discovery | · pending | 7,553 | 121,713 | 0 | 0 |
| 67 | r/altcountry | country | · pending | 23,006 | 107,088 | 0 | 0 |
| 68 | r/Salsa | latin | · pending | 12,129 | 132,370 | 0 | 0 |
| 69 | r/Reggaeton | latin | · pending | 25,177 | 127,748 | 0 | 0 |
| 70 | r/newmusic | discovery | · pending | 94,409 | 99,589 | 0 | 0 |
| 71 | r/Bluegrass | country | · pending | 27,748 | 199,364 | 0 | 0 |
| 72 | r/jazzguitar | jazz | · pending | 34,822 | 225,126 | 0 | 0 |
| 73 | r/TIdaL | streaming | · pending | 23,895 | 239,777 | 0 | 0 |
| 74 | r/postrock | rock | · pending | 58,050 | 254,433 | 0 | 0 |
| 75 | r/opera | classical | · pending | 31,407 | 310,342 | 0 | 0 |
| 76 | r/House | electronic | · pending | 138,957 | 229,051 | 0 | 0 |
| 77 | r/indie | rock | · pending | 144,985 | 247,353 | 0 | 0 |
| 78 | r/composer | classical | · pending | 54,795 | 338,254 | 0 | 0 |
| 79 | r/YoutubeMusic | streaming | · pending | 51,863 | 363,163 | 0 | 0 |
| 80 | r/rock | rock | · pending | 91,655 | 327,296 | 0 | 0 |
| 81 | r/ThisIsOurMusic | indie-artists | · pending | 223,547 | 203,269 | 0 | 0 |
| 82 | r/PromoteYourMusic | indie-artists | · pending | 309,494 | 163,474 | 0 | 0 |
| 83 | r/audio | audiophile | · pending | 95,813 | 378,586 | 0 | 0 |
| 84 | r/shoegaze | rock | · pending | 79,543 | 450,470 | 0 | 0 |
| 85 | r/BlackMetal | metal | · pending | 104,629 | 445,101 | 0 | 0 |
| 86 | r/trance | electronic | · pending | 145,144 | 546,533 | 0 | 0 |
| 87 | r/shareyourmusic | indie-artists | · pending | 328,187 | 375,131 | 0 | 0 |
| 88 | r/violinist | classical | · pending | 66,287 | 659,484 | 0 | 0 |
| 89 | r/progrockmusic | rock | · pending | 77,477 | 663,161 | 0 | 0 |
| 90 | r/doommetal | metal | · pending | 73,439 | 693,114 | 0 | 0 |
| 91 | r/Jcole | hiphop | · pending | 49,622 | 750,706 | 0 | 0 |
| 92 | r/cassetteculture | physical | · pending | 110,559 | 731,285 | 0 | 0 |
| 93 | r/modular | electronic | · pending | 68,813 | 776,320 | 0 | 0 |
| 94 | r/lastfm | streaming | · pending | 88,347 | 887,945 | 0 | 0 |
| 95 | r/AppleMusic | streaming | · pending | 114,200 | 937,389 | 0 | 0 |
| 96 | r/grunge | rock | · pending | 58,768 | 1,018,117 | 0 | 0 |
| 97 | r/trap | hiphop | · pending | 210,983 | 900,525 | 0 | 0 |
| 98 | r/turntables | physical | · pending | 97,941 | 1,069,292 | 0 | 0 |
| 99 | r/progmetal | metal | · pending | 112,313 | 1,131,754 | 0 | 0 |
| 100 | r/Cd_collectors | physical | · pending | 107,170 | 1,168,056 | 0 | 0 |
| 101 | r/Emo | rock | · pending | 147,023 | 1,142,717 | 0 | 0 |
| 102 | r/Deathcore | metal | · pending | 104,618 | 1,222,516 | 0 | 0 |
| 103 | r/ClassicRock | rock | · pending | 94,210 | 1,270,293 | 0 | 0 |
| 104 | r/Jazz | jazz | · pending | 177,144 | 1,242,661 | 0 | 0 |
| 105 | r/Topster | discussion | · pending | 91,010 | 1,375,412 | 0 | 0 |
| 106 | r/BudgetAudiophile | audiophile | · pending | 186,620 | 1,697,722 | 0 | 0 |
| 107 | r/classicalmusic | classical | · pending | 216,567 | 1,738,131 | 0 | 0 |
| 108 | r/kpophelp | pop | · pending | 157,441 | 1,876,470 | 0 | 0 |
| 109 | r/hiphop101 | hiphop | · pending | 58,017 | 2,017,689 | 0 | 0 |
| 110 | r/spotify | streaming | · pending | 507,973 | 1,687,373 | 0 | 0 |
| 111 | r/piano | classical | · pending | 295,072 | 1,990,139 | 0 | 0 |
| 112 | r/edmproduction | producers | · pending | 202,685 | 2,258,606 | 0 | 0 |
| 113 | r/WestSubEver | hiphop | · pending | 135,795 | 2,359,564 | 0 | 0 |
| 114 | r/audioengineering | producers | · pending | 198,515 | 2,340,990 | 0 | 0 |
| 115 | r/MusicRecommendations | discovery | · pending | 65,239 | 2,801,136 | 0 | 0 |
| 116 | r/Metal | metal | · pending | 454,195 | 2,459,620 | 0 | 0 |
| 117 | r/makinghiphop | hiphop | · pending | 187,719 | 2,758,823 | 0 | 0 |
| 118 | r/punk | rock | · pending | 251,213 | 2,775,204 | 0 | 0 |
| 119 | r/rap | hiphop | · pending | 316,903 | 2,863,877 | 0 | 0 |
| 120 | r/Drizzy | hiphop | · pending | 235,811 | 3,105,496 | 0 | 0 |
| 121 | r/audiophile | audiophile | · pending | 271,218 | 3,298,358 | 0 | 0 |
| 122 | r/Metalcore | metal | · pending | 273,572 | 3,475,828 | 0 | 0 |
| 123 | r/kpopthoughts | pop | · pending | 130,342 | 3,761,193 | 0 | 0 |
| 124 | r/synthesizers | electronic | · pending | 267,244 | 3,724,913 | 0 | 0 |
| 125 | r/KendrickLamar | hiphop | · pending | 248,784 | 3,931,057 | 0 | 0 |
| 126 | r/headphones | audiophile | · pending | 416,231 | 4,509,006 | 0 | 0 |
| 127 | r/Eminem | hiphop | · pending | 351,082 | 4,976,717 | 0 | 0 |
| 128 | r/vinyl | physical | · pending | 490,077 | 5,685,271 | 0 | 0 |
| 129 | r/kpop | pop | · pending | 649,904 | 6,504,604 | 0 | 0 |
| 130 | r/hiphopheads | hiphop | · pending | 1,608,534 | 21,921,344 | 0 | 0 |

**36/130 subreddits complete** — 4,604,454 posts + 23,589,033 comments loaded so far (expected total ≈ 23,089,095 posts + 183,968,436 comments).

Expected counts come from Arctic Shift `subreddits/search` metadata (2026-07-30);
loaded counts are live Mongo aggregations. Raw `.zst` files land in `data/raw/`.
