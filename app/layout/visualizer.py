from __future__ import annotations

from pathlib import Path

import cv2

from app.core.logger import logger
from app.layout.region import Region


class LayoutVisualizer:
    """
    Desenha as regiões detectadas sobre a imagem.

    Utilizado apenas para debug.

    Não altera o processamento.
    """

    def __init__(self):

        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.font_scale = 0.55

        self.thickness = 2

    # =====================================================
    # Cor por tipo
    # =====================================================

    def _color(
        self,
        kind: str
    ) -> tuple[int, int, int]:

        colors = {

            "HEADER": (255, 0, 0),

            "EMPLOYEES": (0, 255, 0),

            "ACTIVITIES": (0, 255, 255),

            "SIGNATURES": (255, 0, 255),

            "FOOTER": (255, 255, 0),

            "UNKNOWN": (0, 0, 255)

        }

        return colors.get(

            kind,

            (180, 180, 180)

        )

    # =====================================================
    # Desenhar
    # =====================================================

    def draw(
        self,
        image_path: Path,
        regions: list[Region],
        output_path: Path
    ) -> Path:

        logger.info(

            f"Visualizando {len(regions)} regiões."

        )

        image = cv2.imread(

            str(image_path)

        )

        if image is None:

            raise FileNotFoundError(

                image_path

            )

        for indice, region in enumerate(

            regions,

            start=1

        ):

            color = self._color(

                region.kind

            )

            cv2.rectangle(

                image,

                (region.left, region.top),

                (region.right, region.bottom),

                color,

                2

            )

            texto1 = (

                f"{indice} - {region.kind}"

            )

            texto2 = (

                f"{region.width}x{region.height}"

            )

            texto3 = (

                f"{region.confidence:.2f}"

            )

            y = max(

                25,

                region.top - 8

            )

            cv2.putText(

                image,

                texto1,

                (region.left, y),

                self.font,

                self.font_scale,

                color,

                self.thickness

            )

            cv2.putText(

                image,

                texto2,

                (region.left, y + 20),

                self.font,

                0.45,

                color,

                1

            )

            cv2.putText(

                image,

                texto3,

                (region.left, y + 38),

                self.font,

                0.45,

                color,

                1

            )

        output_path.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        cv2.imwrite(

            str(output_path),

            image

        )

        logger.info(

            f"Imagem salva: {output_path.name}"

        )

        return output_path