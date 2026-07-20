from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(slots=True)
class PromptInfo:
    region: str
    prompt_name: str
    description: str


class PromptRouter:
    """
    Centraliza a escolha do prompt para cada região.

    A saída deste componente será utilizada pelo VisionExecutor.
    """

    def __init__(self) -> None:

        self._routes: Dict[str, PromptInfo] = {

            "header": PromptInfo(
                region="header",
                prompt_name="header",
                description="Extrai cabeçalho do RDO.",
            ),

            "employees": PromptInfo(
                region="employees",
                prompt_name="employees",
                description="Extrai colaboradores e jornadas.",
            ),

            "activities": PromptInfo(
                region="activities",
                prompt_name="activities",
                description="Extrai atividades executadas.",
            ),

            "equipment": PromptInfo(
                region="equipment",
                prompt_name="equipment",
                description="Extrai equipamentos utilizados.",
            ),

            "material": PromptInfo(
                region="material",
                prompt_name="material",
                description="Extrai materiais utilizados.",
            ),

            "weather": PromptInfo(
                region="weather",
                prompt_name="weather",
                description="Extrai condições climáticas.",
            ),

            "observations": PromptInfo(
                region="observations",
                prompt_name="observations",
                description="Extrai observações.",
            ),

            "attendance": PromptInfo(
                region="attendance",
                prompt_name="employees",
                description="Extrai lista de presença.",
            ),

            "photos": PromptInfo(
                region="photos",
                prompt_name="document",
                description="Analisa páginas fotográficas.",
            ),

            "signatures": PromptInfo(
                region="signatures",
                prompt_name="signatures",
                description="Identifica assinaturas.",
            ),

            "document": PromptInfo(
                region="document",
                prompt_name="document",
                description="Fallback.",
            ),
        }

    def get(self, region_name: str) -> PromptInfo:
        return self._routes.get(
            region_name,
            self._routes["document"],
        )

    def prompt_name(self, region_name: str) -> str:
        return self.get(region_name).prompt_name

    def description(self, region_name: str) -> str:
        return self.get(region_name).description
