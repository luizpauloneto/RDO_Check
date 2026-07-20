from __future__ import annotations

from typing import Any

import requests

from app.core.config import settings
from app.core.logger import logger


class AIEngine:
    """
    Camada de comunicação com o Ollama.

    Responsabilidades:

        - Verificar conexão
        - Listar modelos
        - Verificar se o modelo existe
        - Health Check

    Nesta Sprint NÃO executa prompts.
    """

    def __init__(self):

        self.host = settings.OLLAMA_HOST.rstrip("/")

        self.model = settings.OLLAMA_MODEL

        self.timeout = 30

    # =====================================================
    # HEALTH
    # =====================================================

    def health(self) -> dict:

        try:

            response = requests.get(

                f"{self.host}/api/tags",

                timeout=self.timeout

            )

            response.raise_for_status()

            return {

                "online": True,

                "status_code": response.status_code

            }

        except Exception as e:

            logger.exception("Falha ao conectar ao Ollama.")

            return {

                "online": False,

                "erro": str(e)

            }

    # =====================================================
    # MODELOS
    # =====================================================

    def list_models(self) -> list[str]:

        response = requests.get(

            f"{self.host}/api/tags",

            timeout=self.timeout

        )

        response.raise_for_status()

        data = response.json()

        models = []

        for model in data.get("models", []):

            models.append(

                model.get("name")

            )

        return models

    # =====================================================
    # MODELO DISPONÍVEL
    # =====================================================

    def model_exists(self) -> bool:

        try:

            return self.model in self.list_models()

        except Exception:

            return False

    # =====================================================
    # STATUS
    # =====================================================

    def status(self) -> dict:

        health = self.health()

        if not health["online"]:

            return {

                "online": False,

                "model": self.model,

                "loaded": False

            }

        loaded = self.model_exists()

        return {

            "online": True,

            "model": self.model,

            "loaded": loaded

        }

    # =====================================================
    # TESTE
    # =====================================================

    def test(self) -> bool:

        status = self.status()

        return (

            status["online"]

            and

            status["loaded"]

        )