from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


class EmployeeConsolidator:
    """
    Consolida todas as ocorrências de um colaborador em um único histórico.

    Entrada:
        document_pages.json

    Saída:
        employees_consolidated.json
    """

    def consolidate(self, merged_file: Path) -> Path:

        with open(merged_file, "r", encoding="utf-8") as f:
            document = json.load(f)

        employees = defaultdict(lambda: {
            "name": "",
            "role": "",
            "history": [],
            "activities": [],
            "observations": [],
            "signatures": [],
        })

        for page in document.get("pages", []):

            page_number = page.get("page")

            # índice de atividades desta página
            page_activities = []
            page_observations = []
            page_signatures = []

            for result in page.get("results", []):

                if isinstance(result, dict):
                    page_activities.extend(result.get("items", []))
                    page_observations.extend(result.get("observacoes", []))
                    page_signatures.extend(result.get("assinaturas", []))

            for result in page.get("results", []):

                people = (
                    result.get("colaboradores")
                    or result.get("employees")
                    or []
                )

                for person in people:

                    name = (
                        person.get("nome")
                        or person.get("name")
                        or ""
                    ).strip()

                    if not name:
                        continue

                    item = employees[name]
                    item["name"] = name
                    item["role"] = (
                        person.get("funcao")
                        or person.get("role")
                        or item["role"]
                    )

                    item["history"].append({
                        "page": page_number,
                        "entry": person.get("horario_entrada") or person.get("entry"),
                        "exit": person.get("horario_saida") or person.get("exit"),
                        "lunch": person.get("almoço") or person.get("almoco"),
                    })

                    item["activities"].extend(page_activities)
                    item["observations"].extend(page_observations)
                    item["signatures"].extend(page_signatures)

        output = sorted(employees.values(), key=lambda x: x["name"])

        out_file = merged_file.parent / "employees_consolidated.json"

        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)

        return out_file
