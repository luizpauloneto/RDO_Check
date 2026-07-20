from __future__ import annotations

import json
import re

from app.core.logger import logger


class JsonParser:
    """
    Converte a resposta do modelo em um dicionário.

    Remove markdown, blocos ```json```,
    texto antes/depois do JSON e tenta
    recuperar respostas parcialmente válidas.
    """

    # ==========================================================
    # Parse
    # ==========================================================

    def parse(
        self,
        response: str
    ) -> dict:

        if not response:

            return {

                "valid_json": False,

                "error": "Resposta vazia."

            }

        text = response.strip()

        #
        # Remove markdown
        #

        text = re.sub(

            r"^```json",

            "",

            text,

            flags=re.IGNORECASE

        )

        text = re.sub(

            r"^```",

            "",

            text

        )

        text = re.sub(

            r"```$",

            "",

            text

        )

        #
        # Localiza JSON
        #

        inicio = text.find("{")

        fim = text.rfind("}")

        if inicio == -1 or fim == -1:

            return {

                "valid_json": False,

                "raw_response": response

            }

        text = text[inicio:fim + 1]

        try:

            data = json.loads(text.strip())


            if not isinstance(data, dict):
                return {
                    "valid_json": False,
                    "error": "JSON raiz deve ser um objeto.",
                    "raw_response": response,
                }

            data["valid_json"] = True

            return data

        except Exception as e:

            logger.exception(e)

            return {

                "valid_json": False,

                "raw_response": response,

                "error": str(e)

            }