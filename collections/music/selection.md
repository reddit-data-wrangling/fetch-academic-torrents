# Music panel selection

Status: acquisition resumed on 2026-07-31.

The existing programme and loaded counts are recorded in [`progress.md`](progress.md)
and the cross-collection
[operations log](../../docs/operations/collection-log.md). The project owner
authorised resuming the existing 130-subreddit programme. The resume job reads
that table, skips communities already held in both MongoDB collections, and
processes the remainder smallest-first.
