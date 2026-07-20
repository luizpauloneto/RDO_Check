from __future__ import annotations

import asyncio
import shutil
from pathlib import Path
from threading import Thread

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import settings
from app.core.logger import logger
from app.pipeline.document_pipeline import DocumentPipeline
from app.services.job_service import JobService

router = APIRouter(tags=["Upload"])

job_service = JobService()


# ==========================================================
# Processamento em background
# ==========================================================

async def process_job(job):

    pipeline = DocumentPipeline()

    try:

        await job_service.set_step(

            job,

            "Convertendo PDF",

        )

        await pipeline.execute(

            job,

        )

        await job_service.finish(

            job,

        )

        logger.info(

            "Processamento finalizado: %s",

            job.job_id,

        )

    except Exception as exc:

        logger.exception(exc)

        await job_service.fail(

            job,

            exc,

        )


def run_job(job):

    asyncio.run(

        process_job(

            job,

        )

    )


# ==========================================================
# Upload
# ==========================================================

@router.post("/upload")
async def upload_pdf(

    file: UploadFile = File(...)

):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(

            status_code=400,

            detail="Arquivo deve ser PDF.",

        )

    temp_dir = settings.UPLOAD_DIR / "_temp"

    temp_dir.mkdir(

        parents=True,

        exist_ok=True,

    )

    pdf_temp = temp_dir / file.filename

    with open(

        pdf_temp,

        "wb",

    ) as buffer:

        shutil.copyfileobj(

            file.file,

            buffer,

        )

    job = await job_service.create_job(

        filename=file.filename,

        pdf_temp=pdf_temp,

    )

    Thread(

        target=run_job,

        args=(job,),

        daemon=True,

    ).start()

    return {

        "success": True,

        "job_id": job.job_id,

        "filename": job.filename,

        "status": job.status,

    }