from __future__ import annotations

import json
import re


class JsonRepair:
    """
    Corrige respostas do Qwen antes do restante da pipeline.

    Trata:

    - markdown ```json
    - texto antes/depois do JSON
    - listas
    - objetos
    """

    def repair(self, value):

        if value is None:
            return {}

        if isinstance(value, (dict, list)):
            return value

        text = str(value).strip()

        # Remove markdown
        text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
        text = re.sub(r"```", "", text)

        text = text.strip()

        # JSON direto
        try:
            return json.loads(text)
        except Exception:
            pass

        # Procura objeto JSON
        match = re.search(r"\{.*\}", text, flags=re.S)

        if match:

            candidate = match.group(0)

            candidate = re.sub(
                r",\s*([\]}])",
                r"\1",
                candidate,
            )

            try:
                return json.loads(candidate)
            except Exception:
                pass

        # Procura lista JSON
        match = re.search(r"\[.*\]", text, flags=re.S)

        if match:

            candidate = match.group(0)

            candidate = re.sub(
                r",\s*([\]}])",
                r"\1",
                candidate,
            )

            try:
                return json.loads(candidate)
            except Exception:
                pass

        return {
            "_valid_json": False,
            "_raw": text,
        }