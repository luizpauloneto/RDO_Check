from __future__ import annotations

import json
from pathlib import Path


class ConsistencyValidator:
    """
    Valida automaticamente inconsistências encontradas
    no relatório consolidado dos colaboradores.

    Entrada:
        employee_report.json

    Saída:
        consistency_report.json
    """

    def validate(self, report_file: Path) -> Path:

        with open(report_file, "r", encoding="utf-8") as f:
            employees = json.load(f)

        report = []

        for emp in employees:

            issues = []

            history = emp.get("history", [])

            if not history:
                issues.append("Colaborador sem histórico.")

            if not emp.get("activities"):
                issues.append("Nenhuma atividade encontrada.")

            if not emp.get("signatures"):
                issues.append("Nenhuma assinatura encontrada.")

            for item in history:

                entry = item.get("entry")
                exit_ = item.get("exit")

                if not entry:
                    issues.append(
                        f'Página {item.get("page")}: entrada ausente.'
                    )

                if not exit_:
                    issues.append(
                        f'Página {item.get("page")}: saída ausente.'
                    )

            report.append(
                {
                    "name": emp.get("name"),
                    "role": emp.get("role"),
                    "status": (
                        "OK"
                        if not issues
                        else "WARNING"
                    ),
                    "issues": issues,
                }
            )

        out = report_file.parent / "consistency_report.json"

        with open(out, "w", encoding="utf-8") as f:
            json.dump(
                report,
                f,
                indent=4,
                ensure_ascii=False,
            )

        return out
