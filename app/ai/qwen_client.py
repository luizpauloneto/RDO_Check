from __future__ import annotations

import base64
from pathlib import Path

import requests

from app.core.config import settings
from app.core.logger import logger


class QwenClient:
    """
    Cliente oficial do Ollama.

    Toda comunicação com o modelo passa por aqui.

    Responsabilidades:

        • Health Check
        • Chat por texto
        • Chat por imagem
        • Extração de documentos
        • Resumos
    """

    def __init__(self):

        host = str(settings.OLLAMA_HOST).strip()

        # Nunca utilizar 0.0.0.0 como cliente HTTP.
        if host.startswith("0.0.0.0"):
            host = host.replace("0.0.0.0", "127.0.0.1", 1)

        if not host.startswith(("http://", "https://")):
            host = "http://" + host

        self.host = host.rstrip("/")

        self.model = settings.OLLAMA_MODEL

        self.url = f"{self.host}/api/chat"

        logger.info("Ollama URL: %s", self.url)

        self.timeout = (
            settings.OLLAMA_TIMEOUT
            if hasattr(settings, "OLLAMA_TIMEOUT")
            else 600
        )

    # =====================================================
    # HEALTH
    # =====================================================

    def health(self) -> bool:

        try:

            response = requests.get(
                

                f"{self.host}/api/tags",

                timeout=10

            )

            response.raise_for_status()

            return True

        except Exception:

            return False

    # =====================================================
    # IMAGE -> BASE64
    # =====================================================

    def _encode_image(
        self,
        image_path: Path
    ) -> str:

        with open(image_path, "rb") as f:

            return base64.b64encode(

                f.read()

            ).decode("utf-8")

    # =====================================================
    # CHAT TEXTO
    # =====================================================

    def chat_text(
        self,
        prompt: str
    ) -> str:

        logger.info("Qwen (texto)")

        payload = {

            "model": self.model,

            "stream": False,

            "messages": [

                {

                    "role": "user",

                    "content": prompt

                }

            ]

        }

        response = requests.post(

            self.url,

            json=payload,

            timeout=self.timeout

        )

        response.raise_for_status()

        data = response.json()

        return (

            data

            .get("message", {})

            .get("content", "")

        )

    # =====================================================
    # CHAT IMAGEM
    # =====================================================

    def chat_image(
        self,
        prompt: str,
        image_path: Path
    ) -> str:

        logger.info(

            f"Qwen (imagem): {image_path.name}"

        )

        image = self._encode_image(

            image_path

        )

        payload = {

            "model": self.model,

            "stream": False,

            "messages": [

                {

                    "role": "user",

                    "content": prompt,

                    "images": [

                        image

                    ]

                }

            ]

        }

        response = requests.post(

            self.url,

            json=payload,

            timeout=self.timeout

        )

        response.raise_for_status()

        data = response.json()

        return (

            data

            .get("message", {})

            .get("content", "")

        )

    # =====================================================
    # EXTRAIR DOCUMENTO
    # =====================================================

    def extract_document(
        self,
        prompt: str,
        image_path: Path
    ) -> str:

        return self.chat_image(

            prompt,

            image_path

        )

    # =====================================================
    # RESUMO
    # =====================================================

    def summarize(
        self,
        prompt: str
    ) -> str:

        return self.chat_text(

            prompt

        )