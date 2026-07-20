from __future__ import annotations

import json
from pathlib import Path

from app.ai.prompt_manager import PromptManager
from app.ai.qwen_client import QwenClient
from app.core.logger import logger


class PageExtractor:
    """
    Extrai as informações de UMA página utilizando
    o modelo Qwen2.5-VL.

    Entrada:

        page_001.png

    Saída:

        page_001.json
    """

    def __init__(self):

        self.qwen = QwenClient()

        self.prompts = PromptManager()

    # =====================================================
    # Extrair Página
    # =====================================================

    def extract(
        self,
        image_path: Path,
        output_json: Path
    ) -> Path:

        logger.info(

            f"Extraindo {image_path.name}"

        )

        prompt = self.prompts.load(

            "document"

        )

        resposta = self.qwen.extract_document(

            prompt,

            image_path

        )

        output_json.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        try:

            dados = json.loads(

                resposta

            )

        except Exception:

            dados = {

                "page": image_path.stem,

                "raw_response": resposta,

                "valid_json": False

            }

        with open(

            output_json,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                dados,

                f,

                indent=4,

                ensure_ascii=False

            )

        logger.info(

            f"JSON salvo: {output_json.name}"

        )

        return output_json