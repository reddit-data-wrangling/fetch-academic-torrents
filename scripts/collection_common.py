"""Shared helpers for domain collection scripts and JSON metadata."""

from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
COLLECTIONS_DIR = ROOT / "collections"

CATALOG_FIELDS = [
    "subreddit",
    "category",
    "primary_topic",
    "subscribers",
    "posts_per_week",
    "activity_band",
    "created_year",
    "related_communities",
    "research_domains",
    "verification_status",
    "verified_at",
    "metadata_source",
    "selected",
    "archive_posts",
    "archive_comments",
    "archive_earliest_post",
    "archive_earliest_comment",
    "notes",
]

INVENTORY_FIELDS = [
    "subreddit",
    "kind",
    "source",
    "first_created_utc",
    "last_created_utc",
    "records",
    "raw_path",
    "raw_bytes",
    "mongo_uri",
    "mongo_database",
    "mongo_collection",
    "qa_status",
    "acquired_at",
    "notes",
]


def available_collections() -> list[str]:
    return sorted(
        path.parent.name
        for path in COLLECTIONS_DIR.glob("*/collection.toml")
        if path.is_file()
    )


def collection_dir(name: str) -> Path:
    path = COLLECTIONS_DIR / name
    if not (path / "collection.toml").is_file():
        choices = ", ".join(available_collections())
        raise SystemExit(f"unknown collection {name!r}; choose from: {choices}")
    return path


def collection_config(name: str) -> dict:
    with (collection_dir(name) / "collection.toml").open("rb") as stream:
        return tomllib.load(stream)


def read_names(name: str, filename: str) -> list[str]:
    path = collection_dir(name) / filename
    if not path.is_file():
        raise SystemExit(f"{name!r} has no {filename}")
    names: list[str] = []
    seen: set[str] = set()
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        subreddit = line.removeprefix("r/")
        key = subreddit.casefold()
        if key not in seen:
            seen.add(key)
            names.append(subreddit)
    return names


def read_name_groups(name: str, filename: str) -> dict[str, str]:
    """Map names to ``##`` section headings in a comment-friendly name list."""
    path = collection_dir(name) / filename
    if not path.is_file():
        raise SystemExit(f"{name!r} has no {filename}")
    group = ""
    groups: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            group = line.removeprefix("## ").strip()
        elif line and not line.startswith("#"):
            groups[line.removeprefix("r/").casefold()] = group
    return groups


def _integer(value: object) -> int | None:
    if value in ("", None):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _boolean(value: object) -> bool | None:
    if isinstance(value, bool):
        return value
    if value in ("", None):
        return None
    normalized = str(value).strip().casefold()
    if normalized in {"true", "yes", "1"}:
        return True
    if normalized in {"false", "no", "0"}:
        return False
    return None


def _list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in ("", None):
        return []
    return [item.strip() for item in str(value).split("|") if item.strip()]


def catalog_entry(row: dict[str, object]) -> dict:
    """Convert the scripts' flat working row into readable nested JSON."""
    return {
        "subreddit": str(row.get("subreddit", "")),
        "classification": {
            "category": str(row.get("category", "")),
            "primary_topic": str(row.get("primary_topic", "")),
            "related_communities": _list(row.get("related_communities")),
            "research_domains": _list(row.get("research_domains")),
        },
        "current_snapshot": {
            "subscribers": _integer(row.get("subscribers")),
            "created_year": _integer(row.get("created_year")),
            "activity": {
                "posts_per_week": _integer(row.get("posts_per_week")),
                "band": str(row.get("activity_band", "")),
            },
        },
        "archive": {
            "posts": _integer(row.get("archive_posts")),
            "comments": _integer(row.get("archive_comments")),
            "earliest_post": str(row.get("archive_earliest_post", "")),
            "earliest_comment": str(row.get("archive_earliest_comment", "")),
        },
        "verification": {
            "status": str(row.get("verification_status", "")),
            "verified_at": str(row.get("verified_at", "")),
            "source": str(row.get("metadata_source", "")),
        },
        "selection": {
            "selected": _boolean(row.get("selected")),
        },
        "notes": str(row.get("notes", "")),
    }


