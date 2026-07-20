from __future__ import annotations

import json
from pathlib import Path


class EmployeeReportBuilder:
    """
    Gera o relatório final por colaborador.

    Entrada:
        employees_consolidated.json

    Saída:
        employee_report.json
    """

    def build(self, consolidated_file: Path) -> Path:

        with open(consolidated_file, "r", encoding="utf-8") as f:
            employees = json.load(f)

        report = []

        for emp in employees:

            history = sorted(
                emp.get("history", []),
                key=lambda x: (x.get("page", 0), x.get("entry") or "")
            )

            report.append({
                "name": emp.get("name"),
                "role": emp.get("role"),
                "total_occurrences": len(history),
                "history": history,
                "activities": emp.get("activities", []),
                "observations": emp.get("observations", []),
                "signatures": emp.get("signatures", []),
                "ai_summary": (
                    f'{emp.get("name")} participou de '
                    f'{len(history)} ocorrência(s), '
                    f'{len(emp.get("activities", []))} atividade(s) '
                    f'e possui {len(emp.get("signatures", []))} assinatura(s).'
                )
            })

        out = consolidated_file.parent / "employee_report.json"

        with open(out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)

        return out
