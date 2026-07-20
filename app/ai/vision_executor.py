from __future__ import annotations

from app.ai.json_repair import JsonRepair
from app.ai.prompt_manager import PromptManager
from app.ai.qwen_client import QwenClient
from app.ai.response_validator import ResponseValidator
from app.core.logger import logger


class VisionExecutor:
    """
    Responsável por executar o modelo de visão e normalizar a resposta.

    Fluxo:

        PromptManager
              ↓
          QwenClient
              ↓
          JsonRepair
              ↓
      ResponseValidator
              ↓
        Resultado padronizado
    """

    def __init__(self):
        self.qwen = QwenClient()
        self.prompts = PromptManager()
        self.repair = JsonRepair()
        self.validator = ResponseValidator()

    def execute(self, region):

        prompt_name = getattr(region, "prompt", "document")
        prompt = self.prompts.load(prompt_name)

        logger.info(
            "Qwen (imagem): %s",
            region.image_path.name,
        )

        raw = self.qwen.extract_document(
            prompt,
            region.image_path,
        )

        # Corrige respostas parcialmente inválidas
        try:
            data = self.repair.repair(raw)

        except Exception as exc:

            logger.exception(
                "Erro no JsonRepair: %s",
                exc,
            )

            data = {
                "_valid_json": False,
                "_raw": str(raw),
            }

        # Garante estrutura compatível com o prompt
        try:
            data = self.validator.validate(
                prompt_name,
                data,
            )

        except Exception as exc:

            logger.exception(
                "Erro no ResponseValidator: %s",
                exc,
            )

        region_name = getattr(region, "region_type", "document")

        if hasattr(region_name, "value"):
            region_name = region_name.value

        bbox = getattr(region, "bbox", None)

        if isinstance(data, dict):

            data.setdefault("region", region_name)

            if bbox is not None:
                data.setdefault("bbox", bbox)

            return data

        if isinstance(data, list):

            return {
                "region": region_name,
                "bbox": bbox,
                "items": data,
            }

        logger.warning(
            "Resposta do Qwen não pôde ser normalizada."
        )

        return {
            "region": region_name,
            "bbox": bbox,
            "raw_response": str(raw),
            "_valid_json": False,
        }