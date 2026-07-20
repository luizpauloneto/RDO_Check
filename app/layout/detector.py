from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from app.core.logger import logger
from app.layout.region import Region


class LayoutDetector:
    """
    Detector genérico de regiões.

    Responsabilidades:

        - Encontrar a folha
        - Encontrar linhas
        - Encontrar blocos
        - Retornar regiões

    Não conhece RDO.
    Não conhece OCR.
    Não conhece IA.
    """

    def __init__(self):

        self.min_region_height = 40

        self.min_region_width = 300

    # =====================================================
    # Detectar
    # =====================================================

    def detect(
        self,
        image_path: Path,
        page: int = 1
    ) -> list[Region]:

        logger.info(

            f"Detectando layout: {image_path.name}"

        )

        image = cv2.imread(

            str(image_path)

        )

        if image is None:

            raise FileNotFoundError(

                image_path

            )

        gray = cv2.cvtColor(

            image,

            cv2.COLOR_BGR2GRAY

        )

        #
        # Binarização
        #

        binary = cv2.threshold(

            gray,

            0,

            255,

            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU

        )[1]

        #
        # Kernel horizontal
        #

        kernel = cv2.getStructuringElement(

            cv2.MORPH_RECT,

            (120, 1)

        )

        horizontal = cv2.morphologyEx(

            binary,

            cv2.MORPH_OPEN,

            kernel,

            iterations=2

        )

        #
        # Contornos
        #

        contours, _ = cv2.findContours(

            horizontal,

            cv2.RETR_EXTERNAL,

            cv2.CHAIN_APPROX_SIMPLE

        )

        regions = []

        for contour in contours:

            x, y, w, h = cv2.boundingRect(

                contour

            )

            if w < self.min_region_width:

                continue

            if h < self.min_region_height:

                continue

            region = Region(

                page=page,

                kind="UNKNOWN",

                x=x,

                y=y,

                width=w,

                height=h,

                confidence=1.0

            )

            regions.append(

                region

            )

        regions.sort(

            key=lambda r: r.y

        )

        logger.info(

            f"{len(regions)} regiões encontradas."

        )

        return regions