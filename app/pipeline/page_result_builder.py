from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class PageResultBuilder:

    def build(
        self,
        page: int,
        results: list,
        page_type: str | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> dict:

        employees: list[dict] = []
        activities: list[dict] = []
        photos: list[dict] = []
        equipments: list[dict] = []
        signatures: list[dict] = []
        observations: list[dict] = []
        headers: list[dict] = []

        for result in results:

            if not isinstance(result, dict):
                continue

            region = result.get("region")

            if region == "employees":

                employees.extend(
                    result.get("employees", [])
                )

            elif region == "activities":

                activities.append(result)

            elif region == "photos":

                photos.append(result)

            elif region == "equipment":

                equipments.append(result)

            elif region == "signatures":

                signatures.append(result)

            elif region == "observations":

                observations.append(result)

            elif region == "header":

                headers.append(result)

        return {

            "page": page,

            "page_type": page_type or "unknown",

            "width": width,

            "height": height,

            "total_regions": len(results),

            "employees": employees,

            "activities": activities,

            "photos": photos,

            "equipments": equipments,

            "signatures": signatures,

            "observations": observations,

            "headers": headers,

            "statistics": {

                "employees": len(employees),

                "activities": len(activities),

                "photos": len(photos),

                "equipments": len(equipments),

                "signatures": len(signatures),

                "observations": len(observations),

                "regions": len(results),

            },

            "results": results,

        }

    def save(
        self,
        page_result: dict,
        output_dir: Path,
        page: int,
    ) -> Path:

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        file = output_dir / f"page_{page:03}.json"

        with open(
            file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                page_result,
                f,
                indent=4,
                ensure_ascii=False,
            )

        return file