#!/usr/bin/env bash
set -Eeuo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
session_name="reddit_linux_collection"

if tmux has-session -t "$session_name" 2>/dev/null; then
  echo "tmux session already exists: $session_name" >&2
  exit 1
fi

tmux new-session -d -s "$session_name" -c "$repo_dir" \
  "exec bash scripts/run_linux_collection.sh"
echo "started tmux session: $session_name"
