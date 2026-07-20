from __future__ import annotations

import json
from pathlib import Path


class EmployeeTimeline:
    """
    Compatível com document_summary antigo e v2.
    """

    def build(self, summary_file: Path) -> Path:

        with open(summary_file,"r",encoding="utf-8") as f:
            data=json.load(f)

        if isinstance(data, dict):
            employees=data.get("collaborators",[])
        elif isinstance(data, list):
            employees=data
        else:
            employees=[]

        timeline=[]

        for employee in employees:

            if not isinstance(employee,dict):
                continue

            history=employee.get("days") or employee.get("history") or []

            # formato antigo: dict por data
            if isinstance(history,dict):
                entries=[]
                for date in sorted(history.keys()):
                    item=history[date] or {}
                    entries.append({
                        "date":date,
                        "entry":item.get("entry"),
                        "lunch_out":item.get("lunch_out"),
                        "lunch_in":item.get("lunch_in"),
                        "exit":item.get("exit"),
                    })
            else:
                entries=sorted(
                    history,
                    key=lambda x:(
                        x.get("date") or "",
                        x.get("page") or 0,
                    ),
                )

            timeline.append({
                "name":employee.get("name"),
                "role":employee.get("role"),
                "timeline":entries,
                "activities":employee.get("activities",[]),
                "observations":employee.get("observations",[]),
                "signatures":employee.get("signatures",[]),
                "confidence":employee.get("confidence",0.0),
                "summary":employee.get("summary",""),
            })

        out=summary_file.parent/"employee_timeline.json"

        with open(out,"w",encoding="utf-8") as f:
            json.dump(timeline,f,indent=4,ensure_ascii=False)

        return out
