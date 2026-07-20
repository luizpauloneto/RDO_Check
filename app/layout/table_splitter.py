from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from app.core.logger import logger


class TableSplitter:
    """
    Divide uma tabela em linhas.

    Não conhece RDO.

    Apenas encontra linhas horizontais.
    """

    def __init__(self):

        self.min_height = 20

    # =====================================================

    def split(

        self,

        image_path: Path

    ) -> list[tuple[int, int]]:

        image = cv2.imread(

            str(image_path),

            cv2.IMREAD_GRAYSCALE

        )

        if image is None:

            raise FileNotFoundError(

                image_path

            )

        binary = cv2.threshold(

            image,

            0,

            255,

            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU

        )[1]

        projection = np.sum(

            binary,

            axis=1

        )

        linhas = []

        inicio = None

        for y, valor in enumerate(

            projection

        ):

            if valor > 0:

                if inicio is None:

                    inicio = y

            else:

                if inicio is not None:

                    altura = y - inicio

                    if altura >= self.min_height:

                        linhas.append(

                            (inicio, y)

                        )

                    inicio = None

        logger.info(

            f"{len(linhas)} linhas detectadas."

        )

        return linhas