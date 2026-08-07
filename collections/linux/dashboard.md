# Linux subreddit collection dashboard

_Refreshed 2026-08-07 13:45 UTC from MongoDB, the Linux catalogue, `targets.txt`, and `data/raw/`._

> Open with **Markdown: Open Preview** (`Ctrl+Shift+V` / `Cmd+Shift+V`). The tmux worker refreshes this file after every successful load.

## Status

| Panel N | Available | Partial acquisition | Remaining | Expected records | New raw data | Workflow |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 99 | 99 | 0 | 0 | 58,235,417 | 6.6 GiB | `active` |

**Panel availability:** `████████████████████████` 100%

- tmux session: `reddit_linux_collection`
- runtime log: `data/logs/linux-collection.log`
- destination: MongoDB `localhost:27017`, database `reddit`
- queue policy: one low-priority worker, smallest expected capture first
- music protection: Linux API requests pause while the music worker fetches

## Next in queue

| # | Subreddit | Category | Expected records | Existing raw |
| ---: | --- | --- | ---: | ---: |
| — | Queue complete | — | — | — |

## Progress by category

| Category | Complete | Tracked | Progress | Expected records | Raw data |
| --- | ---: | ---: | --- | ---: | ---: |
| General discussion, news, support, and discovery | 5 | 5 | `██████████` 100% | 10,116,908 | 260 KiB |
| Kernel-adjacent, embedded, and low-level systems | 1 | 1 | `██████████` 100% | 94,028 | 0 B |
| Uncategorised | 93 | 93 | `██████████` 100% | 48,024,481 | 6.6 GiB |

## Existing MongoDB holdings

6 Linux panel members were present in both MongoDB collections before the 93-target acquisition queue started.

| Subreddit | Panel status | MongoDB status | Acquisition action |
| --- | --- | --- | --- |
| `r/kernel` | Included in N=99 | Present in both collections | Skip |
| `r/linusrants` | Included in N=99 | Present in both collections | Skip |
| `r/linux` | Included in N=99 | Present in both collections | Skip |
| `r/linux4noobs` | Included in N=99 | Present in both collections | Skip |
| `r/linuxquestions` | Included in N=99 | Present in both collections | Skip |
| `r/osdev` | Included in N=99 | Present in both collections | Skip |

_Excluded unresolved candidates: 21 (missing or restricted at catalogue verification)._

## All panel communities

Expand a category below. Use VS Code search to jump directly to a subreddit.

<details>
<summary><strong>General discussion, news, support, and discovery</strong> — 5/5 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/linux` | 🟢 Complete | 5,716,560 | 0/2 | — |
| `r/linusrants` | 🟢 Complete | 1,849 | 2/2 | 260 KiB |
| `r/linuxquestions` | 🟢 Complete | 2,532,875 | 0/2 | — |
| `r/linux4noobs` | 🟢 Complete | 1,853,344 | 0/2 | — |
| `r/kernel` | 🟢 Complete | 12,280 | 0/2 | — |

</details>

<details>
<summary><strong>Kernel-adjacent, embedded, and low-level systems</strong> — 1/1 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/osdev` | 🟢 Complete | 94,028 | 0/2 | — |

</details>

<details>
<summary><strong>Uncategorised</strong> — 93/93 complete</summary>

