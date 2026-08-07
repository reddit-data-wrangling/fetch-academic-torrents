#!/usr/bin/env bash
set -Eeuo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
log_dir="$repo_dir/data/logs"
log_path="$log_dir/oss-collection.log"

mkdir -p "$log_dir"
cd "$repo_dir"

{
  echo
  echo "=== OSS collection: $(date --iso-8601=seconds) ==="
  exec nice -n 10 ionice -c 2 -n 7 \
    python -u scripts/resume_oss_collection.py
} 2>&1 | tee -a "$log_path"
