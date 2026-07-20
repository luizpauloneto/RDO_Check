from __future__ import annotations

from collections import defaultdict

from app.core.logger import logger
from app.domain.colaborador import Colaborador
from app.domain.dia_trabalho import DiaTrabalho
from app.domain.documento import Documento
from app.domain.projeto import Projeto


class Aggregator:
    """
    Consolida diversos Documentos em um único Projeto.

    Responsabilidades:

        - Eliminar colaboradores duplicados
        - Ordenar histórico
        - Consolidar dias
        - Consolidar funções
        - Preparar dados para IA
    """

    # ==========================================================
    # CONSOLIDAR PROJETO
    # ==========================================================

    def aggregate(
        self,
        documentos: list[Projeto]
    ) -> Projeto:

        projeto = Projeto()

        colaboradores: dict[str, Colaborador] = {}

        logger.info(
            "Consolidando projetos..."
        )

        for parcial in documentos:

            #
            # Cabeçalho
            #

            if not projeto.empresa:

                projeto.empresa = parcial.empresa

            if not projeto.contrato:

                projeto.contrato = parcial.contrato

            if not projeto.obra:

                projeto.obra = parcial.obra

            #
            # Documentos
            #

            for documento in parcial.documentos:

                projeto.adicionar_documento(

                    documento

                )

            #
            # Colaboradores
            #

            for colaborador in parcial.colaboradores:

                chave = self._key(

                    colaborador.nome

                )

                if chave not in colaboradores:

                    colaboradores[chave] = colaborador

                    continue

                existente = colaboradores[chave]

                for dia in colaborador.dias:

                    existente.adicionar_dia(

                        dia

                    )

        #
        # Ordenar
        #

        for colaborador in colaboradores.values():

            colaborador.ordenar()

            projeto.adicionar_colaborador(

                colaborador

            )

        logger.info(

            f"{projeto.total_colaboradores} colaboradores consolidados."

        )

        return projeto

    # ==========================================================
    # CHAVE
    # ==========================================================

    def _key(
        self,
        nome: str
    ) -> str:

        return (

            nome

            .upper()

            .strip()

            .replace("  ", " ")

        )