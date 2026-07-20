from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2


@dataclass
class PhotoAnalysis:
    photo_count: int
    image_ratio: float
    is_photographic: bool


class PhotoDetector:
    """
    Detecta páginas predominantemente fotográficas.

    Utiliza apenas características visuais.
    """

    def analyze(self, image_path: Path) -> PhotoAnalysis:

        image = cv2.imread(str(image_path))
        if image is None:
            raise RuntimeError(f"Não foi possível abrir {image_path}")

        h, w = image.shape[:2]
        total_area = h * w

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray, 80, 180)

        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        photo_count = 0
        photo_area = 0

        for cnt in contours:
            x, y, cw, ch = cv2.boundingRect(cnt)

            area = cw * ch

            if area < total_area * 0.015:
                continue

            ratio = cw / max(ch, 1)

            # Fotos normalmente possuem formato aproximadamente retangular
            if 0.6 <= ratio <= 2.0:
                photo_count += 1
                photo_area += area

        image_ratio = round(photo_area / total_area, 3)

        return PhotoAnalysis(
            photo_count=photo_count,
            image_ratio=image_ratio,
            is_photographic=(
                photo_count >= 2 and image_ratio > 0.25
            ),
        )
