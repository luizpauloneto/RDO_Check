from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


class SummaryBuilder:
    """
    Gera o resumo executivo do processamento.

    Entrada:
        employee_timeline.json

    Saída:
        final_summary.json
    """

    def build(self, timeline_file: Path) -> Path:

        with open(timeline_file, "r", encoding="utf-8") as f:
            employees = json.load(f)

        summary = {
            "total_collaborators": len(employees),
            "total_days": 0,
            "activities": Counter(),
            "equipment": Counter(),
            "materials": Counter(),
            "employees": [],
        }

        for emp in employees:

            summary["total_days"] += len(emp.get("timeline", []))

            for item in emp.get("activities", []):
                summary["activities"][item] += 1

            for item in emp.get("equipment", []):
                summary["equipment"][item] += 1

            for item in emp.get("materials", []):
                summary["materials"][item] += 1

            summary["employees"].append({
                "name": emp.get("name"),
                "days": len(emp.get("timeline", [])),
                "activities": len(emp.get("activities", [])),
                "equipment": len(emp.get("equipment", [])),
                "materials": len(emp.get("materials", [])),
                "signatures": len(emp.get("signatures", [])),
                "summary": emp.get("summary",""),
            })

        summary["activities"] = dict(summary["activities"].most_common())
        summary["equipment"] = dict(summary["equipment"].most_common())
        summary["materials"] = dict(summary["materials"].most_common())

        out = timeline_file.parent / "final_summary.json"

        with open(out,"w",encoding="utf-8") as f:
            json.dump(summary,f,indent=4,ensure_ascii=False)

        return out
