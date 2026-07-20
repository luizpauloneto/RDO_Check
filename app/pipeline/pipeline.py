from __future__ import annotations

from pathlib import Path

from app.core.logger import logger
from app.domain.projeto import Projeto
from app.services.pdf_service import PDFService


class Pipeline:
    """
    Pipeline principal do sistema.

    Cada etapa possui uma única responsabilidade.

    Futuramente:

        PDF
            ↓
        PNG
            ↓
        IA
            ↓
        Parser
            ↓
        Projeto
    """

    def __init__(self):

        self.pdf = PDFService()

    # =====================================================
    # Executar Pipeline
    # =====================================================

    async def execute(
        self,
        pdf_path: Path
    ) -> Projeto:

        logger.info("=" * 70)

        logger.info("PIPELINE INICIADO")

        logger.info("=" * 70)

        #
        # Projeto vazio
        #

        projeto = Projeto()

        #
        # 1 - Converter PDF
        #

        job = self.pdf.process_file(
            pdf_path
        )

        logger.info(
            f"Job............. {job.job_id}"
        )

        logger.info(
            f"Páginas......... {job.pages}"
        )

        #
        # As próximas etapas ainda não existem.
        #

        logger.info("Pipeline finalizado.")

        return projeto