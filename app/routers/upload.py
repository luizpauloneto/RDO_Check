from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.logger import logger
from app.services.pdf_service import PDFService

router = APIRouter(tags=["Upload"])


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):
    """
    Upload do PDF.

    Nesta Sprint apenas:

        PDF
            ↓
        Salvar
            ↓
        Converter em PNG
            ↓
        Retornar informações
    """

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Arquivo inválido."
        )

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Somente PDFs são aceitos."
        )

    logger.info(
        f"Upload: {file.filename}"
    )

    pdf = PDFService()

    resultado = await pdf.process_upload(file)

    return resultado