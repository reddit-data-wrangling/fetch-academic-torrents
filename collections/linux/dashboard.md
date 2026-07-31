# Linux subreddit collection dashboard

_Refreshed 2026-07-31 20:58 UTC from MongoDB, the Linux catalogue, `targets.txt`, and `data/raw/`._

> Open with **Markdown: Open Preview** (`Ctrl+Shift+V` / `Cmd+Shift+V`). The tmux worker refreshes this file after every successful load.

## Status

| Panel N | Available | Partial acquisition | Remaining | Expected records | New raw data | Workflow |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 99 | 49 | 0 | 50 | 58,235,417 | 119 MiB | `active` |

**Panel availability:** `████████████░░░░░░░░░░░░` 49%

- tmux session: `reddit_linux_collection`
- runtime log: `data/logs/linux-collection.log`
- destination: MongoDB `localhost:27017`, database `reddit`
- queue policy: one low-priority worker, smallest expected capture first
- music protection: Linux API requests pause while the music worker fetches

## Next in queue

| # | Subreddit | Category | Expected records | Existing raw |
| ---: | --- | --- | ---: | ---: |
| 1 | `r/Qubes` | Security-focused distributions | 53,633 | 0/2 files |
| 2 | `r/xfce` | Desktop environments | 53,864 | 0/2 files |
| 3 | `r/swaywm` | Window managers, shells, and desktop customization | 59,635 | 0/2 files |
| 4 | `r/EndeavourOS` | Arch family | 74,430 | 0/2 files |
| 5 | `r/SolusProject` | Nix, openSUSE, source-based, and independent distributions | 76,074 | 0/2 files |
| 6 | `r/linuxaudio` | Kernel-adjacent, embedded, and low-level systems | 79,397 | 0/2 files |
| 7 | `r/wine_gaming` | Linux gaming | 84,215 | 0/2 files |
| 8 | `r/SteamOS` | Device, mobile, and specialist Linux systems | 94,211 | 0/2 files |
| 9 | `r/redhat` | Fedora and Red Hat families | 119,840 | 0/2 files |
| 10 | `r/DistroHopping` | General discussion, news, support, and discovery | 120,252 | 0/2 files |
| 11 | `r/elementaryos` | Debian and Ubuntu families | 130,248 | 0/2 files |
| 12 | `r/voidlinux` | Nix, openSUSE, source-based, and independent distributions | 130,441 | 0/2 files |
| 13 | `r/tails` | Security-focused distributions | 136,056 | 0/2 files |
| 14 | `r/termux` | Device, mobile, and specialist Linux systems | 143,352 | 0/2 files |
| 15 | `r/zfs` | Kernel-adjacent, embedded, and low-level systems | 143,809 | 0/2 files |

## Progress by category

| Category | Complete | Tracked | Progress | Expected records | Raw data |
| --- | ---: | ---: | --- | ---: | ---: |
| Arch family | 2 | 6 | `███░░░░░░░` 33% | 1,977,991 | 5 MiB |
| Containers, virtualization, administration, and self-hosting | 2 | 9 | `██░░░░░░░░` 22% | 19,201,103 | 3 MiB |
| Debian and Ubuntu families | 3 | 8 | `████░░░░░░` 38% | 3,521,506 | 14 MiB |
| Desktop environments | 2 | 5 | `████░░░░░░` 40% | 1,217,500 | 8 MiB |
| Device, mobile, and specialist Linux systems | 1 | 6 | `██░░░░░░░░` 17% | 9,864,477 | 4 MiB |
| Fedora and Red Hat families | 5 | 7 | `███████░░░` 71% | 985,473 | 10 MiB |
| General discussion, news, support, and discovery | 8 | 12 | `███████░░░` 67% | 12,013,292 | 6 MiB |
| Immutable and image-based Linux | 1 | 1 | `██████████` 100% | 305 | 93 KiB |
| Kernel-adjacent, embedded, and low-level systems | 5 | 9 | `██████░░░░` 56% | 2,384,575 | 13 MiB |
| Linux gaming | 2 | 4 | `█████░░░░░` 50% | 2,961,472 | 8 MiB |
| Nix, openSUSE, source-based, and independent distributions | 6 | 11 | `██████░░░░` 55% | 977,341 | 13 MiB |
| Open-source ecosystem | 3 | 4 | `████████░░` 75% | 532,684 | 17 MiB |
| Packaging and application distribution | 3 | 3 | `██████████` 100% | 15,551 | 3 MiB |
| Security-focused distributions | 0 | 3 | `░░░░░░░░░░` 0% | 336,617 | 0 B |
| Window managers, shells, and desktop customization | 6 | 11 | `██████░░░░` 55% | 2,245,530 | 14 MiB |

