# Open-source software subreddit collection dashboard

_Refreshed 2026-08-07 13:45 UTC from the OSS worker state, catalogue, `targets.txt`, MongoDB evidence, and `data/raw/`._

> Open with **Markdown: Open Preview** (`Ctrl+Shift+V` / `Cmd+Shift+V`). The tmux worker refreshes this file at each acquisition stage.

## Status

| Panel N | Available in MongoDB | Active/staged | Partial raw | Remaining | Expected records | Raw data | Workflow |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 120 | 20 | 1 | 0 | 100 | 66,377,368 | 1.8 GiB | `active` |

**MongoDB availability:** `████░░░░░░░░░░░░░░░░░░░░` 17%

- worker activity: `fetching r/opentofu`
- worker state updated: `2026-08-07T08:29:17.815740+00:00`
- tmux session: `reddit_oss_collection`
- runtime log: `data/logs/oss-collection.log`
- destination: MongoDB `localhost:27017`, database `reddit`
- queue policy: one low-priority worker, smallest expected capture first
- API priority: yields while the comics/movies worker is fetching

## Next in queue

| # | Subreddit | Category | Expected records | Existing raw |
| ---: | --- | --- | ---: | ---: |
| 1 | `r/opentofu` | Infrastructure, automation, and observability | 254 | 0/2 files |
| 2 | `r/forgejo` | Self-hosted applications and services | 536 | 0/2 files |
| 3 | `r/Gitea` | Self-hosted applications and services | 1,746 | 0/2 files |
| 4 | `r/Vllm` | Open machine learning and scientific computing | 2,225 | 0/2 files |
| 5 | `r/OpenTelemetry` | Infrastructure, automation, and observability | 2,327 | 0/2 files |
| 6 | `r/Ardour` | Graphics, video, and audio | 2,391 | 0/2 files |
| 7 | `r/Clickhouse` | Databases and data systems | 3,032 | 0/2 files |
| 8 | `r/JAX` | Open machine learning and scientific computing | 3,750 | 0/2 files |
| 9 | `r/chocolatey` | Package managers and reproducible systems | 4,521 | 0/2 files |
| 10 | `r/vaultwarden` | Self-hosted applications and services | 5,882 | 0/2 files |
| 11 | `r/huggingface` | Open machine learning and scientific computing | 7,939 | 0/2 files |
| 12 | `r/Paperlessngx` | Self-hosted applications and services | 8,405 | 0/2 files |
| 13 | `r/OnlyOffice` | Office, notes, and productivity | 8,608 | 0/2 files |
| 14 | `r/redis` | Databases and data systems | 8,972 | 0/2 files |
| 15 | `r/sqlite` | Databases and data systems | 10,814 | 0/2 files |

## Progress by category

| Category | Available | Tracked | Progress | Expected records | Raw data |
| --- | ---: | ---: | --- | ---: | ---: |
| Adjacent package-manager comparator | 0 | 1 | `░░░░░░░░░░` 0% | 57,472 | 0 B |
| Browsers and privacy tools | 0 | 7 | `░░░░░░░░░░` 0% | 1,409,052 | 0 B |
| Contribution, collaboration, governance, and documentation | 2 | 10 | `██░░░░░░░░` 20% | 22,081,131 | 967 MiB |
| Databases and data systems | 0 | 6 | `░░░░░░░░░░` 0% | 284,624 | 0 B |
| Editors and developer environments | 0 | 6 | `░░░░░░░░░░` 0% | 1,848,593 | 0 B |
| Foundations and flagship projects | 2 | 8 | `██░░░░░░░░` 25% | 9,429,624 | 157 MiB |
| Graphics, video, and audio | 2 | 10 | `██░░░░░░░░` 20% | 1,405,495 | 15 MiB |
| Infrastructure, automation, and observability | 3 | 11 | `███░░░░░░░` 27% | 1,077,231 | 129 MiB |
| Office, notes, and productivity | 0 | 3 | `░░░░░░░░░░` 0% | 47,193 | 0 B |
| Open machine learning and scientific computing | 0 | 7 | `░░░░░░░░░░` 0% | 2,228,598 | 0 B |
| Open-source and free-software movements | 5 | 6 | `████████░░` 83% | 6,421,806 | 93 MiB |
| Open-source gaming | 2 | 2 | `██████████` 100% | 2,843,319 | 403 MiB |
| Package managers and reproducible systems | 1 | 2 | `█████░░░░░` 50% | 207,150 | 36 MiB |
| Programming languages and runtimes | 1 | 19 | `░░░░░░░░░░` 5% | 10,743,102 | 0 B |
| Self-hosted applications and services | 0 | 8 | `░░░░░░░░░░` 0% | 2,437,951 | 0 B |
| Virtualization, containers, and networking projects | 2 | 5 | `████░░░░░░` 40% | 1,075,325 | 81 MiB |
| Web frameworks and application platforms | 0 | 9 | `░░░░░░░░░░` 0% | 2,779,702 | 0 B |

