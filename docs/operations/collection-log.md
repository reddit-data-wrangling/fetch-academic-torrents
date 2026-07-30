# Data collection log

Source: Arctic Shift API (`arctic-shift.photon-reddit.com`) via
[`scripts/fetch_subreddit.py`](../../scripts/fetch_subreddit.py).
Output: zstd-compressed NDJSON in `data/raw/`, one file per
`(subreddit, kind)`.

This is an append-only historical record, not the current acquisition queue.
Current intent lives in each collection's `selection.md` and `targets.txt`;
machine-readable holdings live in `inventory.json`.

## 2026-05-10

| Subreddit     | Submissions |  Comments | Subm. size | Comm. size | Submissions edge | Comments edge |
| ------------- | ----------: | --------: | ---------: | ---------: | ---------------- | ------------- |
| wikipedia     |     116,628 | 1,061,855 |      27 MB |     123 MB | 2026-04-19       | 2026-04-08    |
| linux         |     294,236 | 5,354,162 |      66 MB |     649 MB | 2026-04-25       | 2026-05-10    |
| linusrants    |         210 |     1,595 |      48 KB |     205 KB | —                | 2021-10-22    |
| rust          |     137,847 | 1,580,400 |      48 MB |     241 MB | 2026-04-22       | 2026-04-09    |
| sampling      |       1,786 |     3,546 |     775 KB |     451 KB | 2024-05-03       | 2026-03-05    |
| Samplehunters |      13,809 |    11,030 |     4.4 MB |     1.1 MB | 2025-08-23       | 2026-03-30    |

Edges = last `created_utc` reached during paging (sidecar `.cursor` files). The Arctic Shift index normally lags real-time by a few weeks; gaps before today reflect that, not premature termination. Re-running the fetcher resumes from each cursor.

### Notes