## Existing MongoDB holdings

6 Linux panel members were present in both MongoDB collections before the 93-target acquisition queue started. 2 additional communities are held outside the N=99 panel.

| Subreddit | Panel status | MongoDB status | Acquisition action |
| --- | --- | --- | --- |
| `r/kernel` | Included in N=99 | Present in both collections | Skip |
| `r/linusrants` | Included in N=99 | Present in both collections | Skip |
| `r/linux` | Included in N=99 | Present in both collections | Skip |
| `r/linux4noobs` | Included in N=99 | Present in both collections | Skip |
| `r/linuxquestions` | Included in N=99 | Present in both collections | Skip |
| `r/osdev` | Included in N=99 | Present in both collections | Skip |
| `r/rust` | Outside panel | Present in both collections | Skip |
| `r/wikipedia` | Outside panel | Present in both collections | Skip |

_Excluded unresolved candidates: 21 (missing or restricted at catalogue verification)._

## All panel communities

Expand a category below. Use VS Code search to jump directly to a subreddit.

<details>
<summary><strong>Arch family</strong> — 2/6 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/archlinux` | ⚪ Pending | 1,395,549 | 0/2 | — |
| `r/EndeavourOS` | ⚪ Pending | 74,430 | 0/2 | — |
| `r/ManjaroLinux` | ⚪ Pending | 245,005 | 0/2 | — |
| `r/artixlinux` | 🟢 Complete | 18,489 | 2/2 | 3 MiB |
| `r/cachyos` | ⚪ Pending | 231,572 | 0/2 | — |
| `r/GarudaLinux` | 🟢 Complete | 12,946 | 2/2 | 2 MiB |

</details>

<details>
<summary><strong>Containers, virtualization, administration, and self-hosting</strong> — 2/9 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/docker` | ⚪ Pending | 332,812 | 0/2 | — |
| `r/podman` | 🟢 Complete | 14,544 | 2/2 | 3 MiB |
| `r/kubernetes` | ⚪ Pending | 398,826 | 0/2 | — |
| `r/LXC` | 🟢 Complete | 3,319 | 2/2 | 514 KiB |
| `r/Proxmox` | ⚪ Pending | 464,854 | 0/2 | — |
| `r/selfhosted` | ⚪ Pending | 2,139,762 | 0/2 | — |
| `r/homelab` | ⚪ Pending | 4,145,635 | 0/2 | — |
| `r/sysadmin` | ⚪ Pending | 11,546,617 | 0/2 | — |
| `r/VFIO` | ⚪ Pending | 154,734 | 0/2 | — |

</details>

<details>
<summary><strong>Debian and Ubuntu families</strong> — 3/8 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/debian` | ⚪ Pending | 571,925 | 0/2 | — |
| `r/Ubuntu` | ⚪ Pending | 1,263,490 | 0/2 | — |
| `r/linuxmint` | ⚪ Pending | 951,952 | 0/2 | — |
| `r/pop_os` | ⚪ Pending | 520,216 | 0/2 | — |
| `r/elementaryos` | ⚪ Pending | 130,248 | 0/2 | — |
| `r/Kubuntu` | 🟢 Complete | 51,657 | 2/2 | 9 MiB |
| `r/Lubuntu` | 🟢 Complete | 20,114 | 2/2 | 3 MiB |
| `r/xubuntu` | 🟢 Complete | 11,904 | 2/2 | 2 MiB |

</details>

<details>
<summary><strong>Desktop environments</strong> — 2/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/gnome` | ⚪ Pending | 361,169 | 0/2 | — |
| `r/kde` | ⚪ Pending | 748,192 | 0/2 | — |
| `r/xfce` | ⚪ Pending | 53,864 | 0/2 | — |
| `r/LXQt` | 🟢 Complete | 2,600 | 2/2 | 420 KiB |
| `r/System76` | 🟢 Complete | 51,675 | 2/2 | 8 MiB |