## Selection boundary

The active census contains all 120 catalogue-verified communities. Excluded unresolved candidates: 10 (3 missing, 7 restricted).

## All panel communities

Expand a category below. Use VS Code search to jump directly to a subreddit.

<details>
<summary><strong>Adjacent package-manager comparator</strong> — 0/1 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/homebrew` | ⚪ Pending | 57,472 | 0/2 | — |

</details>

<details>
<summary><strong>Browsers and privacy tools</strong> — 0/7 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/brave_browser` | ⚪ Pending | 369,989 | 0/2 | — |
| `r/LibreWolf` | ⚪ Pending | 28,569 | 0/2 | — |
| `r/Floorp` | ⚪ Pending | 11,957 | 0/2 | — |
| `r/Bitwarden` | ⚪ Pending | 329,323 | 0/2 | — |
| `r/KeePass` | ⚪ Pending | 44,744 | 0/2 | — |
| `r/signal` | ⚪ Pending | 266,888 | 0/2 | — |
| `r/TOR` | ⚪ Pending | 357,582 | 0/2 | — |

</details>

<details>
<summary><strong>Contribution, collaboration, governance, and documentation</strong> — 2/10 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/git` | ⚪ Pending | 176,617 | 0/2 | — |
| `r/github` | ⚪ Pending | 229,544 | 0/2 | — |
| `r/gitlab` | ⚪ Pending | 39,852 | 0/2 | — |
| `r/coolgithubprojects` | ⚪ Pending | 96,465 | 0/2 | — |
| `r/tinycode` | ⚪ Pending | 11,427 | 0/2 | — |
| `r/programming` | ⚪ Pending | 9,079,458 | 0/2 | — |
| `r/learnprogramming` | ⚪ Pending | 5,234,389 | 0/2 | — |
| `r/devops` | ⚪ Pending | 927,982 | 0/2 | — |
| `r/selfhosted` | 🟢 Complete | 2,139,762 | 2/2 | 332 MiB |
| `r/homelab` | 🟢 Complete | 4,145,635 | 2/2 | 635 MiB |

</details>

<details>
<summary><strong>Databases and data systems</strong> — 0/6 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/PostgreSQL` | ⚪ Pending | 125,145 | 0/2 | — |
| `r/mysql` | ⚪ Pending | 89,532 | 0/2 | — |
| `r/sqlite` | ⚪ Pending | 10,814 | 0/2 | — |
| `r/redis` | ⚪ Pending | 8,972 | 0/2 | — |
| `r/mongodb` | ⚪ Pending | 47,129 | 0/2 | — |
| `r/Clickhouse` | ⚪ Pending | 3,032 | 0/2 | — |

</details>

<details>
<summary><strong>Editors and developer environments</strong> — 0/6 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/vim` | ⚪ Pending | 476,156 | 0/2 | — |
| `r/neovim` | ⚪ Pending | 532,203 | 0/2 | — |
| `r/emacs` | ⚪ Pending | 560,048 | 0/2 | — |
| `r/vscode` | ⚪ Pending | 229,079 | 0/2 | — |
| `r/HelixEditor` | ⚪ Pending | 25,454 | 0/2 | — |
| `r/ZedEditor` | ⚪ Pending | 25,653 | 0/2 | — |

</details>

<details>
<summary><strong>Foundations and flagship projects</strong> — 2/8 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/apache` | ⚪ Pending | 13,885 | 0/2 | — |
| `r/eclipse` | ⚪ Pending | 11,427 | 0/2 | — |
| `r/firefox` | ⚪ Pending | 1,703,058 | 0/2 | — |
| `r/kde` | 🟢 Complete | 748,192 | 2/2 | 106 MiB |
| `r/gnome` | 🟢 Complete | 361,169 | 2/2 | 51 MiB |
| `r/blender` | ⚪ Pending | 4,493,411 | 0/2 | — |
| `r/libreoffice` | ⚪ Pending | 85,534 | 0/2 | — |
| `r/godot` | ⚪ Pending | 2,012,948 | 0/2 | — |

