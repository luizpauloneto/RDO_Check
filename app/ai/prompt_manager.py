from __future__ import annotations

from pathlib import Path

from app.core.config import settings
from app.core.logger import logger


class PromptManager:
    """
    Gerenciador central de prompts.

    Estrutura:

        app/prompts/

            document.txt

            header.txt

            employees.txt

            activities.txt

            equipment.txt

            material.txt

            weather.txt

            observations.txt

            signatures.txt
    """

    def __init__(self):

        self.prompt_dir = settings.APP_DIR / "prompts"

        if not self.prompt_dir.exists():

            raise RuntimeError(

                f"Pasta de prompts não encontrada: {self.prompt_dir}"

            )

        #
        # Cache em memória
        #

        self._cache: dict[str, str] = {}

    # ==========================================================
    # Carregar
    # ==========================================================

    def load(

        self,

        name: str

    ) -> str:

        #
        # Cache
        #

        if name in self._cache:

            return self._cache[name]

        arquivo = self.prompt_dir / f"{name}.txt"

        #
        # Fallback
        #

        if not arquivo.exists():

            logger.warning(

                f"Prompt '{name}' não encontrado. Utilizando document.txt"

            )

            arquivo = self.prompt_dir / "document.txt"

        if not arquivo.exists():

            raise FileNotFoundError(

                "document.txt não encontrado."

            )

        texto = arquivo.read_text(

            encoding="utf-8"

        ).strip()

        self._cache[name] = texto

        logger.info(

            f"Prompt carregado: {arquivo.name}"

        )

        return texto

    # ==========================================================
    # Salvar
    # ==========================================================

    def save(

        self,

        name: str,

        content: str

    ) -> Path:

        arquivo = self.prompt_dir / f"{name}.txt"

        arquivo.write_text(

            content.strip(),

            encoding="utf-8"

        )

        #
        # Atualiza cache
        #

        self._cache[name] = content.strip()

        logger.info(

            f"Prompt salvo: {arquivo.name}"

        )

        return arquivo

    # ==========================================================
    # Existe
    # ==========================================================

    def exists(

        self,

        name: str

    ) -> bool:

        return (

            self.prompt_dir

            / f"{name}.txt"

        ).exists()

    # ==========================================================
    # Listar
    # ==========================================================

    def list(

        self

    ) -> list[str]:

        return sorted(

            arquivo.stem

            for arquivo in self.prompt_dir.glob("*.txt")

        )

    # ==========================================================
    # Remover
    # ==========================================================

    def delete(

        self,

        name: str

    ) -> bool:

        arquivo = self.prompt_dir / f"{name}.txt"

        if not arquivo.exists():

            return False

        arquivo.unlink()

        self._cache.pop(

            name,

            None

        )

        logger.info(

            f"Prompt removido: {arquivo.name}"

        )

        return True

    # ==========================================================
    # Limpar Cache
    # ==========================================================

    def clear_cache(

        self

    ) -> None:

        self._cache.clear()

        logger.info(

            "Cache de prompts limpo."

        )