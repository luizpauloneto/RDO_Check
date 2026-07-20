from __future__ import annotations

from pathlib import Path

import cv2

from app.core.logger import logger
from app.domain.region import Region


class RegionCropper:
    """
    Recorta as regiões detectadas pelo LayoutDetector.
    Atualiza automaticamente region.image_path.
    """

    def crop(
        self,
        image_path: Path,
        region: Region,
        output_dir: Path,
    ) -> Path:

        image = cv2.imread(str(image_path))

        if image is None:
            raise RuntimeError(f"Imagem inválida: {image_path}")

        h_img, w_img = image.shape[:2]

        x = max(0, region.bbox.x)
        y = max(0, region.bbox.y)
        w = max(1, region.bbox.width)
        h = max(1, region.bbox.height)

        x2 = min(x + w, w_img)
        y2 = min(y + h, h_img)

        crop = image[y:y2, x:x2]

        if crop.size == 0:
            raise RuntimeError(
                f"Crop vazio para a região {region.id}"
            )

        output_dir.mkdir(parents=True, exist_ok=True)

        output = output_dir / region.filename

        if not cv2.imwrite(str(output), crop):
            raise RuntimeError(f"Falha ao salvar {output}")

        region.image_path = output

        logger.info(
            "Crop %s salvo (%dx%d)",
            output.name,
            crop.shape[1],
            crop.shape[0],
        )

        return output

    def crop_all(
        self,
        image_path: Path,
        regions: list[Region],
        output_dir: Path,
    ) -> list[Region]:

        processed: list[Region] = []

        for region in regions:
            try:
                self.crop(
                    image_path=image_path,
                    region=region,
                    output_dir=output_dir,
                )
                processed.append(region)
            except Exception:
                logger.exception(
                    "Erro ao recortar região %s",
                    region.id,
                )

        logger.info(
            "%d/%d regiões recortadas.",
            len(processed),
            len(regions),
        )

        return processed