</details>

<details>
<summary><strong>Graphics, video, and audio</strong> — 2/10 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/krita` | ⚪ Pending | 389,742 | 0/2 | — |
| `r/GIMP` | ⚪ Pending | 155,643 | 0/2 | — |
| `r/Inkscape` | ⚪ Pending | 87,066 | 0/2 | — |
| `r/kdenlive` | ⚪ Pending | 37,002 | 0/2 | — |
| `r/obs` | ⚪ Pending | 501,033 | 0/2 | — |
| `r/ffmpeg` | ⚪ Pending | 100,367 | 0/2 | — |
| `r/audacity` | ⚪ Pending | 50,254 | 0/2 | — |
| `r/Ardour` | ⚪ Pending | 2,391 | 0/2 | — |
| `r/pipewire` | 🟢 Complete | 2,600 | 2/2 | 643 KiB |
| `r/linuxaudio` | 🟢 Complete | 79,397 | 2/2 | 15 MiB |

</details>

<details>
<summary><strong>Infrastructure, automation, and observability</strong> — 3/11 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/docker` | 🟢 Complete | 332,812 | 2/2 | 58 MiB |
| `r/podman` | 🟢 Complete | 14,544 | 2/2 | 3 MiB |
| `r/kubernetes` | 🟢 Complete | 398,826 | 2/2 | 69 MiB |
| `r/Terraform` | ⚪ Pending | 124,262 | 0/2 | — |
| `r/opentofu` | 🟠 Fetching | 254 | 0/2 | — |
| `r/ansible` | ⚪ Pending | 131,379 | 0/2 | — |
| `r/Puppet` | ⚪ Pending | 13,309 | 0/2 | — |
| `r/PrometheusMonitoring` | ⚪ Pending | 13,239 | 0/2 | — |
| `r/grafana` | ⚪ Pending | 26,754 | 0/2 | — |
| `r/OpenTelemetry` | ⚪ Pending | 2,327 | 0/2 | — |
| `r/Traefik` | ⚪ Pending | 19,525 | 0/2 | — |

</details>

<details>
<summary><strong>Office, notes, and productivity</strong> — 0/3 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/OnlyOffice` | ⚪ Pending | 8,608 | 0/2 | — |
| `r/joplinapp` | ⚪ Pending | 15,030 | 0/2 | — |
| `r/logseq` | ⚪ Pending | 23,555 | 0/2 | — |

</details>

<details>
<summary><strong>Open machine learning and scientific computing</strong> — 0/7 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/pytorch` | ⚪ Pending | 18,543 | 0/2 | — |
| `r/tensorflow` | ⚪ Pending | 34,315 | 0/2 | — |
| `r/JAX` | ⚪ Pending | 3,750 | 0/2 | — |
| `r/LocalLLaMA` | ⚪ Pending | 2,056,695 | 0/2 | — |
| `r/ollama` | ⚪ Pending | 105,131 | 0/2 | — |
| `r/huggingface` | ⚪ Pending | 7,939 | 0/2 | — |
| `r/Vllm` | ⚪ Pending | 2,225 | 0/2 | — |

</details>

<details>
<summary><strong>Open-source and free-software movements</strong> — 5/6 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/opensource` | 🟢 Complete | 439,717 | 2/2 | 76 MiB |
| `r/foss` | 🟢 Complete | 27,232 | 2/2 | 6 MiB |
| `r/freesoftware` | 🟢 Complete | 50,103 | 2/2 | 9 MiB |
| `r/gnu` | 🟢 Complete | 15,632 | 2/2 | 2 MiB |
| `r/StallmanWasRight` | ⚪ Pending | 172,562 | 0/2 | — |
| `r/linux` | 🟢 Complete | 5,716,560 | 0/2 | — |

</details>

<details>
<summary><strong>Open-source gaming</strong> — 2/2 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/opensourcegames` | 🟢 Complete | 14,764 | 2/2 | 3 MiB |
| `r/linux_gaming` | 🟢 Complete | 2,828,555 | 2/2 | 401 MiB |

