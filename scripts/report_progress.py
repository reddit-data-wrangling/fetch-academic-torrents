"""Generate a collection-progress dashboard for VS Code Markdown Preview."""

from __future__ import annotations

import argparse
import json
import re
import tomllib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COLLECTIONS_DIR = ROOT / "collections"
RAW_DIR = ROOT / "data" / "raw"
DEFAULT_OUTPUT = ROOT / "COLLECTION_PROGRESS.md"


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
        }
    return rows


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


def collect_state() -> tuple[list[dict], int]:
    raw, total_raw_bytes = raw_files()
    themes: list[dict] = []

    for config_path in sorted(COLLECTIONS_DIR.glob("*/collection.toml")):
        directory = config_path.parent
        slug = directory.name
        with config_path.open("rb") as stream:
            config = tomllib.load(stream)
        candidates, groups = read_names(directory / "subreddits.txt")
        catalog = read_catalog(directory / "catalog.json")
        progress = read_progress(directory / "progress.md")

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
            if progress_row:
                status = progress_row["status"]
                percent = progress_row["percent"]
                category = progress_row["category"]
            else:
                status = "complete" if present == 2 else "partial" if present else "pending"
                percent = 100 if present == 2 else 50 if present else 0
                category = (
                    catalog_row.get("classification", {}).get("category")
                    or groups.get(key)
                    or "Uncategorised"
                )
            subreddits.append(
                {
                    "name": names[key],
                    "category": category,
                    "status": status,
                    "percent": percent,
                    "raw_bytes": sum(captures.values()),
                }
            )

        counts = Counter(item["status"] for item in subreddits)
        theme_percent = (
            round(sum(item["percent"] for item in subreddits) / len(subreddits))
            if subreddits
            else 0
        )
        themes.append(
            {
                "slug": slug,
                "title": config.get("title", slug.replace("-", " ").title()),
                "state": config.get("state", "unspecified"),
                "notes": config.get("notes", ""),
                "subreddits": subreddits,
                "percent": theme_percent,
                "complete": counts["complete"],
                "active": counts["loading"] + counts["fetching"],
                "partial": counts["partial"],
                "pending": counts["pending"],
            }
        )
    return themes, total_raw_bytes


def render() -> str:
    themes, total_raw_bytes = collect_state()
    total = sum(len(theme["subreddits"]) for theme in themes)
    unique = len(
        {
            item["name"].casefold()
            for theme in themes
            for item in theme["subreddits"]
        }
    )
    complete = sum(theme["complete"] for theme in themes)
    active = sum(theme["active"] for theme in themes)
    partial = sum(theme["partial"] for theme in themes)
    pending = sum(theme["pending"] for theme in themes)
    overall = (
        round(
            sum(item["percent"] for theme in themes for item in theme["subreddits"])
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
        tracked = len(theme["subreddits"])
        lines.extend(
            [
                "<details>",
                f"<summary><strong>{markdown(theme['title'])}</strong> — "
                f"{theme['complete']}/{tracked} complete · {theme['percent']}%</summary>",
                "",
                f"_{markdown(theme['notes'])}_",
                "",
                "| Subreddit | Category | Status | Progress | Raw size |",
                "| --- | --- | --- | ---: | ---: |",
            ]
        )
        for item in theme["subreddits"]:
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(render(), encoding="utf-8")
    temporary.replace(output)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
