from __future__ import annotations

from pathlib import Path
from typing import List

import cv2

from app.core.logger import logger
from app.pipeline.template_engine import RegionTemplate


class SmartCropper:
    """
    Recorta regiões utilizando coordenadas relativas
    fornecidas pelo TemplateEngine.
    """

    def crop(
        self,
        image_path: Path,
        templates: List[RegionTemplate],
        output_dir: Path,
    ) -> List[dict]:

        image = cv2.imread(str(image_path))

        if image is None:
            raise RuntimeError(f"Imagem inválida: {image_path}")

        output_dir.mkdir(parents=True, exist_ok=True)

        h, w = image.shape[:2]

        regions = []

        stem = image_path.stem

        for template in templates:

            rx, ry, rw, rh = template.bbox

            x = max(0, int(rx * w))
            y = max(0, int(ry * h))
            cw = max(1, int(rw * w))
            ch = max(1, int(rh * h))

            crop = image[y:y + ch, x:x + cw]

            filename = f"{stem}_{template.name}.png"

            crop_path = output_dir / filename

            cv2.imwrite(str(crop_path), crop)

            logger.info(
                "Crop %s salvo (%dx%d)",
                filename,
                cw,
                ch,
            )

            regions.append(
                {
                    "name": template.name,
                    "prompt": template.prompt,
                    "image_path": crop_path,
                    "bbox": (x, y, cw, ch),
                }
            )

        return regions
