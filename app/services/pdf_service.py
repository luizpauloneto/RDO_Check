from __future__ import annotations

import hashlib
from pathlib import Path

import fitz

from app.core.config import settings
from app.core.logger import logger


class PDFService:
    """
    Serviço responsável apenas pelo processamento do PDF.

    Responsabilidades:

        • Converter PDF em PNG
        • Calcular SHA256
        • Informar diretórios

    NÃO:

        • cria Job
        • salva job.json
        • altera status
    """

    def __init__(self):

        settings.PAGE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        settings.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    # =====================================================
    # Converter PDF
    # =====================================================

    def convert_pdf(
        self,
        pdf_path: Path,
        output_dir: Path
    ) -> int:

        if not pdf_path.exists():

            raise FileNotFoundError(pdf_path)

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        logger.info(f"Convertendo PDF: {pdf_path.name}")

        document = fitz.open(pdf_path)

        try:

            for page_number, page in enumerate(document, start=1):

                pix = page.get_pixmap(
                    dpi=settings.PDF_DPI
                )

                output = output_dir / f"page_{page_number:03}.png"

                pix.save(output)

        finally:

            document.close()

        total = len(list(output_dir.glob("page_*.png")))

        logger.info(f"{total} páginas convertidas.")

        return total

    # =====================================================
    # SHA256
    # =====================================================

    def calculate_sha256(
        self,
        file_path: Path
    ) -> str:

        sha = hashlib.sha256()

        with open(file_path, "rb") as f:

            while True:

                bloco = f.read(65536)

                if not bloco:
                    break

                sha.update(bloco)

        return sha.hexdigest()

    # =====================================================
    # Diretórios
    # =====================================================

    def get_pages_directory(
        self,
        job_id: str
    ) -> Path:

        path = settings.PAGE_DIR / job_id

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path

    def get_output_directory(
        self,
        job_id: str
    ) -> Path:

        path = settings.OUTPUT_DIR / job_id

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path