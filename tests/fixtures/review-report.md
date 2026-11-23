# modlock comparison

Context: synthetic:review

| Category | Base index/name | Head index/name | Fields / reason |
|---|---|---|---|
| ambiguous | 0: Partial Files |  | uncertain\_identity |
| ambiguous |  | 0: Partial Files | uncertain\_identity |

## Summary

| Category | Count |
|---|---:|
| ambiguous | 2 |

## Reader warnings

| Side | Location | Code | Message |
|---|---|---|---|
| base | $\[0\]\.general | incomplete\_metadata | Metadata fields are absent or empty\. |
| base | $\[0\]\.installed | metadata\_count | Declared file count is inconsistent\. |
| head | $\[0\]\.general | incomplete\_metadata | Metadata fields are absent or empty\. |
| head | $\[0\]\.installed | metadata\_count | Declared file count is inconsistent\. |

## Reproducibility signals

Unknown means insufficient evidence; presence is declared metadata.

| Side | Unknown signal | Count |
|---|---|---:|
| base | content\_hash | 1 |
| base | file\_references | 1 |
| base | game | 1 |
| base | provenance | 1 |
| base | version | 1 |
| head | content\_hash | 1 |
| head | file\_references | 1 |
| head | game | 1 |
| head | provenance | 1 |
| head | version | 1 |

## Limitations

- Experimental Meteoric JSON 1\.0 structure; producer/version not authenticated\.
- Context is a caller assertion of same game and export lineage, not verification\.
- Reference correspondence is not content integrity, FOMOD equivalence or compatibility\.
- Changed file IDs, incomplete identities and collisions can remain unresolved\.

## Complete evidence (JSON)

```json
{
  "audit": {
    "base": {
      "records": [
        {
          "index": 0,
          "signals": {
            "content_hash": {
              "location": null,
              "reason": "unsupported_content_evidence",
              "state": "unknown"
            },
            "file_references": {
              "location": "$[0].installed",
              "reason": "incomplete_or_ambiguous_references",
              "state": "unknown"
            },
            "game": {
              "location": null,
              "reason": "unverified_game_context",
              "state": "unknown"
            },
            "order": {
              "location": "$[0].order",
              "reason": "export_position_only",
              "state": "present"
            },
            "page_identifier": {
              "location": "$[0].id",
              "reason": "declared_page_id",
              "state": "present"
            },
            "provenance": {
              "location": null,
              "reason": "unauthenticated_producer",
              "state": "unknown"
            },
            "version": {
              "location": "$[0].general.version",
              "reason": "missing_version",
              "state": "unknown"
            }
          }
        }
      ],
      "summary": {
        "mods": 1,
        "unknown_signals": {
          "content_hash": 1,
          "file_references": 1,
          "game": 1,
          "provenance": 1,
          "version": 1
        }
      }
    },
    "head": {
      "records": [
        {
          "index": 0,
          "signals": {
            "content_hash": {
              "location": null,
              "reason": "unsupported_content_evidence",
              "state": "unknown"
            },
            "file_references": {
              "location": "$[0].installed",
              "reason": "incomplete_or_ambiguous_references",
              "state": "unknown"
            },
            "game": {
              "location": null,
              "reason": "unverified_game_context",
              "state": "unknown"
            },
            "order": {
              "location": "$[0].order",
              "reason": "export_position_only",
              "state": "present"
            },
            "page_identifier": {
              "location": "$[0].id",
              "reason": "declared_page_id",
              "state": "present"
            },
            "provenance": {
              "location": null,
              "reason": "unauthenticated_producer",
              "state": "unknown"
            },
            "version": {
              "location": "$[0].general.version",
              "reason": "missing_version",
              "state": "unknown"
            }
          }
        }
      ],
      "summary": {
        "mods": 1,
        "unknown_signals": {
          "content_hash": 1,
          "file_references": 1,
          "game": 1,
          "provenance": 1,
          "version": 1
        }
      }
    },
    "limitations": [
      "Presence is declared export metadata, not verified installed content.",
      "Unknown does not prove absence, incompatibility or malicious content.",
      "Order is export position, not plugin load order or conflict detection.",
      "Unknown extension fields are preserved but not trusted as evidence."
    ],
    "schema": "modlock-audit-0.2-experimental"
  },
  "changes": [
    {
      "base": {
        "data": {
          "active": true,
          "displayName": "Partial Files",
          "general": {},
          "id": 91003,
          "installed": {
            "files": [
              {
                "fileid": "81003",
                "modid": "91003"
              }
            ],
            "size": 2
          },
          "modName": "Partial Files",
          "order": 0,
          "plugins": [],
          "separatorName": "Unsectioned",
          "tags": [],
          "type": "mod"
        },
        "identity": {
          "conflicting_indices": [],
          "reasons": [
            "incomplete_file_list"
          ],
          "references": [
            {
              "file_id": 81003,
              "page_id": 91003
            }
          ],
          "state": "incomplete"
        },
        "index": 0
      },
      "category": "ambiguous",
      "fields": [],
      "head": null,
      "reason": "uncertain_identity"
    },
    {
      "base": null,
      "category": "ambiguous",
      "fields": [],
      "head": {
        "data": {
          "active": true,
          "displayName": "Partial Files",
          "general": {},
          "id": 91003,
          "installed": {
            "files": [
              {
                "fileid": "81003",
                "modid": "91003"
              }
            ],
            "size": 2
          },
          "modName": "Partial Files",
          "order": 0,
          "plugins": [],
          "separatorName": "Unsectioned",
          "tags": [],
          "type": "mod"
        },
        "identity": {
          "conflicting_indices": [],
          "reasons": [
            "incomplete_file_list"
          ],
          "references": [
            {
              "file_id": 81003,
              "page_id": 91003
            }
          ],
          "state": "incomplete"
        },
        "index": 0
      },
      "reason": "uncertain_identity"
    }
  ],
  "context": "synthetic:review",
  "limitations": [
    "Experimental Meteoric JSON 1.0 structure; producer/version not authenticated.",
    "Context is a caller assertion of same game and export lineage, not verification.",
    "Reference correspondence is not content integrity, FOMOD equivalence or compatibility.",
    "Changed file IDs, incomplete identities and collisions can remain unresolved."
  ],
  "schema": "modlock-0.1-experimental",
  "summary": {
    "ambiguous": 2
  },
  "warnings": {
    "base": [
      {
        "code": "incomplete_metadata",
        "location": "$[0].general",
        "message": "Metadata fields are absent or empty."
      },
      {
        "code": "metadata_count",
        "location": "$[0].installed",
        "message": "Declared file count is inconsistent."
      }
    ],
    "head": [
      {
        "code": "incomplete_metadata",
        "location": "$[0].general",
        "message": "Metadata fields are absent or empty."
      },
      {
        "code": "metadata_count",
        "location": "$[0].installed",
        "message": "Declared file count is inconsistent."
      }
    ]
  }
}
```
