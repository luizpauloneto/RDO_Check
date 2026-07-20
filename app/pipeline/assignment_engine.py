from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any


class AssignmentEngine:
    """
    AssignmentEngine v2

    Evolução da versão inicial com regras de inferência.
    """

    def assign(self, page: dict[str, Any]) -> dict[str, Any]:

        results = page.get("results", [])

        header = {}
        employees = []
        activities = []
        observations = []
        signatures = []

        for result in results:

            if not isinstance(result, dict):
                continue

            region = result.get("region")

            if region == "header":
                header = result

            elif region == "employees":
                employees.extend(
                    result.get("employees")
                    or result.get("colaboradores")
                    or []
                )

            elif region == "activities":
                activities.extend(
                    result.get("items")
                    or result.get("activities")
                    or []
                )

            elif region == "observations":
                observations.extend(
                    result.get("observacoes")
                    or result.get("items")
                    or []
                )

            elif region == "signatures":
                signatures.extend(
                    result.get("assinaturas")
                    or result.get("items")
                    or []
                )

        date = header.get("data") or header.get("date")

        enriched = []

        for emp in employees:

            name = (emp.get("nome") or emp.get("name") or "").strip()
            if not name:
                continue

            info = {
                "name": name,
                "role": emp.get("funcao") or emp.get("role"),
                "date": date,
                "entry": emp.get("horario_entrada") or emp.get("entry"),
                "exit": emp.get("horario_saida") or emp.get("exit"),
                "activities": [],
                "observations": list(observations),
                "signatures": [],
                "confidence": 0.50,
            }

            for act in activities:

                ok, inferred = self._match_activity(
                    name,
                    act,
                    len(employees),
                )

                if ok:
                    activity = dict(act) if isinstance(act, dict) else {"value": act}
                    activity["inferred"] = inferred
                    info["activities"].append(activity)

                    info["confidence"] += 0.15 if not inferred else 0.05

            for sig in signatures:

                ok, inferred = self._match_signature(
                    name,
                    sig,
                    len(employees),
                )

                if ok:
                    signature = dict(sig) if isinstance(sig, dict) else {"value": sig}
                    signature["inferred"] = inferred
                    info["signatures"].append(signature)

                    info["confidence"] += 0.10 if not inferred else 0.03

            info["confidence"] = round(min(info["confidence"], 1.0), 2)

            enriched.append(info)

        page["employees"] = enriched

        return page

    def _match_activity(self, employee, activity, total):

        if not isinstance(activity, dict):
            return False, False

        names = activity.get("colaboradores") or activity.get("employees") or []

        if names:
            for n in names:
                if self._similar(employee, str(n)) >= 0.90:
                    return True, False
            return False, False

        if total == 1:
            return True, True

        return False, False

    def _match_signature(self, employee, signature, total):

        if not isinstance(signature, dict):
            return False, False

        names = signature.get("colaboradores") or signature.get("employees") or []

        if names:
            for n in names:
                if self._similar(employee, str(n)) >= 0.90:
                    return True, False
            return False, False

        if total == 1:
            return True, True

        return False, False

    @staticmethod
    def _similar(a, b):
        return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()
