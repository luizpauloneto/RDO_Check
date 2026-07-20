from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.core.logger import logger


class ResponseParser:
    """
    Compatível com Sprint 2 e Sprint 3.
    """

    def parse(self, merged_json: Path) -> dict[str, Any]:

        if not merged_json.exists():
            raise FileNotFoundError(merged_json)

        with open(merged_json, "r", encoding="utf-8") as fp:
            data = json.load(fp)

        document = {
            "pages": [],
            "fields": {},
            "regions": [],
            "collaborators": data.get("collaborators", []),
            "observations": data.get("observations", []),
        }

        for page in data.get("pages", []):

            document["pages"].append(page.get("page"))

            results = page.get("results") or page.get("regions") or []

            for result in results:

                document["regions"].append(result)

                if not isinstance(result, dict):
                    continue

                for key, value in result.items():

                    if key in (
                        "region",
                        "bbox",
                        "items",
                        "employees",
                        "colaboradores",
                        "assinaturas",
                        "observacoes",
                    ):
                        continue

                    if key not in document["fields"]:
                        document["fields"][key] = value

        logger.info(
            "Documento interpretado (%d páginas, %d regiões).",
            len(document["pages"]),
            len(document["regions"]),
        )

        return document
