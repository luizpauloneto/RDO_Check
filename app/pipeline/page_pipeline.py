from __future__ import annotations

import json
from pathlib import Path

from app.core.logger import logger
from app.layout.classifier import RegionClassifier
from app.layout.cropper import RegionCropper
from app.layout.detector import LayoutDetector
from app.layout.visualizer import LayoutVisualizer
from app.vision.executor import VisionExecutor
from app.vision.vision_task import VisionTask


class PagePipeline:

    def __init__(self):

        self.detector = LayoutDetector()

        self.classifier = RegionClassifier()

        self.cropper = RegionCropper()

        self.visualizer = LayoutVisualizer()

        self.vision = VisionExecutor()

    # =====================================================

    def process(

        self,

        image_path: Path,

        output_directory: Path,

        page_number: int

    ) -> Path:

        logger.info(f"Página {page_number}")

        #
        # Detectar regiões
        #

        regions = self.detector.detect(

            image_path,

            page_number

        )

        #
        # Aqui futuramente entra EasyOCR
        #

        for region in regions:

            region.kind = "UNKNOWN"

        #
        # Recortar
        #

        crop_dir = output_directory / "crops"

        self.cropper.crop_all(

            image_path,

            regions,

            crop_dir

        )

        #
        # Debug
        #

        self.visualizer.draw(

            image_path,

            regions,

            output_directory / "layout.png"

        )

        resultados = []

        #
        # IA
        #

        for region in regions:

            task = VisionTask(

                page=page_number,

                task_type=region.kind,

                prompt_name=region.kind.lower(),

                image=Path(region.image)

            )

            resultado = self.vision.execute(

                task

            )

            resultados.append(

                resultado.json

            )

        arquivo = (

            output_directory

            / f"page_{page_number:03}.json"

        )

        with open(

            arquivo,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                resultados,

                f,

                indent=4,

                ensure_ascii=False

            )

        return arquivo