- One bug fixed at the start: the API rejects `after=0` ("must be a valid
  date"), so [`scripts/fetch_subreddit.py`](../../scripts/fetch_subreddit.py)
  omits the parameter when the cursor is 0.
- One transient HTTP 422 hit during r/linux comments around timestamp 1328745842 (Feb 2012); the script's exponential-backoff retry recovered without intervention.

## 2026-05-17

Quality-assessment fetch of r/linusrants via
[`scripts/assess_subreddit.py`](../../scripts/assess_subreddit.py), which wraps
`fetch_subreddit.fetch_kind` and re-reads the `.zst` file to report counts,
time range, field coverage, deleted-body share, and suspicious monthly gaps.

| Subreddit  | Submissions | Comments | Subm. edge | Comm. edge |
| ---------- | ----------: | -------: | ---------- | ---------- |
| linusrants |         210 |    1,596 | 2026-04-26 | 2026-05-14 |

Resume from the 2026-05-10 cursors back-filled the Arctic Shift comment edge from 2021-10-22 → 2026-05-14 (+1 comment), confirming the lag-not-truncation hypothesis in the note above.

## 2026-07-26 — bulk torrent source withdrawn (no fetch)

u/Watchful1 took down their Academic Torrents uploads at Reddit's request ([announcement](https://www.reddit.com/r/pushshift/comments/1v50ved/upon_reddits_request_i_am_taking_down_my_academic/)). Verified the whole landscape directly:

- **Dead** (page 404, tracker scrape returns `d5:filesdee` = zero peers): the subreddit-partitioned dumps `3e3f64d…` (our old primary, 2005-06→2025-12), `1614740…` (→2024-12), `56aa49f…` (→2023-12); and the full-corpus dumps `30dee5f…` (2005-06→2025-06) and `9c263fc…` (2005-06→2023-12). The `.torrent` metadata for these still returns HTTP 200 and passes infohash verification — but there are no seeders, so `torrent_fetch.py` would hang in `aria2c` at 0%. `--dry-run` still looks healthy; do not trust it.
- **Alive** (still listed, healthy swarms): monthly full-corpus dumps — `bec5590…` 2025-06 (~13 seeders), `b6a7ccf…` 2025-07 (~17), `8412b89…` 2026-01 (~23). These are month-partitioned (all subreddits per month), not per-subreddit.
- **Alive**: Arctic Shift API — spot-checked `posts/search` + `comments/search` for r/wikipedia, both HTTP 200 with full records, sub-second. Now the primary path and the only source for pre-2025-06 per-subreddit history.

**Plan (to be run server-side, not from the dev machine):** Track A = Arctic Shift API for the target subreddit allowlist, full history, first (fragile source). Track B = download + seed the surviving monthly full-corpus torrents (2025-06→present, ~1 TB budget) as archive + backfill, then filter target subs out locally. `load_to_mongo.py` dedupes the two tracks by Reddit `id`. See the README's [source-availability snapshot](../../README.md#source-availability). No data fetched in this session.

### Arctic Shift quality findings (r/linusrants)

- **Submissions `selftext` is 90% scrubbed** ([deleted]/[removed]/empty) across 210 posts spanning 2014–2026 — text analysis on submission bodies is largely impossible for this sub. Titles/metadata are intact.
- **Comments are clean**: only 3.2% (51/1596) of `body` fields are deleted/removed.
- **No duplicate ids** in either kind after pagination + dedup.
- **Possible silent gaps in comments** at 2017-03, 2019-04, 2019-05 (1 comment each, vs. neighbouring months in the dozens) — worth manual spot-check before treating monthly time series as reliable.

## 2026-07-30 — music-market subreddit panel (Track A, in progress)

First real Track A run: full-history Arctic Shift fetch of subreddits dealing with the **music market** (business, economics, commerce, promotion of music), loaded into MongoDB — new target: db `reddit` on `mongodb://localhost:27019` (not the default 27017).

**Target selection.** A 5-agent panel (lenses: industry/business, streaming economics, artist monetization, music marketing, music commerce/collecting) plus a synthesizer produced 18 subreddits from 70 raw candidates; all 18 verified to exist via the Arctic Shift `subreddits/search` endpoint, which also supplies expected post/comment counts per sub. Core tier (13): musicmarketing, musicindustry, musicbusiness, MusicPromotion, DistroKidHelpDesk, musicpublishing, synclicensing, recordlabels, TouringMusicians, musiclaw, MusicDistribution, SellingBeats, UnitedMasters. Adjacent tier (5, market content substantial but not exclusive): WeAreTheMusicMakers, SpotifyPlaylists, BandCamp, truespotify, Ticketmaster. Expected grand total ≈ 1.21 M posts + 5.43 M comments; live per-sub status in the [music collection progress](../../collections/music/progress.md).

**Pipeline test** before deployment: bounded fetch of r/musicindustry (Jan 2024 only, 184 submissions / 867 comments) into a scratch dir — deliberately not `data/raw/`, so the partial-range sidecar `.cursor` couldn't later masquerade as full-history progress — then `smoke_load_to_mongo.py` decode check and a real `load_to_mongo.py` run against :27019. Indexes (`id` unique, `(subreddit, created_utc)`) created correctly; upsert idempotency means the full fetch simply extends these rows.

**Deployment**: sequential (one API rate-limit budget), smallest subs first, each sub loaded into Mongo immediately after its fetch; failures logged and skipped, resumable via cursors. Observed throughput ~600–1,100 items/s. **Phase 1 completed 2026-07-30 00:40 UTC** (75 min wall-clock, zero failures, 18/18 subs):

| Subreddit           | Submissions |  Comments | Subm. size | Comm. size | First   | Edge       |
| ------------------- | ----------: | --------: | ---------: | ---------: | ------- | ---------- |
| musiclaw            |          92 |        69 |      40 KB |      17 KB | 2015-02 | 2026-07-20 |
| SellingBeats        |          57 |        38 |      20 KB |       6 KB | 2019-09 | 2025-10-15 |
| musicpublishing     |         331 |       628 |     123 KB |     107 KB | 2015-04 | 2026-07-24 |
| synclicensing       |         569 |     3,997 |     238 KB |     600 KB | 2021-08 | 2026-07-28 |
| recordlabels        |       1,638 |     7,227 |     697 KB |     900 KB | 2012-07 | 2026-07-29 |
| MusicDistribution   |       1,976 |    14,504 |     724 KB |     1.9 MB | 2017-02 | 2026-07-29 |
| UnitedMasters       |       3,714 |    12,944 |     1.1 MB |     1.0 MB | 2019-08 | 2026-07-29 |
| TouringMusicians    |       4,952 |    32,624 |     1.7 MB |     4.7 MB | 2010-12 | 2026-07-29 |
| Ticketmaster        |      23,327 |    27,774 |     3.3 MB |     3.3 MB | 2010-08 | 2026-07-29 |
| musicbusiness       |      11,467 |    40,714 |     3.9 MB |     6.2 MB | 2011-10 | 2026-07-29 |
| DistroKidHelpDesk   |      15,761 |    63,174 |     3.5 MB |     7.1 MB | 2020-05 | 2026-07-29 |
| musicindustry       |      16,787 |   121,888 |     6.0 MB |    18.2 MB | 2011-01 | 2026-07-29 |
| BandCamp            |      43,206 |   149,679 |    17.7 MB |    16.7 MB | 2011-09 | 2026-07-29 |
| musicmarketing      |      27,982 |   213,696 |     9.6 MB |    28.7 MB | 2012-10 | 2026-07-29 |
| truespotify         |      59,446 |   422,134 |    21.3 MB |    45.6 MB | 2015-07 | 2026-07-29 |
| MusicPromotion      |     178,738 |   581,746 |    62.9 MB |    45.0 MB | 2011-05 | 2026-07-29 |
| SpotifyPlaylists    |     423,157 |   403,410 |   133.3 MB |    44.7 MB | 2011-10 | 2026-07-30 |
| WeAreTheMusicMakers |     403,665 | 3,341,329 |   102.0 MB |   416.8 MB | 2008-09 | 2026-07-30 |

**Phase-1 totals: 1,216,865 submissions + 5,437,575 comments** (~1.06 GB compressed raw). First/Edge = min/max `created_utc` in Mongo across both kinds. Loaded counts run a few % above the Arctic Shift metadata "expected" numbers — the endpoint's `num_posts`/`num_comments` are periodic snapshots that lag the live index, not evidence of duplication (`id` is unique-indexed). Phase 2 (below) started automatically on phase-1 exit.

## 2026-07-30 — destination map: where each subreddit's data lives

Audited every storage endpoint (verified 2026-07-30 00:38 BST). Three destinations exist; `data/` is gitignored, so raw `.zst` files on disk are the *only* copy of anything not loaded into Mongo.

| Endpoint | Location | Physical disk |
| --- | --- | --- |
| `data/raw/` (this repo) | `/home/simone/githubRepos/fetch-academic-torrents/data/raw/` | root NVMe `/dev/nvme2n1p3` (SK hynix PC811 1 TB, mounted `/`; 555 GB free) |
| MongoDB `:27017`, db `reddit` | dbPath `/media/simone/ssd2/oss/` (config `~/mongoConfigs/_1.conf`) | Samsung 870 QVO 8 TB SATA SSD (`/media/simone/ssd2`) |
| MongoDB `:27019`, db `reddit` | dbPath `/media/simone/sata1/culturalMarkets/` (config `~/mongoConfigs/_3.conf`) | SABRENT 1.8 TB (`/media/simone/sata1`) |

A third instance (`:27018`, dbPath `/media/simone/sata3/orgAndTech/`, config `_2.conf`) is currently stopped and holds no reddit data (checked its WiredTiger catalog: formula1, stackoverflow, ideaManagement, …).

### 2026-05-10 batch — raw dumps gone; only linux and rust survive (in Mongo :27017)

The May `.zst` files are **no longer in `data/raw/`** and were not found on any of the seven mounted drives or in any Mongo instance (running or stopped). Consequences per sub:

| Subreddit | Raw .zst | MongoDB | Docs in Mongo (S / C) | Status |
| --- | --- | --- | ---: | --- |
| wikipedia | yes (refetched) | `:27017` db `reddit` | 119,278 / 1,097,766 | recovered — full refetch 2026-07-30, see entry below |
| linux | gone | `:27017` db `reddit` | 295,825 / 5,378,339 | safe; counts exceed the May log → later resumed fetches |
| linusrants | yes (refetched) | `:27017` db `reddit` | 212 / 1,638 | recovered — full refetch 2026-07-30, see entry below |
| rust | gone | `:27017` db `reddit` | 139,590 / 1,593,774 | safe; ditto |
| sampling | yes (refetched) | `:27019` db `reddit` | 1,992 / 4,288 | recovered — refetched 2026-07-30 with the music panel |
| Samplehunters | yes (refetched) | `:27019` db `reddit` | 14,096 / 11,151 | recovered — refetched 2026-07-30 with the music panel |

The `:27017` `reddit` db also holds linuxquestions, linux4noobs, osdev, kernel — fetched for the OSS project, never tracked in this log.

### 2026-07-30 music-market panel — uniform destination

Every sub in this panel follows the same path: raw `.zst` (+ resume `.cursor`) in `data/raw/` on the root NVMe, then loaded into **MongoDB `:27019`**, db `reddit`, collections `submissions`/`comments` on the SABRENT 1.8 TB. Per-sub state as of 2026-07-30 00:38 BST (run still in progress; 12/18 loaded):

| Subreddit | Raw .zst in `data/raw/` | Mongo :27019 (S / C) |
| --- | --- | ---: |
| musiclaw | yes | 92 / 69 |
| SellingBeats | yes | 57 / 38 |
| musicpublishing | yes | 331 / 628 |
| synclicensing | yes | 569 / 3,997 |
| recordlabels | yes | 1,638 / 7,227 |
| MusicDistribution | yes | 1,976 / 14,504 |
| UnitedMasters | yes | 3,714 / 12,944 |
| TouringMusicians | yes | 4,952 / 32,624 |
| Ticketmaster | yes | 23,327 / 27,774 |
| musicbusiness | yes | 11,467 / 40,714 |
| DistroKidHelpDesk | yes | 15,761 / 63,174 |
| musicindustry | yes | 16,787 / 121,888 |
| BandCamp | fetching now (PID observed 00:38) | 0 / 0 |
| musicmarketing | not yet | 0 / 0 |
| truespotify | not yet | 0 / 0 |
| MusicPromotion | not yet | 0 / 0 |
| SpotifyPlaylists | not yet | 0 / 0 |
| WeAreTheMusicMakers | not yet | 0 / 0 |

The musicindustry counts include the 184/867 rows from the Jan-2024 pipeline test — the full-history fetch upserted over them, as designed.

**Takeaway**: once a sub is confirmed in Mongo, the `.zst` in `data/raw/` is the only *raw* copy and the Mongo rows the only *loaded* copy — neither is backed up elsewhere. The May batch shows what happens when `data/raw/` is cleaned before loading: four subs needed refetching (all four recovered later the same day — see the May-batch table above and the recovery entry below).

**Phase 2 (user-added, same day).** 14 further music subreddits added beyond the market panel — discovery/sharing (Music, listentothis, vintageobscura, musicsuggestions, ifyoulikeblank), discussion/analysis (LetsTalkMusic, popheads, indieheads, fantanoforever), electronic (electronicmusic, TheOverload, vaporwave), musicians/producers (musicproduction, Songwriting; WeAreTheMusicMakers was already in the panel). All 14 verified in Arctic Shift; combined expected volume ≈ 8.0 M posts + 52.5 M comments — dominated by r/Music alone (4.46 M + 23.7 M, ~28 M items, above the fetcher's then-documented "low millions per sub" comfort zone, but the API was the only implemented per-subreddit source after the torrent withdrawal). Queued as a second sequential job that starts automatically when phase 1 exits, again smallest-first with r/Music last. Disk headroom checked: 555 GB free. New expected grand total across both phases ≈ 9.25 M posts + 57.9 M comments.

**Phase 3 (user-added, same day).** 11 electronic-genre subreddits: techno, housemusic, edm, realdubstep, synthwave, outrun, ambientmusic, IDM, dnb, psytrance, futurebeats (the user's list also named electronicmusic, TheOverload, vaporwave — already queued in phase 2). All verified in Arctic Shift; expected ≈ 1.24 M posts + 4.84 M comments, largest being EDM (2.2 M items), DnB (1.0 M), Techno (0.84 M). Queued as a third sequential job chained behind phase 2. Expected grand total across all three phases ≈ 10.5 M posts + 62.8 M comments (~43 subreddits).

**r/sampling + r/Samplehunters (user-added, same day).** Both were fetched on 2026-05-10, but those `.zst` files are not in `data/raw/` on this machine, so they were re-fetched from scratch — small enough (~31 k items, <1 min) to run inline alongside phase 1 rather than queueing. Fresh full history: sampling 1,992 submissions / 4,288 comments (May: 1,786 / 3,546); Samplehunters 14,096 / 11,151 (May: 13,809 / 11,030) — the growth over the May numbers is new activity plus Arctic Shift index catch-up. Loaded into :27019 like everything else. Running total: 45 subreddits targeted.

**Phase 4 (user-added, same day).** r/soundcloud — verified in Arctic Shift: 179,895 posts + 417,683 comments since 2010-07. Queued as a fourth sequential job chained behind phase 3. Running total: 46 subreddits targeted.

**Collection STOPPED by user 2026-07-30 15:45 UTC.** Both running queues killed on request: the original 48-sub queue (was loading musicsuggestions — that Mongo-only load was allowed to drain since its fetch had completed and it uses no API) and session e0c58541's phase-5 taxonomy queue (killed mid-fetch). State at stop: **36/130 subs fully loaded, ~28.2 M items** in :27019 (see the [music collection progress](../../collections/music/progress.md)). ⚠️ **Before any resume, delete these mid-write files** — a process killed mid-zstd-frame leaves a truncated frame that corrupts the file on append (this exact failure hit fantanoforever_comments earlier today and cost a full refetch): `latinmusic_{submissions,comments}.zst` + cursors, `Americana_{submissions,comments}.zst` + cursors. Everything else in `data/raw/` closed cleanly (a successful Mongo load = a full decode). Remaining unfetched: popheads, Music, the 11 phase-3 electronic subs, soundcloud, and ~78 phase-5 taxonomy subs.

**r/SoundCloudMusic + r/SoundCloudHipHop (user-added, same day).** Both small, fetched inline like the sampling subs: SoundCloudMusic 16,829 submissions / 9,044 comments (since 2016-01); SoundCloudHipHop 49,970 / 39,340 (since 2017-04). Loaded into :27019. Running total: 48 subreddits targeted.

## 2026-07-30 — May-batch recovery: r/wikipedia + r/linusrants → :27017

Full-history Arctic Shift refetch of the two remaining lost May-batch subs (raw dumps had been deleted before loading; see destination map above), run 23:46–00:14 UTC concurrently with the music-panel job (both fetchers honor the shared rate-limit headers; throughput held ~1,100 items/s). Raw `.zst` in `data/raw/`, then loaded into MongoDB **`:27017`** db `reddit` (dbPath `/media/simone/ssd2/oss/`), joining linux and rust. Mongo counts verified equal to fetched counts.

| Subreddit | Submissions | Comments | Subm. size | Comm. size | First | Edge |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| wikipedia | 119,278 | 1,097,766 | 29 MB | 129 MB | 2008-01 | 2026-07-30 |
| linusrants | 212 | 1,638 | 49 KB | 212 KB | 2014-07 | 2026-07-17 |

Growth over the May-2026 numbers (wikipedia +2,650 S / +35,911 C; linusrants +2 S / +42 C) is new activity plus Arctic Shift index catch-up — the fresh fetch also confirms the old edges were index lag, not truncation. Note the destination split: these two live on **:27017** (OSS instance) alongside linux/rust, while the same-day sampling/Samplehunters refetch went to **:27019** with the music panel.

**Phase 5 (user-added, 2026-07-30 ~17:00 UTC).** Full music-market taxonomy expansion: 82 further subreddits across streaming platforms (spotify, AppleMusic, TIdaL, qobuz, plexamp, YoutubeMusic, lastfm), audiophile (audiophile, headphones, BudgetAudiophile, audio), physical media (vinyl, turntables, cassetteculture, Cd_collectors, recordstore), jazz (Jazz, jazzguitar, JazzPiano, jazztheory, JazzFusion, smoothjazz), hip-hop (hiphopheads, rap, makinghiphop, trap, hiphop101, WestSubEver, KendrickLamar, Jcole, Drizzy, Eminem), rock/indie (indie, rock, progrockmusic, postrock, punk, grunge, Emo, shoegaze, ClassicRock), electronic gaps (House, trance, synthesizers, modular), pop/kpop (popmusic, kpop, kpopthoughts, kpophelp), classical (classicalmusic, composer, piano, violinist, opera), country/folk (CountryMusic, Bluegrass, folk, Americana, altcountry), latin (Reggaeton, latinmusic, Salsa, Bachata), metal (Metal, Metalcore, Deathcore, BlackMetal, doommetal, progmetal), discovery (MusicRecommendations, Topster, newmusic, Albumoftheday, 1001AlbumsGenerator), producers (audioengineering, edmproduction, bandmembers), and independent artists (ThisIsOurMusic, shareyourmusic, ratemysong, PromoteYourMusic, BedroomBands). Duplicates against the existing 48-row panel were dropped (e.g. Music, listentothis, WeAreTheMusicMakers, edm, techno, ambientmusic, dnb, popheads, indieheads, Songwriting, BandCamp, vinyl-adjacent subs already queued); r/BlueNote was requested but is not in Arctic Shift's index and was skipped. All 82 verified via `subreddits/search` metadata; combined expected ≈ 12.34 M posts + 120.7 M comments (largest: hiphopheads 23.5 M items, kpop 7.2 M, vinyl 6.2 M, Eminem 5.3 M, headphones 4.9 M). Disk headroom at queue time: 554 GB local (raw), 470 GB on sata1 (:27019). Queued as a fifth sequential job (`deploy_music_p5.sh`, detached) chained behind the running resume queue, smallest-first with hiphopheads last. Expected grand total across all phases ≈ 23.1 M posts + 184.0 M comments (130 subreddits targeted). Per-sub expected counts are in rows 49–130 of the [music collection progress](../../collections/music/progress.md).
