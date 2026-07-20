from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.documento import Documento
from app.domain.colaborador import Colaborador


@dataclass
class Projeto:
    """
    Representa um conjunto de RDOs pertencentes
    ao mesmo contrato/obra.

    É o objeto raiz do sistema.
    """

    codigo: str = ""

    empresa: str = ""

    contrato: str = ""

    obra: str = ""

    documentos: list[Documento] = field(default_factory=list)

    colaboradores: list[Colaborador] = field(default_factory=list)

    # =====================================================

    def adicionar_documento(
        self,
        documento: Documento
    ) -> None:

        self.documentos.append(documento)

    # =====================================================

    def adicionar_colaborador(
        self,
        colaborador: Colaborador
    ) -> None:

        existente = self.buscar_colaborador(
            colaborador.nome
        )

        if existente is None:

            self.colaboradores.append(
                colaborador
            )

            return

        existente.dias.extend(
            colaborador.dias
        )

    # =====================================================

    def buscar_colaborador(
        self,
        nome: str
    ) -> Colaborador | None:

        nome = nome.upper().strip()

        for colaborador in self.colaboradores:

            if colaborador.nome.upper().strip() == nome:

                return colaborador

        return None

    # =====================================================

    @property
    def total_documentos(self):

        return len(self.documentos)

    @property
    def total_colaboradores(self):

        return len(self.colaboradores)