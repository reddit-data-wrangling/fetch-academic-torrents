"""Generate a collection-progress dashboard for VS Code Markdown Preview."""

from __future__ import annotations

import argparse
import json
import re
import tomllib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from pymongo import MongoClient
from pymongo.errors import PyMongoError

ROOT = Path(__file__).resolve().parent.parent
COLLECTIONS_DIR = ROOT / "collections"
MUSIC_DIR = COLLECTIONS_DIR / "music"
LINUX_DIR = COLLECTIONS_DIR / "linux"
BEER_DIR = COLLECTIONS_DIR / "beer"
COMICS_DIR = COLLECTIONS_DIR / "comics"
MOVIES_DIR = COLLECTIONS_DIR / "movies"
OSS_DIR = COLLECTIONS_DIR / "oss"
RAW_DIR = ROOT / "data" / "raw"
COMICS_MOVIES_STATE = ROOT / "data" / "logs" / "comics-movies-state.json"
OSS_STATE = ROOT / "data" / "logs" / "oss-state.json"
DEFAULT_OUTPUT = ROOT / "COLLECTION_PROGRESS.md"
DEFAULT_COMICS_MOVIES_OUTPUT = ROOT / "COMICS_MOVIES_PROGRESS.md"
MONGO_COMPLETE_CACHE: dict[tuple[str, str], set[str]] = {}


def read_names(path: Path) -> tuple[list[str], dict[str, str]]:
    names: list[str] = []
    groups: dict[str, str] = {}
    seen: set[str] = set()
    group = "Uncategorised"
    if not path.is_file():
        return names, groups
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            group = line[3:].strip()
        elif line and not line.startswith("#"):
            name = line.removeprefix("r/")
            key = name.casefold()
            if key not in seen:
                seen.add(key)
                names.append(name)
                groups[key] = group
    return names, groups


def read_catalog(path: Path) -> dict[str, dict]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        item["subreddit"].casefold(): item
        for item in payload.get("communities", [])
        if item.get("subreddit")
    }


def integer(value: str) -> int:
    digits = re.sub(r"[^\d-]", "", value)
    return int(digits) if digits not in {"", "-"} else 0


def read_progress(path: Path) -> dict[str, dict]:
    """Read an optional progress.md table such as the music programme."""
    rows: dict[str, dict] = {}
    if not path.is_file():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^\|\s*\d+\s*\|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 8:
            continue
        name = cells[1].removeprefix("r/")
        raw_status = cells[3].casefold()
        status = (
            "complete"
            if "done" in raw_status
            else "loading"
            if "loading" in raw_status
            else "fetching"
            if "fetching" in raw_status
            else "pending"
        )
        expected = integer(cells[4]) + integer(cells[5])
        loaded = integer(cells[6]) + integer(cells[7])
        percent = min(100, round(loaded / expected * 100)) if expected else 0
        if status == "complete":
            percent = 100
        rows[name.casefold()] = {
            "name": name,
            "order": integer(cells[0]),
            "category": cells[2],
            "status": status,
            "percent": percent,
            "expected_posts": integer(cells[4]),
            "expected_comments": integer(cells[5]),
            "expected": expected,
        }
    return rows


