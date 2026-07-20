from __future__ import annotations

import json
from pathlib import Path


class DocumentAggregator:
    """
    Consolida os colaboradores já produzidos pelo PageMerger.

    Entrada:
        document_pages.json

    Saída:
        document_summary.json
    """

    def aggregate(self, merged_file: Path) -> Path:

        with open(merged_file, "r", encoding="utf-8") as f:
            document = json.load(f)

        collaborators = document.get("collaborators", [])

        summary = []

        for col in collaborators:

            history = sorted(
                col.get("history", []),
                key=lambda x: (
                    x.get("date") or "",
                    x.get("page") or 0,
                ),
            )

            summary.append(
                {
                    "name": col.get("name"),
                    "role": col.get("role"),
                    "days": history,
                    "activities": col.get("activities", []),
                    "observations": col.get("observations", []),
                    "signatures": col.get("signatures", []),
                    "confidence": col.get("confidence", 0.0),
                    "statistics": {
                        "occurrences": len(history),
                        "activities": len(col.get("activities", [])),
                        "observations": len(col.get("observations", [])),
                        "signatures": len(col.get("signatures", [])),
                    },
                }
            )

        output = {
            "total_pages": document.get("total_pages", 0),
            "total_collaborators": len(summary),
            "collaborators": summary,
        }

        out = merged_file.parent / "document_summary.json"

        with open(out, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)

        return out
