from __future__ import annotations

import re
from pathlib import Path

import cv2


class EmployeeRowValidator:
    """
    Filtra linhas da tabela antes de enviá-las ao Qwen.

    O objetivo é eliminar:

    - cabeçalhos
    - separadores
    - linhas vazias
    - linhas muito pequenas
    - regiões sem texto útil
    """

    INVALID_WORDS = (
        "MÃO DE OBRA",
        "MAO DE OBRA",
        "FISCAL RESPONSÁVEL",
        "FISCAL RESPONSAVEL",
        "FUNÇÃO",
        "FUNCAO",
        "ASSINATURA",
        "ENTRADA",
        "SAÍDA",
        "SAIDA",
        "RETORNO",
        "HORÁRIO",
        "HORARIO",
        "OS/OM",
        "O.S.",
        "O.M.",
    )

    def is_valid(self, image_path: Path) -> bool:

        image = cv2.imread(str(image_path))

        if image is None:
            return False

        h, w = image.shape[:2]

        # linhas muito pequenas
        if h < 35:
            return False

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # pouca informação visual
        pixels = cv2.countNonZero(255 - gray)

        if pixels < (w * h) * 0.01:
            return False

        return True

    def validate_result(self, employee: dict) -> bool:

        if not employee:
            return False

        name = str(employee.get("name", "")).strip().upper()

        role = str(employee.get("role", "")).strip().upper()

        if not name and not role:
            return False

        for word in self.INVALID_WORDS:

            if word in name:
                return False

            if word in role:
                return False

        # nomes extremamente pequenos
        if len(name) < 3:
            return False

        # evita números como nome
        if re.fullmatch(r"[0-9 ]+", name):
            return False

        return True