def read_comics_movies_state() -> dict:
    if not COMICS_MOVIES_STATE.is_file():
        return {}
    try:
        payload = json.loads(COMICS_MOVIES_STATE.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def read_oss_state() -> dict:
    if not OSS_STATE.is_file():
        return {}
    try:
        payload = json.loads(OSS_STATE.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def raw_files() -> tuple[dict[tuple[str, str], int], int]:
    files: dict[tuple[str, str], int] = {}
    total_bytes = 0
    if not RAW_DIR.is_dir():
        return files, total_bytes
    for path in RAW_DIR.glob("*.zst"):
        match = re.match(r"(.+)_(submissions|comments)\.zst$", path.name)
        if match:
            name, kind = match.groups()
            size = path.stat().st_size
            files[(name.casefold(), kind)] = size
            total_bytes += size
    return files, total_bytes


def completed_in_mongo(config: dict) -> set[str]:
    """Return communities present in both Mongo collections when available."""
    mongo_uri = config.get("mongo_uri")
    database = config.get("mongo_database")
    if not mongo_uri or not database:
        return set()
    cache_key = (str(mongo_uri), str(database))
    if cache_key in MONGO_COMPLETE_CACHE:
        return MONGO_COMPLETE_CACHE[cache_key]
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=1_500)
        db = client[database]
        submissions = {
            str(name).casefold()
            for name in db.submissions.distinct("subreddit", maxTimeMS=10_000)
        }
        comments = {
            str(name).casefold()
            for name in db.comments.distinct("subreddit", maxTimeMS=10_000)
        }
        client.close()
        complete = submissions & comments
        MONGO_COMPLETE_CACHE[cache_key] = complete
        return complete
    except PyMongoError:
        MONGO_COMPLETE_CACHE[cache_key] = set()
        return MONGO_COMPLETE_CACHE[cache_key]


def human_bytes(value: int) -> str:
    size = float(value)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if size < 1024 or unit == "TiB":
            return f"{size:.1f} {unit}" if unit in {"GiB", "TiB"} else f"{size:.0f} {unit}"
        size /= 1024
    return f"{value} B"


def markdown(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def progress_bar(percent: int, width: int = 12) -> str:
    filled = round(percent / 100 * width)
    return f"`{'█' * filled}{'░' * (width - filled)}` {percent}%"


def status_label(status: str) -> str:
    return {
        "complete": "🟢 Complete",
        "loading": "🟠 Loading",
        "fetching": "🟠 Fetching",
        "partial": "🟡 Partial",
        "pending": "⚪ Pending",
    }[status]


def collect_state(only_slug: str | None = None) -> tuple[list[dict], int]:
    raw, total_raw_bytes = raw_files()
    comics_movies_worker_state = read_comics_movies_state()
    oss_worker_state = read_oss_state()
    themes: list[dict] = []

    for config_path in sorted(COLLECTIONS_DIR.glob("*/collection.toml")):
        directory = config_path.parent
        slug = directory.name
        if only_slug is not None and slug != only_slug:
            continue
        with config_path.open("rb") as stream:
            config = tomllib.load(stream)
        candidates, groups = read_names(directory / "subreddits.txt")
        targets, target_groups = read_names(directory / "targets.txt")
        target_order = {
            name.casefold(): position for position, name in enumerate(targets, start=1)
        }
        catalog = read_catalog(directory / "catalog.json")
        progress = read_progress(directory / "progress.md")
        worker_state = (
            oss_worker_state if slug == "oss" else comics_movies_worker_state
        )
        if slug == "oss" and isinstance(
            oss_worker_state.get("complete_names"), list
        ):
            mongo_complete = {
                str(name).casefold()
                for name in oss_worker_state["complete_names"]
            }
        elif slug in {"beer", "comics", "linux", "movies", "music", "oss"}:
            mongo_complete = completed_in_mongo(config)
        else:
            mongo_complete = set()

        order: list[str] = []
        names: dict[str, str] = {}
        for name in candidates:
            key = name.casefold()
            order.append(key)
            names[key] = name
        for key, item in catalog.items():
            if key not in names:
                order.append(key)
                names[key] = item["subreddit"]
        for key, item in sorted(progress.items(), key=lambda row: row[1]["order"]):
            if key not in names:
                order.append(key)
                names[key] = item["name"]

        subreddits = []
        for key in order:
            captures = {
                kind: raw.get((key, kind), 0)
                for kind in ("submissions", "comments")
            }
            present = sum(bool(size) for size in captures.values())
            progress_row = progress.get(key)
            catalog_row = catalog.get(key, {})
            if (
                slug == worker_state.get("collection")
                and key == str(worker_state.get("subreddit", "")).casefold()
                and worker_state.get("status")
                in {"fetching", "validating", "loading"}
            ):
                status = (
                    "fetching"
                    if worker_state.get("status") == "fetching"
                    else "loading"
                )
                percent = 25 if status == "fetching" else 75
                category = (
                    target_groups.get(key)
                    or catalog_row.get("classification", {}).get("category")
                    or groups.get(key)
                    or "Uncategorised"
                )
            elif key in mongo_complete:
                status = "complete"
                percent = 100
                category = (
                    (progress_row or {}).get("category")
                    or catalog_row.get("classification", {}).get("category")
                    or target_groups.get(key)
                    or groups.get(key)
                    or "Uncategorised"
                )
            elif progress_row:
                status = progress_row["status"]
                percent = progress_row["percent"]
                category = progress_row["category"]
            elif slug in {"beer", "comics", "movies", "oss"}:
                status = "loading" if present == 2 else "partial" if present else "pending"
                percent = 75 if present == 2 else 50 if present else 0
                category = (
                    target_groups.get(key)
                    or catalog_row.get("classification", {}).get("category")
                    or groups.get(key)
                    or "Uncategorised"
                )
            else:
                status = "complete" if present == 2 else "partial" if present else "pending"
                percent = 100 if present == 2 else 50 if present else 0
                category = (
                    target_groups.get(key)
                    or catalog_row.get("classification", {}).get("category")
                    or groups.get(key)
                    or "Uncategorised"
                )
            subreddits.append(
                {
                    "name": names[key],
                    "category": category,
                    "status": status,
                    "percent": percent,
                    "order": (progress_row or {}).get("order"),
                    "expected": (progress_row or {}).get(
                        "expected",
                        integer(str(catalog_row.get("archive", {}).get("posts") or 0))
                        + integer(
                            str(catalog_row.get("archive", {}).get("comments") or 0)
                        ),
                    ),
                    "raw_files": present,
                    "raw_bytes": sum(captures.values()),
                    "verification": catalog_row.get("verification", {}).get(
                        "status", ""
                    ),
                    "selected": catalog_row.get("selection", {}).get("selected")
                    is True,
                    "target_order": target_order.get(key),
                }
            )

        state = config.get("state", "unspecified")
        if state == "active" and progress:
            tracked_subreddits = [
                item for item in subreddits if item["order"] is not None
            ]
        elif state == "active" and any(item["selected"] for item in subreddits):
            tracked_subreddits = [item for item in subreddits if item["selected"]]
        else:
            tracked_subreddits = subreddits

        counts = Counter(item["status"] for item in tracked_subreddits)
        theme_percent = (
            round(
                sum(item["percent"] for item in tracked_subreddits)
                / len(tracked_subreddits)
            )
            if tracked_subreddits
            else 0
        )
        themes.append(
            {
                "slug": slug,
                "title": config.get("title", slug.replace("-", " ").title()),
                "state": state,
                "notes": config.get("notes", ""),
                "subreddits": subreddits,
                "tracked_subreddits": tracked_subreddits,
                "mongo_complete": sorted(mongo_complete),
                "percent": theme_percent,
                "complete": counts["complete"],
                "active": counts["loading"] + counts["fetching"],
                "partial": counts["partial"],
                "pending": counts["pending"],
            }
        )
    return themes, total_raw_bytes


def render(themes: list[dict], total_raw_bytes: int) -> str:
    total = sum(len(theme["tracked_subreddits"]) for theme in themes)
    unique = len(
        {
            item["name"].casefold()
            for theme in themes
            for item in theme["tracked_subreddits"]
        }
    )
    complete = sum(theme["complete"] for theme in themes)
    active = sum(theme["active"] for theme in themes)
    partial = sum(theme["partial"] for theme in themes)
    pending = sum(theme["pending"] for theme in themes)
    overall = (
        round(
            sum(
                item["percent"]
                for theme in themes
                for item in theme["tracked_subreddits"]
            )
            / total
        )
        if total
        else 0
    )
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# Reddit collection monitor",
        "",
        f"_Refreshed {generated_at} from collection files and `data/raw/`._",
        "",
        "> Open this file with **Markdown: Open Preview** (`Ctrl+Shift+V` / `Cmd+Shift+V`).",
        "",
        "## Overview",
        "",
        "| Themes | Theme/subreddit rows | Unique subreddits | Complete | Active | Partial | Pending | Raw data |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        f"| {len(themes)} | {total:,} | {unique:,} | {complete:,} | {active:,} | {partial:,} | {pending:,} | {human_bytes(total_raw_bytes)} |",
        "",
        f"**Overall coverage:** {progress_bar(overall, 20)}",
        "",
        "## Progress by theme",
        "",
        "| Theme | Workflow | Progress | Complete | Active | Partial | Pending |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for theme in themes:
        lines.append(
            f"| {markdown(theme['title'])} | `{theme['state']}` | "
            f"{progress_bar(theme['percent'])} | {theme['complete']} | "
            f"{theme['active']} | {theme['partial']} | {theme['pending']} |"
        )

    lines.extend(
        [
            "",
            "## Progress by subreddit",
            "",
            "Expand a theme below. Use VS Code search to jump to a subreddit.",
            "",
        ]
    )
    for theme in themes:
        tracked_subreddits = theme["tracked_subreddits"]
        tracked = len(tracked_subreddits)
        excluded = len(theme["subreddits"]) - tracked
        lines.extend(
            [
                "<details>",
                f"<summary><strong>{markdown(theme['title'])}</strong> — "
                f"{theme['complete']}/{tracked} complete · {theme['percent']}%</summary>",
                "",
                f"_{markdown(theme['notes'])}_",
                "",
                *(
                    [
                        f"_{excluded} discovery candidates are outside the active "
                        "reviewed scope and are not counted as pending._",
                        "",
                    ]
                    if excluded and theme["state"] == "active"
                    else []
                ),
                "| Subreddit | Category | Status | Progress | Raw size |",
                "| --- | --- | --- | ---: | ---: |",
            ]
        )
        for item in tracked_subreddits:
            lines.append(
                f"| `r/{markdown(item['name'])}` | {markdown(item['category'])} | "
                f"{status_label(item['status'])} | {progress_bar(item['percent'], 8)} | "
                f"{human_bytes(item['raw_bytes']) if item['raw_bytes'] else '—'} |"
            )
        lines.extend(["", "</details>", ""])

    lines.extend(
        [
            "---",
            "",
            "🟢 complete · 🟠 fetching/loading · 🟡 one raw file present · ⚪ pending",
            "",
        ]
    )
    return "\n".join(lines)


def render_music_dashboard(themes: list[dict]) -> str:
    theme = next(item for item in themes if item["slug"] == "music")
    subreddits = [
        item for item in theme["subreddits"] if item["order"] is not None
    ]
    pending_candidates = [
        item for item in theme["subreddits"] if item["order"] is None
    ]
    tracked = len(subreddits)
    complete = sum(item["status"] == "complete" for item in subreddits)
    remaining = tracked - complete
    completion_percent = round(complete / tracked * 100) if tracked else 0
    expected = sum(item["expected"] for item in subreddits)
    raw_bytes = sum(item["raw_bytes"] for item in subreddits)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    queue = sorted(
        (item for item in subreddits if item["status"] != "complete"),
        key=lambda item: (
            item["expected"] or 10**30,
            item["order"] or 10**9,
        ),
    )

    categories: dict[str, list[dict]] = {}
    for item in subreddits:
        categories.setdefault(item["category"], []).append(item)
    candidate_categories: dict[str, list[dict]] = {}
    for item in pending_candidates:
        candidate_categories.setdefault(item["category"], []).append(item)
    category_rows = sorted(
        [
            ("Programme", category, items)
            for category, items in categories.items()
        ]
        + [
            ("Candidate", category, items)
            for category, items in candidate_categories.items()
        ],
        key=lambda row: (row[1].casefold(), row[0]),
    )

    lines = [
        "# Music subreddit collection dashboard",
        "",
        f"_Refreshed {generated_at} from MongoDB, `progress.md`, and `data/raw/`._",
        "",
        "> Open with **Markdown: Open Preview** (`Ctrl+Shift+V` / `Cmd+Shift+V`). "
        "The tmux job refreshes this file after every successful load.",
        "",
        "## Status",
        "",
        "| Programme | Complete | Remaining | Expected records | Raw data | Workflow |",
        "| ---: | ---: | ---: | ---: | ---: | --- |",
        f"| {tracked} | {complete} | {remaining} | {expected:,} | "
        f"{human_bytes(raw_bytes)} | `{theme['state']}` |",
        "",
        f"**Subreddit completion:** {progress_bar(completion_percent, 24)}",
        "",
        "- tmux session: `reddit_music_resume`",
        "- runtime log: `data/logs/music-resume.log`",
        "- destination: MongoDB `localhost:27019`, database `reddit`",
        "- queue policy: one worker, smallest expected capture first",
        "",
        "## Next in queue",
        "",
        "| # | Subreddit | Category | Expected records | Existing raw |",
        "| ---: | --- | --- | ---: | ---: |",
    ]
    for position, item in enumerate(queue[:15], 1):
        lines.append(
            f"| {position} | `r/{markdown(item['name'])}` | "
            f"{markdown(item['category'])} | {item['expected']:,} | "
            f"{item['raw_files']}/2 files |"
        )
    if not queue:
        lines.append("| — | Queue complete | — | — | — |")

    lines.extend(
        [
            "",
            "## Pending candidates",
            "",
            "These catalogue entries are outside the authorised 130-subreddit "
            "programme and are not in its acquisition queue.",
            "",
            "| Subreddit | Category | Verification | Expected archive records | Selection |",
            "| --- | --- | --- | ---: | --- |",
        ]
    )
    for item in sorted(pending_candidates, key=lambda row: row["name"].casefold()):
        selection = "Selected" if item["selected"] else "Pending review"
        lines.append(
            f"| `r/{markdown(item['name'])}` | {markdown(item['category'])} | "
            f"{markdown(item['verification'] or 'uncatalogued')} | "
            f"{item['expected']:,} | {selection} |"
        )
    if not pending_candidates:
        lines.append("| — | — | — | — | No additional candidates |")

    lines.extend(
        [
            "",
            "## Progress by category",
            "",
            "| Category | Scope | Complete | Tracked | Progress | Expected records | Raw data |",
            "| --- | --- | ---: | ---: | --- | ---: | ---: |",
        ]
    )
    for scope, category, items in category_rows:
        category_complete = sum(item["status"] == "complete" for item in items)
        category_percent = round(category_complete / len(items) * 100)
        lines.append(
            f"| {markdown(category)} | {scope} | {category_complete} | "
            f"{len(items)} | "
            f"{progress_bar(category_percent, 10)} | "
            f"{sum(item['expected'] for item in items):,} | "
            f"{human_bytes(sum(item['raw_bytes'] for item in items))} |"
        )

    lines.extend(
        [
            "",
            "## All subreddits",
            "",
            "Expand a category below. Use VS Code search to jump directly to a subreddit.",
            "",
        ]
    )
    for scope, category, items in category_rows:
        items.sort(key=lambda item: item["order"] or 10**9)
        category_complete = sum(item["status"] == "complete" for item in items)
        scope_suffix = "" if scope == "Programme" else " · candidate"
        lines.extend(
            [
                "<details>",
                f"<summary><strong>{markdown(category)}</strong> — "
                f"{category_complete}/{len(items)} complete{scope_suffix}</summary>",
                "",
                "| Subreddit | Status | Expected records | Raw files | Raw size |",
                "| --- | --- | ---: | ---: | ---: |",
            ]
        )
        for item in items:
            status = (
                status_label(item["status"])
                if scope == "Programme"
                else "🟠 Selected"
                if item["selected"]
                else "⚪ Pending review"
            )
            lines.append(
                f"| `r/{markdown(item['name'])}` | {status} | "
                f"{item['expected']:,} | {item['raw_files']}/2 | "
                f"{human_bytes(item['raw_bytes']) if item['raw_bytes'] else '—'} |"
            )
        lines.extend(["", "</details>", ""])

    lines.extend(
        [
            "---",
            "",
            "🟢 present in both MongoDB collections · 🟠 fetching/loading · "
            "🟡 one raw file present · ⚪ pending",
            "",
        ]
    )
    return "\n".join(lines)


def render_linux_dashboard(themes: list[dict]) -> str:
    theme = next(item for item in themes if item["slug"] == "linux")
    panel = [item for item in theme["subreddits"] if item["selected"]]
    acquisition_targets = [item for item in panel if item["target_order"] is not None]
    target_keys = {item["name"].casefold() for item in acquisition_targets}
    complete = sum(item["status"] == "complete" for item in panel)
    partial = sum(item["status"] == "partial" for item in acquisition_targets)
    remaining = len(panel) - complete
    completion_percent = round(complete / len(panel) * 100) if panel else 0
    expected = sum(item["expected"] for item in panel)
    raw_bytes = sum(item["raw_bytes"] for item in acquisition_targets)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    queue = sorted(
        (
            item
            for item in acquisition_targets
            if item["status"] != "complete"
        ),
        key=lambda item: (
            item["expected"] or 10**30,
            item["target_order"] or 10**9,
        ),
    )
    categories: dict[str, list[dict]] = {}
    for item in panel:
        categories.setdefault(item["category"], []).append(item)
    panel_existing = [
        item
        for item in panel
        if item["name"].casefold() in theme["mongo_complete"]
        and item["name"].casefold() not in target_keys
    ]
    excluded = [
        item
        for item in theme["subreddits"]
        if not item["selected"]
    ]

    lines = [
        "# Linux subreddit collection dashboard",
        "",
        f"_Refreshed {generated_at} from MongoDB, the Linux catalogue, "
        "`targets.txt`, and `data/raw/`._",
        "",
        "> Open with **Markdown: Open Preview** (`Ctrl+Shift+V` / `Cmd+Shift+V`). "
        "The tmux worker refreshes this file after every successful load.",
        "",
        "## Status",
        "",
        "| Panel N | Available | Partial acquisition | Remaining | Expected records | New raw data | Workflow |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        f"| {len(panel)} | {complete} | {partial} | {remaining} | "
        f"{expected:,} | {human_bytes(raw_bytes)} | `{theme['state']}` |",
        "",
        f"**Panel availability:** {progress_bar(completion_percent, 24)}",
        "",
        "- tmux session: `reddit_linux_collection`",
        "- runtime log: `data/logs/linux-collection.log`",
        "- destination: MongoDB `localhost:27017`, database `reddit`",
        "- queue policy: one low-priority worker, smallest expected capture first",
        "- music protection: Linux API requests pause while the music worker fetches",
        "",
        "## Next in queue",
        "",
        "| # | Subreddit | Category | Expected records | Existing raw |",
        "| ---: | --- | --- | ---: | ---: |",
    ]
    for position, item in enumerate(queue[:15], start=1):
        lines.append(
            f"| {position} | `r/{markdown(item['name'])}` | "
            f"{markdown(item['category'])} | {item['expected']:,} | "
            f"{item['raw_files']}/2 files |"
        )
    if not queue:
        lines.append("| — | Queue complete | — | — | — |")

    lines.extend(
        [
            "",
            "## Progress by category",
            "",
            "| Category | Complete | Tracked | Progress | Expected records | Raw data |",
            "| --- | ---: | ---: | --- | ---: | ---: |",
        ]
    )
    for category, items in sorted(categories.items(), key=lambda row: row[0].casefold()):
        category_complete = sum(item["status"] == "complete" for item in items)
        category_percent = round(category_complete / len(items) * 100)
        lines.append(
            f"| {markdown(category)} | {category_complete} | {len(items)} | "
            f"{progress_bar(category_percent, 10)} | "
            f"{sum(item['expected'] for item in items):,} | "
            f"{human_bytes(sum(item['raw_bytes'] for item in items))} |"
        )

    lines.extend(
        [
            "",
            "## Existing MongoDB holdings",
            "",
            f"{len(panel_existing)} Linux panel members were present in both "
            "MongoDB collections before the 93-target acquisition queue "
            "started.",
            "",
            "| Subreddit | Panel status | MongoDB status | Acquisition action |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in sorted(panel_existing, key=lambda row: row["name"].casefold()):
        lines.append(
            f"| `r/{markdown(item['name'])}` | Included in N={len(panel)} | "
            "Present in both collections | Skip |"
        )
    lines.extend(
        [
            "",
            f"_Excluded unresolved candidates: {len(excluded)} "
            "(missing or restricted at catalogue verification)._",
            "",
            "## All panel communities",
            "",
            "Expand a category below. Use VS Code search to jump directly to a subreddit.",
            "",
        ]
    )
    for category, items in sorted(categories.items(), key=lambda row: row[0].casefold()):
        items.sort(key=lambda item: item["target_order"] or 10**9)
        category_complete = sum(item["status"] == "complete" for item in items)
        lines.extend(
            [
                "<details>",
                f"<summary><strong>{markdown(category)}</strong> — "
                f"{category_complete}/{len(items)} complete</summary>",
                "",
                "| Subreddit | Status | Expected records | Raw files | Raw size |",
                "| --- | --- | ---: | ---: | ---: |",
            ]
        )
        for item in items:
            lines.append(
                f"| `r/{markdown(item['name'])}` | {status_label(item['status'])} | "
                f"{item['expected']:,} | {item['raw_files']}/2 | "
                f"{human_bytes(item['raw_bytes']) if item['raw_bytes'] else '—'} |"
            )
        lines.extend(["", "</details>", ""])

    lines.extend(
        [
            "---",
            "",
            "🟢 present in both MongoDB collections · 🟡 one raw file present · "
            "⚪ pending acquisition",
            "",
        ]
    )
    return "\n".join(lines)


def render_beer_dashboard(themes: list[dict]) -> str:
    theme = next(item for item in themes if item["slug"] == "beer")
    panel = [
        item for item in theme["subreddits"] if item["target_order"] is not None
    ]
    excluded = [item for item in theme["subreddits"] if not item["selected"]]
    complete = sum(item["status"] == "complete" for item in panel)
    active = sum(item["status"] in {"fetching", "loading"} for item in panel)
    partial = sum(item["status"] == "partial" for item in panel)
    remaining = len(panel) - complete
    completion_percent = round(complete / len(panel) * 100) if panel else 0
    expected = sum(item["expected"] for item in panel)
    raw_bytes = sum(item["raw_bytes"] for item in panel)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    queue = sorted(
        (item for item in panel if item["status"] != "complete"),
        key=lambda item: (
            item["expected"] or 10**30,
            item["target_order"] or 10**9,
        ),
    )
    categories: dict[str, list[dict]] = {}
    for item in panel:
        categories.setdefault(item["category"], []).append(item)
    excluded_by_verification = Counter(
        item["verification"] or "uncatalogued" for item in excluded
    )

    lines = [
        "# Beer subreddit collection dashboard",
        "",
        f"_Refreshed {generated_at} from MongoDB, the beer catalogue, "
        "`targets.txt`, and `data/raw/`._",
        "",
        "> Open with **Markdown: Open Preview** (`Ctrl+Shift+V` / `Cmd+Shift+V`). "
        "The tmux worker refreshes this file after every successful load.",
        "",
        "## Status",
        "",
        "| Panel | Complete | Active capture/load | Partial raw | Remaining | Expected records | Raw data | Workflow |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        f"| {len(panel)} | {complete} | {active} | {partial} | {remaining} | "
        f"{expected:,} | {human_bytes(raw_bytes)} | `{theme['state']}` |",
        "",
        f"**MongoDB completion:** {progress_bar(completion_percent, 24)}",
        "",
        "- tmux session: `reddit_beer_collection`",
        "- runtime log: `data/logs/beer-collection.log`",
        "- destination: MongoDB `localhost:27019`, database `reddit`",
        "- queue policy: one low-priority worker, smallest expected capture first",
        "- music protection: beer API requests pause while the music worker fetches",
        "- completion gate: both MongoDB collections plus 64 decodable raw files",
        "",
        "## Next in queue",
        "",
        "| # | Subreddit | Stratum | Status | Expected records | Existing raw |",
        "| ---: | --- | --- | --- | ---: | ---: |",
    ]
    for position, item in enumerate(queue[:15], start=1):
        lines.append(
            f"| {position} | `r/{markdown(item['name'])}` | "
            f"{markdown(item['category'])} | {status_label(item['status'])} | "
            f"{item['expected']:,} | {item['raw_files']}/2 files |"
        )
    if not queue:
        lines.append("| — | Queue complete | — | — | — | — |")

    lines.extend(
        [
            "",
            "## Progress by stratum",
            "",
            "| Stratum | Complete | Tracked | Progress | Expected records | Raw data |",
            "| --- | ---: | ---: | --- | ---: | ---: |",
        ]
    )
    for category, items in sorted(categories.items(), key=lambda row: row[0].casefold()):
        category_complete = sum(item["status"] == "complete" for item in items)
        category_percent = round(category_complete / len(items) * 100)
        lines.append(
            f"| {markdown(category)} | {category_complete} | {len(items)} | "
            f"{progress_bar(category_percent, 10)} | "
            f"{sum(item['expected'] for item in items):,} | "
            f"{human_bytes(sum(item['raw_bytes'] for item in items))} |"
        )

    lines.extend(
        [
            "",
            "## Selection boundary",
            "",
            f"The acquisition panel contains {len(panel)} reviewed communities; "
            f"{len(excluded)} catalogue candidates are outside it.",
            "",
            "| Excluded catalogue status | Communities |",
            "| --- | ---: |",
        ]
    )
    for verification, count in sorted(excluded_by_verification.items()):
        lines.append(f"| {markdown(verification)} | {count} |")

    lines.extend(
        [
            "",
            "Cider and mead are included as an adjacent-fermentation comparator "
            "stratum and should remain separate in downstream analysis.",
            "",
            "## All panel communities",
            "",
            "Expand a stratum below. Use VS Code search to jump directly to a subreddit.",
            "",
        ]
    )
    for category, items in sorted(categories.items(), key=lambda row: row[0].casefold()):
        items.sort(key=lambda item: item["target_order"] or 10**9)
        category_complete = sum(item["status"] == "complete" for item in items)
        lines.extend(
            [
                "<details>",
                f"<summary><strong>{markdown(category)}</strong> — "
                f"{category_complete}/{len(items)} complete</summary>",
                "",
                "| Subreddit | Status | Expected records | Raw files | Raw size |",
                "| --- | --- | ---: | ---: | ---: |",
            ]
        )
        for item in items:
            lines.append(
                f"| `r/{markdown(item['name'])}` | {status_label(item['status'])} | "
                f"{item['expected']:,} | {item['raw_files']}/2 | "
                f"{human_bytes(item['raw_bytes']) if item['raw_bytes'] else '—'} |"
            )
        lines.extend(["", "</details>", ""])

    lines.extend(
        [
            "---",
            "",
            "🟢 present in both MongoDB collections · 🟠 two raw captures awaiting/under load · "
            "🟡 one raw file present · ⚪ pending",
            "",
        ]
    )
    return "\n".join(lines)


def render_comics_movies_dashboard(themes: list[dict]) -> str:
    programme = [
        next(item for item in themes if item["slug"] == slug)
        for slug in ("comics", "movies")
    ]
    panels = {
        theme["slug"]: [
            item
            for item in theme["subreddits"]
            if item["target_order"] is not None
        ]
        for theme in programme
    }
    all_targets = [
        {**item, "collection": theme["slug"], "theme_title": theme["title"]}
        for theme in programme
        for item in panels[theme["slug"]]
    ]
    queue = sorted(
        (item for item in all_targets if item["status"] != "complete"),
        key=lambda item: (
            item["expected"],
            0 if item["collection"] == "comics" else 1,
            item["target_order"] or 10**9,
        ),
    )
    worker_state = read_comics_movies_state()
    complete = sum(item["status"] == "complete" for item in all_targets)
    active = sum(
        item["status"] in {"fetching", "loading"} for item in all_targets
    )
    partial = sum(item["status"] == "partial" for item in all_targets)
    remaining = len(all_targets) - complete
    completion_percent = (
        round(complete / len(all_targets) * 100) if all_targets else 0
    )
    expected = sum(item["expected"] for item in all_targets)
    raw_bytes = sum(item["raw_bytes"] for item in all_targets)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    current_status = str(worker_state.get("status", "not started"))
    current_subreddit = worker_state.get("subreddit")
    current_collection = worker_state.get("collection")
    if current_subreddit and current_collection:
        current = (
            f"`{markdown(current_status)}` — {markdown(current_collection)} "
            f"`r/{markdown(current_subreddit)}` "
            f"({worker_state.get('position', '?')}/{worker_state.get('queued', '?')})"
        )
    else:
        current = f"`{markdown(current_status)}`"

    lines = [
        "# Comics and movies collection dashboard",
        "",
        f"_Refreshed {generated_at} from MongoDB, the two reviewed catalogues, "
        "`targets.txt`, worker state, and `data/raw/`._",
        "",
        "> Open with **Markdown: Open Preview** (`Ctrl+Shift+V` / `Cmd+Shift+V`). "
        "The shared tmux worker refreshes this file at every fetch, validation, "
        "and load transition.",
        "",
        "## Shared programme",
        "",
        "| Targets | Complete | Active | Partial raw | Remaining | Expected records | Raw data |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        f"| {len(all_targets)} | {complete} | {active} | {partial} | "
        f"{remaining} | {expected:,} | {human_bytes(raw_bytes)} |",
        "",
        f"**MongoDB completion:** {progress_bar(completion_percent, 24)}",
        "",
        f"- worker: {current}",
        "- tmux session: `reddit_comics_movies`",
        "- runtime log: `data/logs/comics-movies-collection.log`",
        "- destination: MongoDB `localhost:27019`, database `reddit`",
        "- payload: submissions and comments",
        "- queue policy: one low-priority worker, globally smallest expected capture first",
        "- completion gate: both MongoDB collections and two decodable raw files per target",
        "",
        "## Track status",
        "",
        "| Track | Panel | Complete | Active | Partial | Remaining | Expected records | Raw data | Workflow |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for theme in programme:
        panel = panels[theme["slug"]]
        track_complete = sum(item["status"] == "complete" for item in panel)
        track_active = sum(
            item["status"] in {"fetching", "loading"} for item in panel
        )
        track_partial = sum(item["status"] == "partial" for item in panel)
        lines.append(
            f"| {markdown(theme['title'])} | {len(panel)} | {track_complete} | "
            f"{track_active} | {track_partial} | {len(panel) - track_complete} | "
            f"{sum(item['expected'] for item in panel):,} | "
            f"{human_bytes(sum(item['raw_bytes'] for item in panel))} | "
            f"`{theme['state']}` |"
        )

    lines.extend(
        [
            "",
            "## Next in shared queue",
            "",
            "| # | Track | Subreddit | Stratum | Status | Expected records | Existing raw |",
            "| ---: | --- | --- | --- | --- | ---: | ---: |",
        ]
    )
    for position, item in enumerate(queue[:20], start=1):
        lines.append(
            f"| {position} | {markdown(item['theme_title'])} | "
            f"`r/{markdown(item['name'])}` | {markdown(item['category'])} | "
            f"{status_label(item['status'])} | {item['expected']:,} | "
            f"{item['raw_files']}/2 files |"
        )
    if not queue:
        lines.append("| — | — | Queue complete | — | — | — | — |")

    for theme in programme:
        panel = panels[theme["slug"]]
        categories: dict[str, list[dict]] = {}
        for item in panel:
            categories.setdefault(item["category"], []).append(item)
        lines.extend(
            [
                "",
                f"## {markdown(theme['title'])} by stratum",
                "",
                "| Stratum | Complete | Tracked | Progress | Expected records | Raw data |",
                "| --- | ---: | ---: | --- | ---: | ---: |",
            ]
        )
        for category, items in sorted(
            categories.items(), key=lambda row: row[0].casefold()
        ):
            category_complete = sum(
                item["status"] == "complete" for item in items
            )
            category_percent = round(category_complete / len(items) * 100)
            lines.append(
                f"| {markdown(category)} | {category_complete} | {len(items)} | "
                f"{progress_bar(category_percent, 10)} | "
                f"{sum(item['expected'] for item in items):,} | "
                f"{human_bytes(sum(item['raw_bytes'] for item in items))} |"
            )

        lines.extend(
            [
                "",
                f"### All {markdown(theme['title'].lower())} targets",
                "",
            ]
        )
        for category, items in sorted(
            categories.items(), key=lambda row: row[0].casefold()
        ):
            items.sort(key=lambda item: item["target_order"] or 10**9)
            category_complete = sum(
                item["status"] == "complete" for item in items
            )
            lines.extend(
                [
                    "<details>",
                    f"<summary><strong>{markdown(category)}</strong> — "
                    f"{category_complete}/{len(items)} complete</summary>",
                    "",
                    "| Subreddit | Status | Expected records | Raw files | Raw size |",
                    "| --- | --- | ---: | ---: | ---: |",
                ]
            )
            for item in items:
                lines.append(
                    f"| `r/{markdown(item['name'])}` | "
                    f"{status_label(item['status'])} | {item['expected']:,} | "
                    f"{item['raw_files']}/2 | "
                    f"{human_bytes(item['raw_bytes']) if item['raw_bytes'] else '—'} |"
                )
            lines.extend(["", "</details>", ""])

    lines.extend(
        [
            "---",
            "",
            "🟢 present in both MongoDB collections · 🟠 fetching/validating/loading · "
            "🟡 one raw file present · ⚪ pending",
            "",
        ]
    )
    return "\n".join(lines)


def render_comics_movies_track_dashboard(
    themes: list[dict], slug: str
) -> str:
    theme = next(item for item in themes if item["slug"] == slug)
    panel = [
        item for item in theme["subreddits"] if item["target_order"] is not None
    ]
    queue = sorted(
        (item for item in panel if item["status"] != "complete"),
        key=lambda item: (
            item["expected"],
            item["target_order"] or 10**9,
        ),
    )
    excluded = [item for item in theme["subreddits"] if not item["selected"]]
    excluded_by_verification = Counter(
        item["verification"] or "uncatalogued" for item in excluded
    )
    complete = sum(item["status"] == "complete" for item in panel)
    active = sum(item["status"] in {"fetching", "loading"} for item in panel)
    partial = sum(item["status"] == "partial" for item in panel)
    remaining = len(panel) - complete
    completion_percent = round(complete / len(panel) * 100) if panel else 0
    expected = sum(item["expected"] for item in panel)
    raw_bytes = sum(item["raw_bytes"] for item in panel)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    worker_state = read_comics_movies_state()
    current_status = str(worker_state.get("status", "not started"))
    current_subreddit = worker_state.get("subreddit")
    current_collection = worker_state.get("collection")
    if current_subreddit and current_collection:
        current = (
            f"`{markdown(current_status)}` — {markdown(current_collection)} "
            f"`r/{markdown(current_subreddit)}` "
            f"({worker_state.get('position', '?')}/{worker_state.get('queued', '?')})"
        )
    else:
        current = f"`{markdown(current_status)}`"

    categories: dict[str, list[dict]] = {}
    for item in panel:
        categories.setdefault(item["category"], []).append(item)

    title = markdown(theme["title"])
    lines = [
        f"# {title} subreddit collection dashboard",
        "",
        f"_Refreshed {generated_at} from MongoDB, the reviewed {slug} catalogue, "
        "`targets.txt`, shared-worker state, and `data/raw/`._",
        "",
        "> Open with **Markdown: Open Preview** (`Ctrl+Shift+V` / `Cmd+Shift+V`). "
        "The shared tmux worker refreshes this file at every fetch, validation, "
        "and load transition.",
        "",
        "## Status",
        "",
        "| Panel | Complete | Active | Partial raw | Remaining | Expected records | Raw data | Workflow |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        f"| {len(panel)} | {complete} | {active} | {partial} | {remaining} | "
        f"{expected:,} | {human_bytes(raw_bytes)} | `{theme['state']}` |",
        "",
        f"**MongoDB completion:** {progress_bar(completion_percent, 24)}",
        "",
        f"- shared worker: {current}",
        "- tmux session: `reddit_comics_movies`",
        "- runtime log: `data/logs/comics-movies-collection.log`",
        "- destination: MongoDB `localhost:27019`, database `reddit`",
        "- payload: submissions and comments",
        "- queue policy: one low-priority worker, globally smallest expected capture first",
        "- completion gate: both MongoDB collections and two decodable raw files per target",
        "- combined view: [`COMICS_MOVIES_PROGRESS.md`](../../COMICS_MOVIES_PROGRESS.md)",
        "",
        f"## Next {markdown(slug)} targets",
        "",
        "The shared queue may interleave targets from the other collection.",
        "",
        "| # | Subreddit | Stratum | Status | Expected records | Existing raw |",
        "| ---: | --- | --- | --- | ---: | ---: |",
    ]
    for position, item in enumerate(queue[:20], start=1):
        lines.append(
            f"| {position} | `r/{markdown(item['name'])}` | "
            f"{markdown(item['category'])} | {status_label(item['status'])} | "
            f"{item['expected']:,} | {item['raw_files']}/2 files |"
        )
    if not queue:
        lines.append("| — | Queue complete | — | — | — | — |")

    lines.extend(
        [
            "",
            "## Progress by stratum",
            "",
            "| Stratum | Complete | Tracked | Progress | Expected records | Raw data |",
            "| --- | ---: | ---: | --- | ---: | ---: |",
        ]
    )
    for category, items in sorted(
        categories.items(), key=lambda row: row[0].casefold()
    ):
        category_complete = sum(item["status"] == "complete" for item in items)
        category_percent = round(category_complete / len(items) * 100)
        lines.append(
            f"| {markdown(category)} | {category_complete} | {len(items)} | "
            f"{progress_bar(category_percent, 10)} | "
            f"{sum(item['expected'] for item in items):,} | "
            f"{human_bytes(sum(item['raw_bytes'] for item in items))} |"
        )

    lines.extend(
        [
            "",
            "## Selection boundary",
            "",
            f"The acquisition panel contains {len(panel)} reviewed communities; "
            f"{len(excluded)} catalogue candidates are outside it.",
            "",
            "| Excluded catalogue status | Communities |",
            "| --- | ---: |",
        ]
    )
    for verification, count in sorted(excluded_by_verification.items()):
        lines.append(f"| {markdown(verification)} | {count} |")

    lines.extend(
        [
            "",
            "## All panel communities",
            "",
            "Expand a stratum below. Use VS Code search to jump directly to a subreddit.",
            "",
        ]
    )
    for category, items in sorted(
        categories.items(), key=lambda row: row[0].casefold()
    ):
        items.sort(key=lambda item: item["target_order"] or 10**9)
        category_complete = sum(item["status"] == "complete" for item in items)
        lines.extend(
            [
                "<details>",
                f"<summary><strong>{markdown(category)}</strong> — "
                f"{category_complete}/{len(items)} complete</summary>",
                "",
                "| Subreddit | Status | Expected records | Raw files | Raw size |",
                "| --- | --- | ---: | ---: | ---: |",
            ]
        )
        for item in items:
            lines.append(
                f"| `r/{markdown(item['name'])}` | {status_label(item['status'])} | "
                f"{item['expected']:,} | {item['raw_files']}/2 | "
                f"{human_bytes(item['raw_bytes']) if item['raw_bytes'] else '—'} |"
            )
        lines.extend(["", "</details>", ""])

    lines.extend(
        [
            "---",
            "",
            "🟢 present in both MongoDB collections · 🟠 fetching/validating/loading · "
            "🟡 one raw file present · ⚪ pending",
            "",
        ]
    )
    return "\n".join(lines)


def render_oss_dashboard(themes: list[dict]) -> str:
    theme = next(item for item in themes if item["slug"] == "oss")
    panel = [item for item in theme["subreddits"] if item["selected"]]
    excluded = [item for item in theme["subreddits"] if not item["selected"]]
    complete = sum(item["status"] == "complete" for item in panel)
    active = sum(item["status"] in {"fetching", "loading"} for item in panel)
    partial = sum(item["status"] == "partial" for item in panel)
    remaining = len(panel) - complete
    completion_percent = round(complete / len(panel) * 100) if panel else 0
    expected = sum(item["expected"] for item in panel)
    raw_bytes = sum(item["raw_bytes"] for item in panel)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    worker_state = read_oss_state()
    queue = sorted(
        (item for item in panel if item["status"] != "complete"),
        key=lambda item: (
            item["expected"] or 10**30,
            item["target_order"] or 10**9,
        ),
    )

    categories: dict[str, list[dict]] = {}
    for item in panel:
        categories.setdefault(item["category"], []).append(item)

    current_status = str(worker_state.get("status", "not started"))
    current_name = str(worker_state.get("subreddit", ""))
    current_activity = current_status
    if current_name and current_status in {"fetching", "validating", "loading"}:
        current_activity = f"{current_status} r/{current_name}"
    updated_at = str(worker_state.get("updated_at", "not yet recorded"))

    lines = [
        "# Open-source software subreddit collection dashboard",
        "",
        f"_Refreshed {generated_at} from the OSS worker state, catalogue, "
        "`targets.txt`, MongoDB evidence, and `data/raw/`._",
        "",
        "> Open with **Markdown: Open Preview** (`Ctrl+Shift+V` / `Cmd+Shift+V`). "
        "The tmux worker refreshes this file at each acquisition stage.",
        "",
        "## Status",
        "",
        "| Panel N | Available in MongoDB | Active/staged | Partial raw | Remaining | Expected records | Raw data | Workflow |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        f"| {len(panel)} | {complete} | {active} | {partial} | {remaining} | "
        f"{expected:,} | {human_bytes(raw_bytes)} | `{theme['state']}` |",
        "",
        f"**MongoDB availability:** {progress_bar(completion_percent, 24)}",
        "",
        f"- worker activity: `{markdown(current_activity)}`",
        f"- worker state updated: `{markdown(updated_at)}`",
        "- tmux session: `reddit_oss_collection`",
        "- runtime log: `data/logs/oss-collection.log`",
        "- destination: MongoDB `localhost:27017`, database `reddit`",
        "- queue policy: one low-priority worker, smallest expected capture first",
        "- API priority: yields while the comics/movies worker is fetching",
        "",
        "## Next in queue",
        "",
        "| # | Subreddit | Category | Expected records | Existing raw |",
        "| ---: | --- | --- | ---: | ---: |",
    ]
    for position, item in enumerate(queue[:15], start=1):
        lines.append(
            f"| {position} | `r/{markdown(item['name'])}` | "
            f"{markdown(item['category'])} | {item['expected']:,} | "
            f"{item['raw_files']}/2 files |"
        )
    if not queue:
        lines.append("| — | Queue complete | — | — | — |")

    lines.extend(
        [
            "",
            "## Progress by category",
            "",
            "| Category | Available | Tracked | Progress | Expected records | Raw data |",
            "| --- | ---: | ---: | --- | ---: | ---: |",
        ]
    )
    for category, items in sorted(categories.items(), key=lambda row: row[0].casefold()):
        category_complete = sum(item["status"] == "complete" for item in items)
        category_percent = round(category_complete / len(items) * 100)
        lines.append(
            f"| {markdown(category)} | {category_complete} | {len(items)} | "
            f"{progress_bar(category_percent, 10)} | "
            f"{sum(item['expected'] for item in items):,} | "
            f"{human_bytes(sum(item['raw_bytes'] for item in items))} |"
        )

    unresolved = Counter(item["verification"] or "uncatalogued" for item in excluded)
    unresolved_summary = ", ".join(
        f"{count} {status}" for status, count in sorted(unresolved.items())
    )
    lines.extend(
        [
            "",
            "## Selection boundary",
            "",
            f"The active census contains all {len(panel)} catalogue-verified "
            f"communities. Excluded unresolved candidates: {len(excluded)} "
            f"({unresolved_summary}).",
            "",
            "## All panel communities",
            "",
            "Expand a category below. Use VS Code search to jump directly to a subreddit.",
            "",
        ]
    )
    for category, items in sorted(categories.items(), key=lambda row: row[0].casefold()):
        items.sort(key=lambda item: item["target_order"] or 10**9)
        category_complete = sum(item["status"] == "complete" for item in items)
        lines.extend(
            [
                "<details>",
                f"<summary><strong>{markdown(category)}</strong> — "
                f"{category_complete}/{len(items)} available</summary>",
                "",
                "| Subreddit | Status | Expected records | Raw files | Raw size |",
                "| --- | --- | ---: | ---: | ---: |",
            ]
        )
        for item in items:
            lines.append(
                f"| `r/{markdown(item['name'])}` | {status_label(item['status'])} | "
                f"{item['expected']:,} | {item['raw_files']}/2 | "
                f"{human_bytes(item['raw_bytes']) if item['raw_bytes'] else '—'} |"
            )
        lines.extend(["", "</details>", ""])

    lines.extend(
        [
            "---",
            "",
            "🟢 present in both MongoDB collections · 🟠 fetching/validating/loading · "
            "🟡 one raw file present · ⚪ pending",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)
    print(f"Wrote {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--music-output",
        type=Path,
        default=MUSIC_DIR / "dashboard.md",
    )
    parser.add_argument(
        "--linux-output",
        type=Path,
        default=LINUX_DIR / "dashboard.md",
    )
    parser.add_argument(
        "--beer-output",
        type=Path,
        default=BEER_DIR / "dashboard.md",
    )
    parser.add_argument(
        "--comics-movies-output",
        type=Path,
        default=DEFAULT_COMICS_MOVIES_OUTPUT,
    )
    parser.add_argument(
        "--comics-output",
        type=Path,
        default=COMICS_DIR / "dashboard.md",
    )
    parser.add_argument(
        "--movies-output",
        type=Path,
        default=MOVIES_DIR / "dashboard.md",
    )
    parser.add_argument(
        "--oss-output",
        type=Path,
        default=OSS_DIR / "dashboard.md",
    )
    parser.add_argument(
        "--only-oss",
        action="store_true",
        help="refresh only the OSS dashboard without querying other collections",
    )
    args = parser.parse_args()
    themes, total_raw_bytes = collect_state("oss" if args.only_oss else None)
    output = args.output.resolve()
    music_output = args.music_output.resolve()
    linux_output = args.linux_output.resolve()
    beer_output = args.beer_output.resolve()
    comics_movies_output = args.comics_movies_output.resolve()
    comics_output = args.comics_output.resolve()
    movies_output = args.movies_output.resolve()
    oss_output = args.oss_output.resolve()
    if args.only_oss:
        write_report(oss_output, render_oss_dashboard(themes))
        return
    write_report(output, render(themes, total_raw_bytes))
    write_report(music_output, render_music_dashboard(themes))
    write_report(linux_output, render_linux_dashboard(themes))
    write_report(beer_output, render_beer_dashboard(themes))
    write_report(
        comics_movies_output,
        render_comics_movies_dashboard(themes),
    )
    write_report(
        comics_output,
        render_comics_movies_track_dashboard(themes, "comics"),
    )
    write_report(
        movies_output,
        render_comics_movies_track_dashboard(themes, "movies"),
    )
    write_report(oss_output, render_oss_dashboard(themes))


if __name__ == "__main__":
    main()