| Subreddit | Status | Expected records | Raw files | Raw size |
| --- | --- | ---: | ---: | ---: |
| `r/linuxadmin` | 🟢 Complete | 331,451 | 2/2 | 52 MiB |
| `r/linuxhardware` | 🟢 Complete | 180,943 | 2/2 | 30 MiB |
| `r/linuxprojects` | 🟢 Complete | 695 | 2/2 | 216 KiB |
| `r/linuxunplugged` | 🟢 Complete | 4,396 | 2/2 | 991 KiB |
| `r/linuxmemes` | 🟢 Complete | 1,230,719 | 2/2 | 128 MiB |
| `r/DistroHopping` | 🟢 Complete | 120,252 | 2/2 | 17 MiB |
| `r/FindMeALinuxDistro` | 🟢 Complete | 27,928 | 2/2 | 4 MiB |
| `r/embedded` | 🟢 Complete | 576,897 | 2/2 | 103 MiB |
| `r/raspberry_pi` | 🟢 Complete | 1,424,057 | 2/2 | 185 MiB |
| `r/systemd` | 🟢 Complete | 5,686 | 2/2 | 1 MiB |
| `r/wayland` | 🟢 Complete | 9,534 | 2/2 | 2 MiB |
| `r/pipewire` | 🟢 Complete | 2,600 | 2/2 | 643 KiB |
| `r/linuxaudio` | 🟢 Complete | 79,397 | 2/2 | 15 MiB |
| `r/zfs` | 🟢 Complete | 143,809 | 2/2 | 28 MiB |
| `r/btrfs` | 🟢 Complete | 48,567 | 2/2 | 9 MiB |
| `r/debian` | 🟢 Complete | 571,925 | 2/2 | 84 MiB |
| `r/Ubuntu` | 🟢 Complete | 1,263,490 | 2/2 | 170 MiB |
| `r/linuxmint` | 🟢 Complete | 951,952 | 2/2 | 141 MiB |
| `r/pop_os` | 🟢 Complete | 520,216 | 2/2 | 77 MiB |
| `r/elementaryos` | 🟢 Complete | 130,248 | 2/2 | 17 MiB |
| `r/Kubuntu` | 🟢 Complete | 51,657 | 2/2 | 9 MiB |
| `r/Lubuntu` | 🟢 Complete | 20,114 | 2/2 | 3 MiB |
| `r/xubuntu` | 🟢 Complete | 11,904 | 2/2 | 2 MiB |
| `r/Fedora` | 🟢 Complete | 803,110 | 2/2 | 120 MiB |
| `r/FedoraWorkstation` | 🟢 Complete | 7 | 2/2 | 6 KiB |
| `r/FedoraSilverblue` | 🟢 Complete | 648 | 2/2 | 145 KiB |
| `r/redhat` | 🟢 Complete | 119,840 | 2/2 | 18 MiB |
| `r/RockyLinux` | 🟢 Complete | 11,262 | 2/2 | 2 MiB |
| `r/AlmaLinux` | 🟢 Complete | 12,149 | 2/2 | 2 MiB |
| `r/CentOS` | 🟢 Complete | 38,457 | 2/2 | 6 MiB |
| `r/archlinux` | 🟢 Complete | 1,395,549 | 2/2 | 194 MiB |
| `r/EndeavourOS` | 🟢 Complete | 74,430 | 2/2 | 11 MiB |
| `r/ManjaroLinux` | 🟢 Complete | 245,005 | 2/2 | 35 MiB |
| `r/artixlinux` | 🟢 Complete | 18,489 | 2/2 | 3 MiB |
| `r/cachyos` | 🟢 Complete | 231,572 | 2/2 | 39 MiB |
| `r/GarudaLinux` | 🟢 Complete | 12,946 | 2/2 | 2 MiB |
| `r/NixOS` | 🟢 Complete | 202,629 | 2/2 | 36 MiB |
| `r/Nix` | 🟢 Complete | 5,176 | 2/2 | 1 MiB |
| `r/openSUSE` | 🟢 Complete | 264,232 | 2/2 | 41 MiB |
| `r/Gentoo` | 🟢 Complete | 230,440 | 2/2 | 34 MiB |
| `r/voidlinux` | 🟢 Complete | 130,441 | 2/2 | 19 MiB |
| `r/AlpineLinux` | 🟢 Complete | 12,475 | 2/2 | 2 MiB |
| `r/slackware` | 🟢 Complete | 19,755 | 2/2 | 3 MiB |
| `r/linuxfromscratch` | 🟢 Complete | 7,032 | 2/2 | 1 MiB |
| `r/bedrocklinux` | 🟢 Complete | 6,085 | 2/2 | 1 MiB |
| `r/MXLinux` | 🟢 Complete | 23,002 | 2/2 | 4 MiB |
| `r/SolusProject` | 🟢 Complete | 76,074 | 2/2 | 10 MiB |
| `r/Universalblue` | 🟢 Complete | 305 | 2/2 | 93 KiB |
| `r/Qubes` | 🟢 Complete | 53,633 | 2/2 | 8 MiB |
| `r/tails` | 🟢 Complete | 136,056 | 2/2 | 17 MiB |
| `r/Kalilinux` | 🟢 Complete | 146,928 | 2/2 | 19 MiB |
| `r/gnome` | 🟢 Complete | 361,169 | 2/2 | 51 MiB |
| `r/kde` | 🟢 Complete | 748,192 | 2/2 | 106 MiB |
| `r/xfce` | 🟢 Complete | 53,864 | 2/2 | 8 MiB |
| `r/LXQt` | 🟢 Complete | 2,600 | 2/2 | 420 KiB |
| `r/System76` | 🟢 Complete | 51,675 | 2/2 | 8 MiB |
| `r/swaywm` | 🟢 Complete | 59,635 | 2/2 | 9 MiB |
| `r/hyprland` | 🟢 Complete | 191,362 | 2/2 | 29 MiB |
| `r/bspwm` | 🟢 Complete | 21,216 | 2/2 | 3 MiB |
| `r/awesomewm` | 🟢 Complete | 30,377 | 2/2 | 5 MiB |
| `r/dwm` | 🟢 Complete | 6,590 | 2/2 | 967 KiB |
| `r/qtile` | 🟢 Complete | 9,977 | 2/2 | 2 MiB |
| `r/xmonad` | 🟢 Complete | 14,276 | 2/2 | 2 MiB |
| `r/openbox` | 🟢 Complete | 4,051 | 2/2 | 642 KiB |
| `r/unixporn` | 🟢 Complete | 1,522,508 | 2/2 | 168 MiB |
| `r/commandline` | 🟢 Complete | 221,513 | 2/2 | 38 MiB |
| `r/bash` | 🟢 Complete | 164,025 | 2/2 | 28 MiB |
| `r/flatpak` | 🟢 Complete | 14,405 | 2/2 | 3 MiB |
| `r/AppImage` | 🟢 Complete | 1,131 | 2/2 | 371 KiB |
| `r/snapcraft` | 🟢 Complete | 15 | 2/2 | 6 KiB |
| `r/docker` | 🟢 Complete | 332,812 | 2/2 | 58 MiB |
| `r/podman` | 🟢 Complete | 14,544 | 2/2 | 3 MiB |
| `r/kubernetes` | 🟢 Complete | 398,826 | 2/2 | 69 MiB |
| `r/LXC` | 🟢 Complete | 3,319 | 2/2 | 514 KiB |
| `r/Proxmox` | 🟢 Complete | 464,854 | 2/2 | 81 MiB |
| `r/selfhosted` | 🟢 Complete | 2,139,762 | 2/2 | 332 MiB |
| `r/homelab` | 🟢 Complete | 4,145,635 | 2/2 | 635 MiB |
| `r/sysadmin` | 🟢 Complete | 11,546,617 | 2/2 | 1.6 GiB |
| `r/VFIO` | 🟢 Complete | 154,734 | 2/2 | 28 MiB |
| `r/linux_gaming` | 🟢 Complete | 2,828,555 | 2/2 | 401 MiB |
| `r/wine_gaming` | 🟢 Complete | 84,215 | 2/2 | 13 MiB |
| `r/SteamPlay` | 🟢 Complete | 33,938 | 2/2 | 5 MiB |
| `r/opensourcegames` | 🟢 Complete | 14,764 | 2/2 | 3 MiB |
| `r/chromeos` | 🟢 Complete | 1,044,693 | 2/2 | 139 MiB |
| `r/SteamDeck` | 🟢 Complete | 8,401,995 | 2/2 | 1.0 GiB |
| `r/steamdeckhq` | 🟢 Complete | 24,427 | 2/2 | 4 MiB |
| `r/SteamOS` | 🟢 Complete | 94,211 | 2/2 | 15 MiB |
| `r/openwrt` | 🟢 Complete | 155,799 | 2/2 | 26 MiB |
| `r/termux` | 🟢 Complete | 143,352 | 2/2 | 21 MiB |
| `r/opensource` | 🟢 Complete | 439,717 | 2/2 | 76 MiB |
| `r/foss` | 🟢 Complete | 27,232 | 2/2 | 6 MiB |
| `r/freesoftware` | 🟢 Complete | 50,103 | 2/2 | 9 MiB |
| `r/gnu` | 🟢 Complete | 15,632 | 2/2 | 2 MiB |

</details>

---

🟢 present in both MongoDB collections · 🟡 one raw file present · ⚪ pending acquisition
