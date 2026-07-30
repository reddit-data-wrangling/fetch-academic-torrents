# Collection schemas

Reusable metadata contracts for every collection:

- [`catalog.schema.json`](catalog.schema.json) describes candidate-community
  metadata, verification, and selection.
- [`inventory.schema.json`](inventory.schema.json) describes known raw
  holdings, MongoDB metadata, and QA state.

Collection instances remain in `collections/<domain>/`; schemas are kept here
so they are not mistaken for collection manifests.

The schemas constrain the complete nested object shape and scalar types.
`scripts/audit_collection.py` currently checks only the catalogue envelope and
selection gates; full automated JSON Schema validation remains roadmap work.