</details>

<details>
<summary><strong>Package managers and reproducible systems</strong> — 1/2 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/NixOS` | 🟢 Complete | 202,629 | 2/2 | 36 MiB |
| `r/chocolatey` | ⚪ Pending | 4,521 | 0/2 | — |

</details>

<details>
<summary><strong>Programming languages and runtimes</strong> — 1/19 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/rust` | 🟢 Complete | 1,758,457 | 0/2 | — |
| `r/golang` | ⚪ Pending | 902,755 | 0/2 | — |
| `r/Python` | ⚪ Pending | 1,785,861 | 0/2 | — |
| `r/javascript` | ⚪ Pending | 1,090,069 | 0/2 | — |
| `r/node` | ⚪ Pending | 562,361 | 0/2 | — |
| `r/cpp` | ⚪ Pending | 894,710 | 0/2 | — |
| `r/C_Programming` | ⚪ Pending | 625,423 | 0/2 | — |
| `r/java` | ⚪ Pending | 681,303 | 0/2 | — |
| `r/swift` | ⚪ Pending | 379,505 | 0/2 | — |
| `r/Zig` | ⚪ Pending | 49,585 | 0/2 | — |
| `r/haskell` | ⚪ Pending | 554,312 | 0/2 | — |
| `r/ocaml` | ⚪ Pending | 23,938 | 0/2 | — |
| `r/elixir` | ⚪ Pending | 83,687 | 0/2 | — |
| `r/erlang` | ⚪ Pending | 10,883 | 0/2 | — |
| `r/lua` | ⚪ Pending | 68,728 | 0/2 | — |
| `r/ruby` | ⚪ Pending | 291,041 | 0/2 | — |
| `r/PHP` | ⚪ Pending | 837,812 | 0/2 | — |
| `r/Julia` | ⚪ Pending | 48,750 | 0/2 | — |
| `r/Rlanguage` | ⚪ Pending | 93,922 | 0/2 | — |

</details>

<details>
<summary><strong>Self-hosted applications and services</strong> — 0/8 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/NextCloud` | ⚪ Pending | 148,605 | 0/2 | — |
| `r/immich` | ⚪ Pending | 124,682 | 0/2 | — |
| `r/Paperlessngx` | ⚪ Pending | 8,405 | 0/2 | — |
| `r/Gitea` | ⚪ Pending | 1,746 | 0/2 | — |
| `r/forgejo` | ⚪ Pending | 536 | 0/2 | — |
| `r/vaultwarden` | ⚪ Pending | 5,882 | 0/2 | — |
| `r/homeassistant` | ⚪ Pending | 2,126,527 | 0/2 | — |
| `r/Syncthing` | ⚪ Pending | 21,568 | 0/2 | — |

</details>

<details>
<summary><strong>Virtualization, containers, and networking projects</strong> — 2/5 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/Proxmox` | 🟢 Complete | 464,854 | 2/2 | 81 MiB |
| `r/qemu_kvm` | ⚪ Pending | 11,727 | 0/2 | — |
| `r/LXC` | 🟢 Complete | 3,319 | 2/2 | 514 KiB |
| `r/opnsense` | ⚪ Pending | 118,764 | 0/2 | — |
| `r/PFSENSE` | ⚪ Pending | 476,661 | 0/2 | — |

</details>

<details>
<summary><strong>Web frameworks and application platforms</strong> — 0/9 available</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/reactjs` | ⚪ Pending | 990,669 | 0/2 | — |
| `r/vuejs` | ⚪ Pending | 258,523 | 0/2 | — |
| `r/angular` | ⚪ Pending | 92,720 | 0/2 | — |
| `r/sveltejs` | ⚪ Pending | 171,407 | 0/2 | — |
| `r/nextjs` | ⚪ Pending | 374,602 | 0/2 | — |
| `r/laravel` | ⚪ Pending | 305,805 | 0/2 | — |
| `r/django` | ⚪ Pending | 436,184 | 0/2 | — |
| `r/flask` | ⚪ Pending | 126,123 | 0/2 | — |
| `r/FastAPI` | ⚪ Pending | 23,669 | 0/2 | — |

</details>

---

🟢 present in both MongoDB collections · 🟠 fetching/validating/loading · 🟡 one raw file present · ⚪ pending
