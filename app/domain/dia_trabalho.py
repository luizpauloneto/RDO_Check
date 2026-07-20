from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from app.domain.atividade import Atividade


@dataclass
class DiaTrabalho:
    """
    Representa um único dia trabalhado
    por um colaborador.
    """

    # =====================================================
    # Identificação
    # =====================================================

    data: date | None = None

    documento_id: str = ""

    empresa: str = ""

    contrato: str = ""

    obra: str = ""

    # =====================================================
    # Jornada
    # =====================================================

    entrada: str = ""

    saida_intervalo: str = ""

    retorno_intervalo: str = ""

    saida: str = ""

    horas_trabalhadas: str = ""

    # =====================================================
    # Função
    # =====================================================

    funcao: str = ""

    equipe: str = ""

    encarregado: str = ""

    # =====================================================
    # Conteúdo
    # =====================================================

    atividades: list[Atividade] = field(default_factory=list)

    observacoes: list[str] = field(default_factory=list)

    assinaturas: list[str] = field(default_factory=list)

    anexos: list[str] = field(default_factory=list)

    # =====================================================
    # IA
    # =====================================================

    resumo_ia: str = ""

    alertas: list[str] = field(default_factory=list)

    score_confianca: float = 1.0

    # =====================================================

    def adicionar_atividade(
        self,
        atividade: Atividade
    ) -> None:

        self.atividades.append(atividade)

    # =====================================================

    def adicionar_observacao(
        self,
        texto: str
    ) -> None:

        texto = texto.strip()

        if texto:

            self.observacoes.append(texto)

    # =====================================================

    def adicionar_alerta(
        self,
        alerta: str
    ) -> None:

        alerta = alerta.strip()

        if alerta:

            self.alertas.append(alerta)

    # =====================================================

    def adicionar_assinatura(
        self,
        assinatura: str
    ) -> None:

        assinatura = assinatura.strip()

        if assinatura:

            self.assinaturas.append(assinatura)

    # =====================================================

    def adicionar_anexo(
        self,
        arquivo: str
    ) -> None:

        arquivo = arquivo.strip()

        if arquivo:

            self.anexos.append(arquivo)

    # =====================================================

    @property
    def total_atividades(self) -> int:

        return len(self.atividades)

    # =====================================================

    @property
    def total_alertas(self) -> int:

        return len(self.alertas)

    # =====================================================

    @property
    def total_os(self) -> int:

        total = 0

        for atividade in self.atividades:

            total += atividade.total_os

        return total

    # =====================================================

    def calcular_horas(self) -> str:
        """
        Calcula automaticamente a jornada
        caso os horários estejam preenchidos.
        """

        try:

            if (
                not self.entrada
                or not self.saida
            ):
                return ""

            entrada = datetime.strptime(
                self.entrada,
                "%H:%M"
            )

            saida = datetime.strptime(
                self.saida,
                "%H:%M"
            )

            total = saida - entrada

            if (
                self.saida_intervalo
                and self.retorno_intervalo
            ):

                almoco_inicio = datetime.strptime(
                    self.saida_intervalo,
                    "%H:%M"
                )

                almoco_fim = datetime.strptime(
                    self.retorno_intervalo,
                    "%H:%M"
                )

                total -= (
                    almoco_fim - almoco_inicio
                )

            horas = int(
                total.total_seconds() // 3600
            )

            minutos = int(
                (
                    total.total_seconds() % 3600
                ) // 60
            )

            self.horas_trabalhadas = (
                f"{horas:02}:{minutos:02}"
            )

            return self.horas_trabalhadas

        except Exception:

            return ""

    # =====================================================

    def to_dict(self) -> dict:

        return {

            "data": (
                self.data.isoformat()
                if self.data
                else None
            ),

            "funcao": self.funcao,

            "entrada": self.entrada,

            "saida_intervalo": self.saida_intervalo,

            "retorno_intervalo": self.retorno_intervalo,

            "saida": self.saida,

            "horas_trabalhadas": self.horas_trabalhadas,

            "atividades": [

                atividade.to_dict()

                for atividade in self.atividades

            ],

            "observacoes": self.observacoes,

            "alertas": self.alertas,

            "resumo_ia": self.resumo_ia,

            "score_confianca": self.score_confianca

        }

    # =====================================================

    def __str__(self) -> str:

        return (

            f"{self.data} "

            f"{self.entrada}-{self.saida}"

        )