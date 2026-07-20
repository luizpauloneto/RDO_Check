from __future__ import annotations

import json

from app.ai.prompt_manager import PromptManager
from app.ai.qwen_client import QwenClient
from app.core.logger import logger
from app.domain.colaborador import Colaborador


class CollaboratorSummary:
    """
    Gera um resumo executivo do histórico
    de um colaborador utilizando o Qwen.

    O modelo não recebe imagens.

    Recebe apenas um JSON consolidado.
    """

    def __init__(self):

        self.client = QwenClient()

        self.prompts = PromptManager()

    # =====================================================
    # GERAR RESUMO
    # =====================================================

    def generate(
        self,
        colaborador: Colaborador
    ) -> str:

        logger.info(

            f"Gerando resumo de {colaborador.nome}"

        )

        prompt = self.prompts.load(
            "summary"
        )

        dados = json.dumps(

            colaborador.to_dict(),

            ensure_ascii=False,

            indent=2

        )

        prompt_final = (

            f"{prompt}\n\n"

            "Dados do colaborador:\n\n"

            f"{dados}"

        )

        resposta = self.client.chat_text(

            prompt_final

        )

        colaborador.resumo_ia = resposta.strip()

        return colaborador.resumo_ia

    # =====================================================
    # GERAR PARA VÁRIOS
    # =====================================================

    def generate_all(
        self,
        colaboradores: list[Colaborador]
    ) -> None:

        total = len(colaboradores)

        logger.info(

            f"Gerando resumo de {total} colaboradores."

        )

        for indice, colaborador in enumerate(

            colaboradores,

            start=1

        ):

            logger.info(

                f"[{indice}/{total}] "

                f"{colaborador.nome}"

            )

            self.generate(

                colaborador

            )