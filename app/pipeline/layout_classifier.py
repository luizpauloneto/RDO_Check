from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2

from app.ai.vision_executor import VisionExecutor


@dataclass
class LayoutResult:
    page_type: str
    confidence: float
    reason: str


class LayoutClassifier:
    """
    Classificador sem pytesseract.
    Usa OpenCV e consulta o Qwen apenas quando necessário.
    """

    def __init__(self):
        self.vision = VisionExecutor()

    def classify(self, image_path: Path) -> LayoutResult:

        image = cv2.imread(str(image_path))
        if image is None:
            raise RuntimeError(f"Não foi possível abrir {image_path}")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        edges = cv2.Canny(gray, 80, 180)

        lines = cv2.HoughLinesP(
            edges,
            1,
            3.14159 / 180,
            threshold=120,
            minLineLength=int(w * 0.45),
            maxLineGap=8,
        )

        horizontal = 0

        if lines is not None:

            for line in lines:

                coords = line.flatten()

                if len(coords) != 4:
                    continue

                x1, y1, x2, y2 = map(int, coords)

                if abs(y2 - y1) <= 2:
                    horizontal += 1

        if horizontal > 35:
            return LayoutResult("rdo",0.90,"opencv_table")

        cnts,_=cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        photo_blocks=0
        total=h*w
        for c in cnts:
            x,y,cw,ch=cv2.boundingRect(c)
            if cw*ch>total*0.04:
                photo_blocks+=1

        if photo_blocks>=4:
            return LayoutResult("fotografico",0.85,"opencv_blocks")

        region=type("Region",(),{
            "prompt":"layout",
            "region_type":"layout",
            "image_path":image_path,
            "bbox":None,
        })()

        try:
            result=self.vision.execute(region)
            if isinstance(result,dict):
                layout=(result.get("layout") or result.get("page_type") or "").lower()
                if layout in ("rdo","fotografico","lista_presenca"):
                    return LayoutResult(layout,0.75,"qwen")
        except Exception:
            pass

        return LayoutResult("unknown",0.40,"fallback")
