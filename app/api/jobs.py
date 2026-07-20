from __future__ import annotations

import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.core.config import settings
from app.services.job_service import JobService
from app.services.pdf_service import PDFService

router = APIRouter(
    tags=["Jobs"]
)

job_service = JobService()
pdf_service = PDFService()


# =====================================================
# LISTA DE JOBS
# =====================================================

@router.get("/jobs")
async def jobs():

    resultado = []

    if not settings.UPLOAD_DIR.exists():

        return resultado

    for pasta in sorted(settings.UPLOAD_DIR.iterdir()):

        if not pasta.is_dir():

            continue

        arquivo = pasta / "job.json"

        if not arquivo.exists():

            continue

        try:

            with open(

                arquivo,

                encoding="utf-8"

            ) as f:

                resultado.append(

                    json.load(f)

                )

        except json.JSONDecodeError:

            # Job ainda está sendo gravado
            continue

    resultado.sort(

        key=lambda x: x.get("created_at", ""),

        reverse=True

    )

    return resultado


# =====================================================
# JOB
# =====================================================

@router.get("/jobs/{job_id}")
async def job(job_id: str):

    arquivo = (

        settings.UPLOAD_DIR

        / job_id

        / "job.json"

    )

    if not arquivo.exists():

        raise HTTPException(

            status_code=404,

            detail="Job não encontrado."

        )

    try:

        with open(

            arquivo,

            encoding="utf-8"

        ) as f:

            return json.load(f)

    except json.JSONDecodeError:

        raise HTTPException(

            status_code=503,

            detail="Job em atualização. Tente novamente."

        )


# =====================================================
# PDF
# =====================================================

@router.get("/jobs/{job_id}/pdf")
async def job_pdf(job_id: str):

    try:

        job = job_service.load(job_id)

    except FileNotFoundError:

        raise HTTPException(

            status_code=404,

            detail="Job não encontrado."

        )

    pdf = (

        job_service.get_upload_directory(job_id)

        / job.filename

    )

    if not pdf.exists():

        raise HTTPException(

            status_code=404,

            detail="PDF não encontrado."

        )

    return FileResponse(

        pdf,

        media_type="application/pdf",

        filename=job.filename,

    )


# =====================================================
# PÁGINA PNG
# =====================================================

@router.get("/jobs/{job_id}/pages/{page}")
async def page_image(

    job_id: str,

    page: int,

):

    image = (

        pdf_service.get_pages_directory(job_id)

        / f"page_{page:03}.png"

    )

    if not image.exists():

        raise HTTPException(

            status_code=404,

            detail="Página não encontrada."

        )

    return FileResponse(

        image,

        media_type="image/png",

    )


# =====================================================
# CROP
# =====================================================

@router.get("/jobs/{job_id}/crops/{filename}")
async def crop(

    job_id: str,

    filename: str,

):

    image = (

        pdf_service.get_output_directory(job_id)

        / "crops"

        / filename

    )

    if not image.exists():

        raise HTTPException(

            status_code=404,

            detail="Crop não encontrado."

        )

    return FileResponse(

        image,

        media_type="image/png",

    )


# =====================================================
# JSON DA PÁGINA
# =====================================================

@router.get("/jobs/{job_id}/json/{page}")
async def page_json(

    job_id: str,

    page: int,

):

    arquivo = (

        pdf_service.get_output_directory(job_id)

        / f"page_{page:03}.json"

    )

    if not arquivo.exists():

        raise HTTPException(

            status_code=404,

            detail="JSON não encontrado."

        )

    try:

        with open(

            arquivo,

            encoding="utf-8"

        ) as f:

            return json.load(f)

    except json.JSONDecodeError:

        raise HTTPException(

            status_code=503,

            detail="JSON ainda está sendo gravado."

        )