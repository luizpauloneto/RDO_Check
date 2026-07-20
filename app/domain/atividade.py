from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Atividade:
    """
    Representa uma atividade executada
    por um colaborador em um determinado dia.

    Exemplo:

        • Manutenção preventiva
        • Inspeção elétrica
        • Apoio operacional
    """

    descricao: str = ""

    local: str = ""

    equipamento: str = ""

    sistema: str = ""

    observacao: str = ""

    ordens_servico: list[str] = field(default_factory=list)

    equipamentos: list[str] = field(default_factory=list)

    # =====================================================

    def adicionar_os(
        self,
        numero: str
    ) -> None:

        numero = numero.strip()

        if not numero:

            return

        if numero not in self.ordens_servico:

            self.ordens_servico.append(numero)

    # =====================================================

    def adicionar_equipamento(
        self,
        equipamento: str
    ) -> None:

        equipamento = equipamento.strip()

        if not equipamento:

            return

        if equipamento not in self.equipamentos:

            self.equipamentos.append(equipamento)

    # =====================================================

    @property
    def total_os(self) -> int:

        return len(self.ordens_servico)

    # =====================================================

    @property
    def total_equipamentos(self) -> int:

        return len(self.equipamentos)

    # =====================================================

    def to_dict(self) -> dict:

        return {

            "descricao": self.descricao,

            "local": self.local,

            "equipamento": self.equipamento,

            "sistema": self.sistema,

            "observacao": self.observacao,

            "ordens_servico": self.ordens_servico,

            "equipamentos": self.equipamentos

        }

    # =====================================================

    def __str__(self) -> str:

        return (

            f"{self.descricao}"

            if self.descricao

            else "Atividade"

        )