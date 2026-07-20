from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


class PageMerger:
    """
    Consolida páginas utilizando os colaboradores já enriquecidos
    pelo AssignmentEngine.
    """

    def merge(self, output_dir: Path) -> Path:

        pages = []
        employees = defaultdict(lambda: {
            "name": "",
            "role": "",
            "history": [],
            "activities": [],
            "observations": [],
            "signatures": [],
            "confidence": [],
        })

        for file in sorted(output_dir.glob("page_*.json")):

            with open(file, "r", encoding="utf-8") as fp:
                page = json.load(fp)

            pages.append(page)

            for emp in page.get("employees", []):

                name = emp.get("name", "").strip()

                if not name:
                    continue

                item = employees[name]

                item["name"] = name
                item["role"] = emp.get("role", item["role"])

                item["history"].append({
                    "page": page.get("page"),
                    "date": emp.get("date"),
                    "entry": emp.get("entry"),
                    "exit": emp.get("exit"),
                })

                item["activities"].extend(emp.get("activities", []))
                item["observations"].extend(emp.get("observations", []))
                item["signatures"].extend(emp.get("signatures", []))
                item["confidence"].append(emp.get("confidence", 0.0))

        collaborators = []

        for emp in sorted(employees.values(), key=lambda x: x["name"]):

            conf = emp["confidence"]
            emp["confidence"] = (
                round(sum(conf) / len(conf), 3) if conf else 0.0
            )

            collaborators.append(emp)

        document = {
            "pages": pages,
            "collaborators": collaborators,
            "total_pages": len(pages),
            "total_collaborators": len(collaborators),
        }

        out = output_dir / "document_pages.json"

        with open(out, "w", encoding="utf-8") as fp:
            json.dump(document, fp, indent=4, ensure_ascii=False)

        return out
