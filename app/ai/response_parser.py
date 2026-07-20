from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json

from app.core.logger import logger

from app.domain.projeto import Projeto
from app.domain.documento import Documento
from app.domain.colaborador import Colaborador
from app.domain.dia_trabalho import DiaTrabalho
from app.domain.atividade import Atividade


class ResponseParser:
    """
    Converte o merged.json produzido pelo
    PageMerger em um objeto Projeto.
    """

    # =====================================================
    # PARSE
    # =====================================================

    def parse(
        self,
        merged_json: Path
    ) -> Projeto:

        logger.info(
            f"Lendo {merged_json.name}"
        )

        with open(
            merged_json,
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        projeto = Projeto()

        documento = Documento()

        projeto.adicionar_documento(
            documento
        )

        colaboradores = {}

        for page in data.get("pages", []):

            #
            # Cabeçalho
            #

            if not projeto.empresa:

                projeto.empresa = page.get(
                    "empresa",
                    ""
                )

            if not projeto.contrato:

                projeto.contrato = page.get(
                    "contrato",
                    ""
                )

            if not projeto.obra:

                projeto.obra = page.get(
                    "obra",
                    ""
                )

            documento.empresa = projeto.empresa
            documento.contrato = projeto.contrato
            documento.obra = projeto.obra

            #
            # Colaboradores
            #

            for item in page.get(
                "colaboradores",
                []
            ):

                nome = item.get(
                    "nome",
                    ""
                ).strip()

                if not nome:

                    continue

                chave = nome.upper()

                if chave not in colaboradores:

                    colaborador = Colaborador()

                    colaborador.nome = nome

                    colaborador.funcao = item.get(
                        "funcao",
                        ""
                    )

                    colaborador.empresa = projeto.empresa

                    colaboradores[chave] = colaborador

                colaborador = colaboradores[chave]

                #
                # Dia
                #

                dia = DiaTrabalho()

                data_txt = item.get(
                    "data",
                    ""
                )

                if data_txt:

                    try:

                        dia.data = datetime.strptime(

                            data_txt,

                            "%d/%m/%Y"

                        ).date()

                    except Exception:

                        pass

                dia.entrada = item.get(
                    "entrada",
                    ""
                )

                dia.saida_intervalo = item.get(
                    "saida_intervalo",
                    ""
                )

                dia.retorno_intervalo = item.get(
                    "retorno_intervalo",
                    ""
                )

                dia.saida = item.get(
                    "saida",
                    ""
                )

                dia.calcular_horas()

                #
                # Atividades
                #

                for atividade_json in item.get(
                    "atividades",
                    []
                ):

                    atividade = Atividade()

                    atividade.descricao = atividade_json.get(
                        "descricao",
                        ""
                    )

                    atividade.local = atividade_json.get(
                        "local",
                        ""
                    )

                    atividade.equipamento = atividade_json.get(
                        "equipamento",
                        ""
                    )

                    atividade.observacao = atividade_json.get(
                        "observacao",
                        ""
                    )

                    for os in atividade_json.get(
                        "ordens_servico",
                        []
                    ):

                        atividade.adicionar_os(
                            str(os)
                        )

                    dia.adicionar_atividade(
                        atividade
                    )

                colaborador.adicionar_dia(
                    dia
                )

        #
        # Adicionar colaboradores
        #

        for colaborador in colaboradores.values():

            projeto.adicionar_colaborador(
                colaborador
            )

        logger.info(
            f"{projeto.total_colaboradores} colaboradores encontrados."
        )

        return projeto