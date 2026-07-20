from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2

from app.pipeline.layout_classifier import LayoutClassifier


@dataclass
class PageInfo:
    page_type: str
    width: int
    height: int
    confidence: float
    reason: str


class PageAnalyzer:
    """
    Analisa a página e delega a classificação de layout
    ao LayoutClassifier.
    """

    def __init__(self):
        self.classifier = LayoutClassifier()

    def analyze(self, image_path: Path) -> PageInfo:

        image = cv2.imread(str(image_path))

        if image is None:
            raise RuntimeError(f"Não foi possível abrir {image_path}")

        height, width = image.shape[:2]

        layout = self.classifier.classify(image_path)

        return PageInfo(
            page_type=layout.page_type,
            width=width,
            height=height,
            confidence=layout.confidence,
            reason=layout.reason,
        )
