from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from app.core.logger import logger
from app.domain.region import BoundingBox, Region, RegionType


class LayoutDetector:
    """Detector base de layout da Sprint 2."""

    def detect(
        self,
        image_path: Path,
        page: int,
    ) -> list[Region]:

        logger.info(
            "Detectando layout da página %d (%s)",
            page,
            image_path.name,
        )

        region = Region(
            id=str(uuid4()),
            page=page,
            region_type=RegionType.UNKNOWN,
            bbox=BoundingBox(
                x=0,
                y=0,
                width=0,
                height=0,
            ),
            confidence=1.0,
            metadata={
                "source": "layout_detector",
                "image": image_path.name,
            },
        )

        return [region]
