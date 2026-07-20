from __future__ import annotations

import re

from app.core.logger import logger
from app.layout.region import Region


class RegionClassifier:
    """
    Classificador de regiões.

    Utiliza apenas texto OCR.

    Não utiliza IA.
    """

    def __init__(self):

        self.rules = {

            "HEADER": [

                "RELATÓRIO DIÁRIO",

                "RELATORIO DIARIO",

                "RDO",

                "CONTRATO",

                "EMPRESA",

                "OBRA",

                "DATA"

            ],

            "EMPLOYEES": [

                "NOME",

                "FUNÇÃO",

                "FUNCAO",

                "ENTRADA",

                "SAÍDA",

                "SAIDA",

                "MATRÍCULA",

                "MATRICULA"

            ],

            "ACTIVITIES": [

                "ATIVIDADE",

                "ATIVIDADES",

                "SERVIÇO",

                "SERVICO",

                "DESCRIÇÃO",

                "DESCRICAO",

                "EXECUTADO",

                "OBSERVAÇÃO",

                "OBSERVACAO"

            ],

            "SIGNATURES": [

                "ASSINATURA",

                "ASSINATURAS",

                "RESPONSÁVEL",

                "RESPONSAVEL",

                "FISCAL",

                "ENCARREGADO"

            ]

        }

    # =====================================================
    # CLASSIFICAR
    # =====================================================

    def classify(

        self,

        region: Region,

        text: str

    ) -> Region:

        texto = self.normalize(text)

        melhor = "UNKNOWN"

        pontos = 0

        for tipo, palavras in self.rules.items():

            score = 0

            for palavra in palavras:

                if palavra in texto:

                    score += 1

            if score > pontos:

                melhor = tipo

                pontos = score

        region.kind = melhor

        region.confidence = min(

            1.0,

            pontos / 5

        )

        logger.info(

            f"{melhor} ({region.confidence:.2f})"

        )

        return region

    # =====================================================

    @staticmethod

    def normalize(texto: str) -> str:

        texto = texto.upper()

        texto = re.sub(

            r"\s+",

            " ",

            texto

        )

        return texto