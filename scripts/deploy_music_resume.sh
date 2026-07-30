#!/usr/bin/env bash
set -Eeuo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
log_dir="$repo_dir/data/logs"
log_path="$log_dir/music-resume.log"

mkdir -p "$log_dir"
cd "$repo_dir"

{
  echo
  echo "=== music collection resume: $(date --iso-8601=seconds) ==="
  exec python -u scripts/resume_music_collection.py
} 2>&1 | tee -a "$log_path"
