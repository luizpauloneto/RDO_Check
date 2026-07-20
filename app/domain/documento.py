from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from app.domain.atividade import Atividade


@dataclass
class Documento:
    """
    Representa um único RDO.

    Um Projeto poderá possuir diversos Documentos.
    """

    id: str = ""

    arquivo: str = ""

    caminho_pdf: Path | None = None

    pasta_paginas: Path | None = None

    empresa: str = ""

    contrato: str = ""

    obra: str = ""

    numero_rdo: str = ""

    data: date | None = None

    contratada: str = ""

    fiscal: str = ""

    paginas: int = 0

    hash_sha256: str = ""

    atividades: list[Atividade] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    # =====================================================

    def adicionar_atividade(
        self,
        atividade: Atividade
    ) -> None:

        self.atividades.append(atividade)

    # =====================================================

    @property
    def total_atividades(self) -> int:

        return len(self.atividades)

    # =====================================================

    def to_dict(self) -> dict:

        return {

            "id": self.id,

            "arquivo": self.arquivo,

            "empresa": self.empresa,

            "contrato": self.contrato,

            "obra": self.obra,

            "numero_rdo": self.numero_rdo,

            "data": self.data.isoformat() if self.data else None,

            "contratada": self.contratada,

            "fiscal": self.fiscal,

            "paginas": self.paginas,

            "hash_sha256": self.hash_sha256,

            "total_atividades": self.total_atividades

        }

    # =====================================================

    def __str__(self) -> str:

        return (

            f"Documento("

            f"arquivo='{self.arquivo}', "

            f"data={self.data}, "

            f"paginas={self.paginas})"

        )