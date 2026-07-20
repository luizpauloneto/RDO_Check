from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

from app.domain.dia_trabalho import DiaTrabalho


@dataclass
class Colaborador:
    """
    Representa um colaborador e todo o seu
    histórico de trabalho extraído dos RDOs.
    """

    # =====================================================
    # Identificação
    # =====================================================

    nome: str = ""

    matricula: str = ""

    cpf: str = ""

    empresa: str = ""

    contratada: str = ""

    funcao: str = ""

    equipe: str = ""

    encarregado: str = ""

    # =====================================================
    # Histórico
    # =====================================================

    dias: list[DiaTrabalho] = field(default_factory=list)

    resumo_ia: str = ""

    alertas: list[str] = field(default_factory=list)

    score_confianca: float = 1.0

    # =====================================================
    # Dias
    # =====================================================

    def adicionar_dia(
        self,
        dia: DiaTrabalho
    ) -> None:

        self.dias.append(dia)

        self.dias.sort(

            key=lambda x: (

                x.data or date.min,

                x.entrada

            )

        )

    # =====================================================
    # Estatísticas
    # =====================================================

    @property
    def total_dias(self) -> int:

        return len(self.dias)

    @property
    def total_atividades(self) -> int:

        total = 0

        for dia in self.dias:

            total += dia.total_atividades

        return total

    @property
    def total_os(self) -> int:

        total = 0

        for dia in self.dias:

            total += dia.total_os

        return total

    @property
    def horas_totais(self) -> str:

        total = timedelta()

        for dia in self.dias:

            if not dia.horas_trabalhadas:

                continue

            try:

                h, m = map(

                    int,

                    dia.horas_trabalhadas.split(":")

                )

                total += timedelta(

                    hours=h,

                    minutes=m

                )

            except Exception:

                continue

        horas = int(

            total.total_seconds() // 3600

        )

        minutos = int(

            (

                total.total_seconds() % 3600

            ) // 60

        )

        return f"{horas:02}:{minutos:02}"

    # =====================================================

    def periodo(self):

        datas = [

            d.data

            for d in self.dias

            if d.data

        ]

        if not datas:

            return None, None

        return min(datas), max(datas)

    # =====================================================

    def to_dict(self):

        inicio, fim = self.periodo()

        return {

            "nome": self.nome,

            "matricula": self.matricula,

            "cpf": self.cpf,

            "empresa": self.empresa,

            "contratada": self.contratada,

            "funcao": self.funcao,

            "equipe": self.equipe,

            "encarregado": self.encarregado,

            "periodo_inicio": (

                inicio.isoformat()

                if inicio

                else None

            ),

            "periodo_fim": (

                fim.isoformat()

                if fim

                else None

            ),

            "dias": [

                d.to_dict()

                for d in self.dias

            ],

            "total_dias": self.total_dias,

            "total_atividades": self.total_atividades,

            "total_os": self.total_os,

            "horas_totais": self.horas_totais,

            "alertas": self.alertas,

            "resumo_ia": self.resumo_ia,

            "score_confianca": self.score_confianca

        }