</details>

<details>
<summary><strong>Device, mobile, and specialist Linux systems</strong> — 1/6 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/chromeos` | ⚪ Pending | 1,044,693 | 0/2 | — |
| `r/SteamDeck` | ⚪ Pending | 8,401,995 | 0/2 | — |
| `r/steamdeckhq` | 🟢 Complete | 24,427 | 2/2 | 4 MiB |
| `r/SteamOS` | ⚪ Pending | 94,211 | 0/2 | — |
| `r/openwrt` | ⚪ Pending | 155,799 | 0/2 | — |
| `r/termux` | ⚪ Pending | 143,352 | 0/2 | — |

</details>

<details>
<summary><strong>Fedora and Red Hat families</strong> — 5/7 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/Fedora` | ⚪ Pending | 803,110 | 0/2 | — |
| `r/FedoraWorkstation` | 🟢 Complete | 7 | 2/2 | 6 KiB |
| `r/FedoraSilverblue` | 🟢 Complete | 648 | 2/2 | 145 KiB |
| `r/redhat` | ⚪ Pending | 119,840 | 0/2 | — |
| `r/RockyLinux` | 🟢 Complete | 11,262 | 2/2 | 2 MiB |
| `r/AlmaLinux` | 🟢 Complete | 12,149 | 2/2 | 2 MiB |
| `r/CentOS` | 🟢 Complete | 38,457 | 2/2 | 6 MiB |

</details>

<details>
<summary><strong>General discussion, news, support, and discovery</strong> — 8/12 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/linuxadmin` | ⚪ Pending | 331,451 | 0/2 | — |
| `r/linuxhardware` | ⚪ Pending | 180,943 | 0/2 | — |
| `r/linuxprojects` | 🟢 Complete | 695 | 2/2 | 216 KiB |
| `r/linuxunplugged` | 🟢 Complete | 4,396 | 2/2 | 991 KiB |
| `r/linuxmemes` | ⚪ Pending | 1,230,719 | 0/2 | — |
| `r/DistroHopping` | ⚪ Pending | 120,252 | 0/2 | — |
| `r/FindMeALinuxDistro` | 🟢 Complete | 27,928 | 2/2 | 4 MiB |
| `r/linux` | 🟢 Complete | 5,716,560 | 0/2 | — |
| `r/linusrants` | 🟢 Complete | 1,849 | 2/2 | 260 KiB |
| `r/linuxquestions` | 🟢 Complete | 2,532,875 | 0/2 | — |
| `r/linux4noobs` | 🟢 Complete | 1,853,344 | 0/2 | — |
| `r/kernel` | 🟢 Complete | 12,280 | 0/2 | — |

</details>

<details>
<summary><strong>Immutable and image-based Linux</strong> — 1/1 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/Universalblue` | 🟢 Complete | 305 | 2/2 | 93 KiB |

</details>

<details>
<summary><strong>Kernel-adjacent, embedded, and low-level systems</strong> — 5/9 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/embedded` | ⚪ Pending | 576,897 | 0/2 | — |
| `r/raspberry_pi` | ⚪ Pending | 1,424,057 | 0/2 | — |
| `r/systemd` | 🟢 Complete | 5,686 | 2/2 | 1 MiB |
| `r/wayland` | 🟢 Complete | 9,534 | 2/2 | 2 MiB |
| `r/pipewire` | 🟢 Complete | 2,600 | 2/2 | 643 KiB |
| `r/linuxaudio` | ⚪ Pending | 79,397 | 0/2 | — |
| `r/zfs` | ⚪ Pending | 143,809 | 0/2 | — |
| `r/btrfs` | 🟢 Complete | 48,567 | 2/2 | 9 MiB |
| `r/osdev` | 🟢 Complete | 94,028 | 0/2 | — |

</details>

<details>
<summary><strong>Linux gaming</strong> — 2/4 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/linux_gaming` | ⚪ Pending | 2,828,555 | 0/2 | — |
| `r/wine_gaming` | ⚪ Pending | 84,215 | 0/2 | — |
| `r/SteamPlay` | 🟢 Complete | 33,938 | 2/2 | 5 MiB |
| `r/opensourcegames` | 🟢 Complete | 14,764 | 2/2 | 3 MiB |

