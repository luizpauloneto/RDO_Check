from __future__ import annotations

from pathlib import Path

import cv2

from app.core.logger import logger
from app.layout.region import Region


class RegionCropper:
    """
    Responsável por recortar regiões detectadas.

    Não conhece IA.

    Não conhece OCR.

    Não conhece RDO.
    """

    # =====================================================
    # Crop
    # =====================================================

    def crop(
        self,
        image_path: Path,
        region: Region,
        output_path: Path
    ) -> Path:

        logger.info(

            f"Crop: {region.kind}"

        )

        image = cv2.imread(

            str(image_path)

        )

        if image is None:

            raise FileNotFoundError(

                image_path

            )

        crop = image[

            region.top:region.bottom,

            region.left:region.right

        ]

        output_path.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        cv2.imwrite(

            str(output_path),

            crop

        )

        region.image = str(output_path)

        return output_path

    # =====================================================
    # Crop múltiplos
    # =====================================================

    def crop_all(
        self,
        image_path: Path,
        regions: list[Region],
        output_directory: Path
    ) -> list[Region]:

        output_directory.mkdir(

            parents=True,

            exist_ok=True

        )

        resultado = []

        for indice, region in enumerate(

            regions,

            start=1

        ):

            nome = (

                f"{indice:03d}_"

                f"{region.kind.lower()}.png"

            )

            destino = output_directory / nome

            self.crop(

                image_path,

                region,

                destino

            )

            resultado.append(

                region

            )

        logger.info(

            f"{len(resultado)} regiões recortadas."

        )

        return resultado