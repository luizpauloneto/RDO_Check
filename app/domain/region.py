from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class RegionType(str, Enum):
    """
    Tipos de regiões reconhecidas em um RDO.
    """

    HEADER = "HEADER"

    EMPLOYEES = "EMPLOYEES"

    ACTIVITIES = "ACTIVITIES"

    EQUIPMENT = "EQUIPMENT"

    MATERIAL = "MATERIAL"

    WEATHER = "WEATHER"

    OBSERVATIONS = "OBSERVATIONS"

    SIGNATURES = "SIGNATURES"

    UNKNOWN = "UNKNOWN"


@dataclass(slots=True)
class BoundingBox:
    """
    Coordenadas absolutas da região na página.
    """

    x: int

    y: int

    width: int

    height: int

    @property
    def right(self) -> int:

        return self.x + self.width

    @property
    def bottom(self) -> int:

        return self.y + self.height

    @property
    def area(self) -> int:

        return self.width * self.height

    def as_tuple(self) -> tuple[int, int, int, int]:

        return (

            self.x,

            self.y,

            self.width,

            self.height

        )


@dataclass(slots=True)
class Region:

    """
    Região identificada em uma página.
    """

    id: str

    page: int

    region_type: RegionType

    bbox: BoundingBox

    confidence: float = 1.0

    image_path: Path | None = None

    json_path: Path | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    # ==========================================================
    # Conversão
    # ==========================================================

    def to_dict(self) -> dict:

        return {

            "id": self.id,

            "page": self.page,

            "type": self.region_type.value,

            "confidence": self.confidence,

            "bbox": {

                "x": self.bbox.x,

                "y": self.bbox.y,

                "width": self.bbox.width,

                "height": self.bbox.height

            },

            "image_path": (

                str(self.image_path)

                if self.image_path

                else None

            ),

            "json_path": (

                str(self.json_path)

                if self.json_path

                else None

            ),

            "metadata": self.metadata

        }

    # ==========================================================
    # Construção
    # ==========================================================

    @classmethod
    def from_dict(

        cls,

        data: dict

    ) -> "Region":

        bbox = BoundingBox(

            x=data["bbox"]["x"],

            y=data["bbox"]["y"],

            width=data["bbox"]["width"],

            height=data["bbox"]["height"]

        )

        return cls(

            id=data["id"],

            page=data["page"],

            region_type=RegionType(

                data["type"]

            ),

            bbox=bbox,

            confidence=data.get(

                "confidence",

                1.0

            ),

            image_path=(

                Path(data["image_path"])

                if data.get("image_path")

                else None

            ),

            json_path=(

                Path(data["json_path"])

                if data.get("json_path")

                else None

            ),

            metadata=data.get(

                "metadata",

                {}

            )

        )

    # ==========================================================
    # Nome padrão
    # ==========================================================

    @property
    def filename(self) -> str:

        return (

            f"page_{self.page:03d}_"

            f"{self.region_type.value.lower()}.png"

        )

    @property
    def json_filename(self) -> str:

        return (

            f"page_{self.page:03d}_"

            f"{self.region_type.value.lower()}.json"

        )