</details>

<details>
<summary><strong>Nix, openSUSE, source-based, and independent distributions</strong> — 6/11 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/NixOS` | ⚪ Pending | 202,629 | 0/2 | — |
| `r/Nix` | 🟢 Complete | 5,176 | 2/2 | 1 MiB |
| `r/openSUSE` | ⚪ Pending | 264,232 | 0/2 | — |
| `r/Gentoo` | ⚪ Pending | 230,440 | 0/2 | — |
| `r/voidlinux` | ⚪ Pending | 130,441 | 0/2 | — |
| `r/AlpineLinux` | 🟢 Complete | 12,475 | 2/2 | 2 MiB |
| `r/slackware` | 🟢 Complete | 19,755 | 2/2 | 3 MiB |
| `r/linuxfromscratch` | 🟢 Complete | 7,032 | 2/2 | 1 MiB |
| `r/bedrocklinux` | 🟢 Complete | 6,085 | 2/2 | 1 MiB |
| `r/MXLinux` | 🟢 Complete | 23,002 | 2/2 | 4 MiB |
| `r/SolusProject` | ⚪ Pending | 76,074 | 0/2 | — |

</details>

<details>
<summary><strong>Open-source ecosystem</strong> — 3/4 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/opensource` | ⚪ Pending | 439,717 | 0/2 | — |
| `r/foss` | 🟢 Complete | 27,232 | 2/2 | 6 MiB |
| `r/freesoftware` | 🟢 Complete | 50,103 | 2/2 | 9 MiB |
| `r/gnu` | 🟢 Complete | 15,632 | 2/2 | 2 MiB |

</details>

<details>
<summary><strong>Packaging and application distribution</strong> — 3/3 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/flatpak` | 🟢 Complete | 14,405 | 2/2 | 3 MiB |
| `r/AppImage` | 🟢 Complete | 1,131 | 2/2 | 371 KiB |
| `r/snapcraft` | 🟢 Complete | 15 | 2/2 | 6 KiB |

</details>

<details>
<summary><strong>Security-focused distributions</strong> — 0/3 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/Qubes` | ⚪ Pending | 53,633 | 0/2 | — |
| `r/tails` | ⚪ Pending | 136,056 | 0/2 | — |
| `r/Kalilinux` | ⚪ Pending | 146,928 | 0/2 | — |

</details>

<details>
<summary><strong>Window managers, shells, and desktop customization</strong> — 6/11 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/swaywm` | ⚪ Pending | 59,635 | 0/2 | — |
| `r/hyprland` | ⚪ Pending | 191,362 | 0/2 | — |
| `r/bspwm` | 🟢 Complete | 21,216 | 2/2 | 3 MiB |
| `r/awesomewm` | 🟢 Complete | 30,377 | 2/2 | 5 MiB |
| `r/dwm` | 🟢 Complete | 6,590 | 2/2 | 967 KiB |
| `r/qtile` | 🟢 Complete | 9,977 | 2/2 | 2 MiB |
| `r/xmonad` | 🟢 Complete | 14,276 | 2/2 | 2 MiB |
| `r/openbox` | 🟢 Complete | 4,051 | 2/2 | 642 KiB |
| `r/unixporn` | ⚪ Pending | 1,522,508 | 0/2 | — |
| `r/commandline` | ⚪ Pending | 221,513 | 0/2 | — |
| `r/bash` | ⚪ Pending | 164,025 | 0/2 | — |

</details>

---

🟢 present in both MongoDB collections · 🟡 one raw file present · ⚪ pending acquisition