def flatten_catalog_entry(entry: dict) -> dict[str, str]:
    classification = entry.get("classification", {})
    snapshot = entry.get("current_snapshot", {})
    activity = snapshot.get("activity", {})
    archive = entry.get("archive", {})
    verification = entry.get("verification", {})
    selection = entry.get("selection", {})
    values: dict[str, object] = {
        "subreddit": entry.get("subreddit", ""),
        "category": classification.get("category", ""),
        "primary_topic": classification.get("primary_topic", ""),
        "related_communities": "|".join(classification.get("related_communities", [])),
        "research_domains": "|".join(classification.get("research_domains", [])),
        "subscribers": snapshot.get("subscribers"),
        "created_year": snapshot.get("created_year"),
        "posts_per_week": activity.get("posts_per_week"),
        "activity_band": activity.get("band", ""),
        "archive_posts": archive.get("posts"),
        "archive_comments": archive.get("comments"),
        "archive_earliest_post": archive.get("earliest_post", ""),
        "archive_earliest_comment": archive.get("earliest_comment", ""),
        "verification_status": verification.get("status", ""),
        "verified_at": verification.get("verified_at", ""),
        "metadata_source": verification.get("source", ""),
        "selected": selection.get("selected"),
        "notes": entry.get("notes", ""),
    }
    return {
        field: "" if values.get(field) is None else str(values.get(field, ""))
        for field in CATALOG_FIELDS
    }


def read_catalog(path: Path) -> dict[str, dict[str, str]]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    entries = payload.get("communities", [])
    rows = [flatten_catalog_entry(entry) for entry in entries]
    return {row["subreddit"].casefold(): row for row in rows if row["subreddit"]}


def write_catalog(path: Path, rows: Iterable[dict[str, object]]) -> None:
    """Atomically replace a catalogue with readable nested JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    payload = {
        "schema_version": 1,
        "collection": path.parent.name,
        "communities": [catalog_entry(row) for row in rows],
    }
    temporary.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def inventory_entry(row: dict[str, object]) -> dict:
    return {
        "subreddit": str(row.get("subreddit", "")),
        "kind": str(row.get("kind", "")),
        "source": str(row.get("source", "")),
        "time_range": {
            "first_created_utc": _integer(row.get("first_created_utc")),
            "last_created_utc": _integer(row.get("last_created_utc")),
        },
        "records": _integer(row.get("records")),
        "raw": {
            "path": str(row.get("raw_path", "")),
            "bytes": _integer(row.get("raw_bytes")),
        },
        "mongo": {
            "uri": str(row.get("mongo_uri", "")),
            "database": str(row.get("mongo_database", "")),
            "collection": str(row.get("mongo_collection", "")),
        },
        "qa": {
            "status": str(row.get("qa_status", "")),
        },
        "acquired_at": str(row.get("acquired_at", "")),
        "notes": str(row.get("notes", "")),
    }


def flatten_inventory_entry(entry: dict) -> dict[str, str]:
    time_range = entry.get("time_range", {})
    raw = entry.get("raw", {})
    mongo = entry.get("mongo", {})
    qa = entry.get("qa", {})
    values: dict[str, object] = {
        "subreddit": entry.get("subreddit", ""),
        "kind": entry.get("kind", ""),
        "source": entry.get("source", ""),
        "first_created_utc": time_range.get("first_created_utc"),
        "last_created_utc": time_range.get("last_created_utc"),
        "records": entry.get("records"),
        "raw_path": raw.get("path", ""),
        "raw_bytes": raw.get("bytes"),
        "mongo_uri": mongo.get("uri", ""),
        "mongo_database": mongo.get("database", ""),
        "mongo_collection": mongo.get("collection", ""),
        "qa_status": qa.get("status", ""),
        "acquired_at": entry.get("acquired_at", ""),
        "notes": entry.get("notes", ""),
    }
    return {
        field: "" if values.get(field) is None else str(values.get(field, ""))
        for field in INVENTORY_FIELDS
    }


def read_inventory(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = [flatten_inventory_entry(entry) for entry in payload.get("holdings", [])]
    return {
        (row["subreddit"].casefold(), row["kind"].casefold()): row
        for row in rows
        if row["subreddit"] and row["kind"]
    }


def write_inventory(path: Path, rows: Iterable[dict[str, object]]) -> None:
    """Atomically replace an inventory with readable nested JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    payload = {
        "schema_version": 1,
        "collection": path.parent.name,
        "holdings": [inventory_entry(row) for row in rows],
    }
    temporary.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)
