"""Fetch all submissions and/or comments for one subreddit via the Arctic Shift API.

Pages chronologically by advancing ``after`` past the last ``created_utc``
seen, writing newline-delimited JSON into a zstandard-compressed file whose
name matches the bulk-dump convention (``<sub>_submissions.zst`` /
``<sub>_comments.zst``). Resumable: a sidecar ``<output>.cursor`` records
the last successful timestamp.

The Arctic Shift API recommends bulk dumps for massive collections. This
script is intended for bounded or moderate per-subreddit captures; estimate
volume and validate completeness before using it for very large communities.
The repository's legacy torrent script is not a fallback: it targets a
withdrawn, subreddit-partitioned torrent.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

import zstandard

API_BASE = "https://arctic-shift.photon-reddit.com/api"
USER_AGENT = "data-gathering/0.1 (+https://github.com/reddit-data-wrangling/data-gathering)"
KIND_PATHS = {"submissions": "/posts/search", "comments": "/comments/search"}
YIELD_TO_PARENT_COMMAND: str | None = None


def process_table() -> list[tuple[int, int, str]]:
    """Read PID, parent PID, and command line from procfs."""
    processes: list[tuple[int, int, str]] = []
    for directory in Path("/proc").iterdir():
        if not directory.name.isdigit():
            continue
        try:
            stat = (directory / "stat").read_text(encoding="utf-8")
            closing = stat.rfind(")")
            fields = stat[closing + 2 :].split()
            parent = int(fields[1])
            command = (directory / "cmdline").read_bytes().replace(b"\0", b" ")
            processes.append(
                (int(directory.name), parent, command.decode(errors="replace"))
            )
        except (FileNotFoundError, PermissionError, ProcessLookupError, ValueError):
            continue
    return processes


def priority_fetch_active(parent_command: str) -> bool:
    """Return true when a matching supervisor has an active fetch child."""
    processes = process_table()
    supervisors = {
        pid for pid, _, command in processes if parent_command in command
    }
    return any(
        parent in supervisors and "fetch_subreddit.py" in command
        for _, parent, command in processes
    )


def yield_to_priority_fetch(parent_command: str) -> None:
    announced = False
    while priority_fetch_active(parent_command):
        if not announced:
            print(
                f"priority fetch active under {parent_command!r}; waiting",
                file=sys.stderr,
                flush=True,
            )
            announced = True
        time.sleep(2)
    if announced:
        print("priority fetch idle; resuming", file=sys.stderr, flush=True)


def request(path: str, params: dict) -> tuple[dict, dict]:
    if YIELD_TO_PARENT_COMMAND:
        yield_to_priority_fetch(YIELD_TO_PARENT_COMMAND)
    qs = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    url = f"{API_BASE}{path}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read()), dict(resp.headers)


def respect_rate_limit(headers: dict) -> None:
    remaining = headers.get("X-RateLimit-Remaining")
    reset = headers.get("X-RateLimit-Reset")
    if remaining is None:
        return
    try:
        remaining_i = int(remaining)
    except ValueError:
        return
    if remaining_i <= 1 and reset:
        try:
            time.sleep(max(0, int(reset)))
        except ValueError:
            time.sleep(5)


def paginate(kind: str, subreddit: str, after: int, before: int | None) -> Iterator[dict]:
    path = KIND_PATHS[kind]
    cursor = after
    seen_last_id: str | None = None
    while True:
        for attempt in range(5):
            try:
                payload, headers = request(
                    path,
                    {
                        "subreddit": subreddit,
                        "after": cursor if cursor else None,
                        "before": before,
                        "sort": "asc",
                        "limit": "auto",
                    },
                )
                break
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
                wait = 2 ** attempt
                print(f"  request failed ({exc}); retrying in {wait}s", file=sys.stderr)
                time.sleep(wait)
        else:
            raise RuntimeError("giving up after 5 retries")

        items = payload.get("data", payload) if isinstance(payload, dict) else payload
        if not items:
            return

        last_ts = cursor
        emitted = 0
        for item in items:
            if item.get("id") == seen_last_id:
                continue
            yield item
            emitted += 1
            ts = item.get("created_utc")
            if isinstance(ts, (int, float)) and ts > last_ts:
                last_ts = int(ts)
            seen_last_id = item.get("id")

        respect_rate_limit(headers)

        if emitted == 0 or last_ts == cursor:
            # No forward progress; either end of data or all items share a timestamp.
            # Bump by one second to escape ties at the cost of possibly skipping
            # same-second items (deduped via seen_last_id on next page anyway).
            if last_ts == cursor:
                cursor += 1
            else:
                return
        else:
            cursor = last_ts


def _fmt_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.0f}s"
    if seconds < 3600:
        return f"{seconds / 60:.1f}m"
    return f"{seconds / 3600:.1f}h"


def _render_progress(count: int, cursor_ts: int, start_wall: float,
                     after: int, before: int | None) -> str:
    elapsed = max(1e-3, time.time() - start_wall)
    rate = count / elapsed
    end_ts = before if before is not None else int(time.time())
    span = max(1, end_ts - after)
    done = max(0, min(span, cursor_ts - after))
    frac = done / span
    eta = (elapsed / frac - elapsed) if 0 < frac < 1 else 0
    bar_w = 24
    filled = int(bar_w * frac)
    bar = "#" * filled + "-" * (bar_w - filled)
    date = datetime.fromtimestamp(cursor_ts, tz=timezone.utc).strftime("%Y-%m-%d")
    return (f"[{bar}] {frac * 100:5.1f}% | {count:>7} items | @{date} | "
            f"{rate:5.0f}/s | elapsed {_fmt_duration(elapsed)} | "
            f"eta {_fmt_duration(eta)}")


def write_stream(items: Iterator[dict], out_path: Path, cursor_path: Path,
                 after: int, before: int | None) -> tuple[int, int]:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cctx = zstandard.ZstdCompressor(level=10)
    count = 0
    mode = "ab" if out_path.exists() else "wb"
    is_tty = sys.stderr.isatty()
    start_wall = time.time()
    last_paint = 0.0
    last_ts = after
    with open(out_path, mode) as raw, cctx.stream_writer(raw) as writer:
        for item in items:
            writer.write(
                (json.dumps(item, separators=(",", ":")) + "\n").encode("utf-8")
            )
            count += 1
            ts = item.get("created_utc")
            if isinstance(ts, (int, float)):
                last_ts = int(ts)
            if count % 1000 == 0 and isinstance(ts, (int, float)):
                cursor_path.write_text(str(int(ts)))
            now = time.time()
            if is_tty and now - last_paint >= 0.25:
                line = _render_progress(count, last_ts, start_wall, after, before)
                print(f"\r{line}", end="", file=sys.stderr, flush=True)
                last_paint = now
            elif not is_tty and count % 1000 == 0:
                line = _render_progress(count, last_ts, start_wall, after, before)
                print(line, file=sys.stderr, flush=True)
    if is_tty and count:
        line = _render_progress(count, last_ts, start_wall, after, before)
        print(f"\r{line}", file=sys.stderr, flush=True)
    if count:
        # Persist the final partial page too. Previously only multiples of 1,000
        # advanced the cursor, causing small captures to restart from scratch.
        cursor_path.write_text(str(last_ts))
    return count, last_ts


def fetch_kind(subreddit: str, kind: str, outdir: Path, after: int,
               before: int | None) -> None:
    out_path = outdir / f"{subreddit}_{kind}.zst"
    cursor_path = outdir / f"{subreddit}_{kind}.cursor"
    resume_from = after
    if cursor_path.exists():
        try:
            resume_from = max(after, int(cursor_path.read_text().strip()))
            print(f"resuming {kind} from {resume_from}", file=sys.stderr)
        except ValueError:
            pass
    print(
        f"fetching r/{subreddit} {kind} after={resume_from} before={before}",
        file=sys.stderr,
    )
    n, _ = write_stream(
        paginate(kind, subreddit, resume_from, before),
        out_path,
        cursor_path,
        resume_from,
        before,
    )
    print(f"wrote {n} {kind} -> {out_path}", file=sys.stderr)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("subreddit", help="name without r/ prefix, e.g. wikipedia")
    p.add_argument("--outdir", type=Path, default=Path("data/raw"))
    p.add_argument(
        "--kind",
        choices=["submissions", "comments", "both"],
        default="both",
    )
    p.add_argument("--after", type=int, default=0, help="epoch seconds; 0 = start of Reddit")
    p.add_argument("--before", type=int, default=None, help="epoch seconds; default = now")
    p.add_argument(
        "--yield-to-parent-command",
        default=None,
        help=(
            "pause between API requests while a matching supervisor has an "
            "active fetch_subreddit.py child"
        ),
    )
    args = p.parse_args()

    global YIELD_TO_PARENT_COMMAND
    YIELD_TO_PARENT_COMMAND = args.yield_to_parent_command

    kinds = ["submissions", "comments"] if args.kind == "both" else [args.kind]
    for kind in kinds:
        fetch_kind(args.subreddit, kind, args.outdir, args.after, args.before)


if __name__ == "__main__":
    main()
