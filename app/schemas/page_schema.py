from __future__ import annotations

from pydantic import BaseModel, Field


class ActivitySchema(BaseModel):

    descricao: str = ""

    local: str = ""

    equipamento: str = ""

    observacao: str = ""

    ordens_servico: list[str] = Field(default_factory=list)


class CollaboratorSchema(BaseModel):

    nome: str = ""

    funcao: str = ""

    data: str = ""

    entrada: str = ""

    saida_intervalo: str = ""

    retorno_intervalo: str = ""

    saida: str = ""

    atividades: list[ActivitySchema] = Field(default_factory=list)


class PageSchema(BaseModel):

    page: int = 0

    empresa: str = ""

    contrato: str = ""

    obra: str = ""

    fiscal: str = ""

    contratada: str = ""

    colaboradores: list[CollaboratorSchema] = Field(default_factory=list)