from __future__ import annotations

from typing import Any

from app.core.logger import logger
from app.websocket.events import Event
from app.websocket.manager import manager


class WebSocketSender:
    """
    Camada responsável pelo envio de eventos WebSocket.

    Todos os eventos são enviados em broadcast para os clientes
    conectados.
    """

    # =====================================================
    # Método Base
    # =====================================================

    async def send(

        self,

        event: Event,

        **data: Any,

    ):

        message = {

            "event": event.value,

            **data,

        }

        logger.info(

            "WS SEND -> %s",

            message,

        )

        await manager.broadcast(

            message,

        )

    # =====================================================
    # JOB
    # =====================================================

    async def job_created(

        self,

        job,

    ):

        await self.send(

            Event.JOB_CREATED,

            job_id=job.job_id,

            filename=job.filename,

            status=job.status.value,

        )

    async def job_started(

        self,

        job,

    ):

        await self.send(

            Event.JOB_STARTED,

            job_id=job.job_id,

            filename=job.filename,

            status=job.status.value,

        )

    async def job_finished(

        self,

        job,

    ):

        await self.send(

            Event.JOB_FINISHED,

            job_id=job.job_id,

            filename=job.filename,

            status=job.status.value,

        )

    async def job_failed(

        self,

        job,

        error: str,

    ):

        await self.send(

            Event.JOB_FAILED,

            job_id=job.job_id,

            filename=job.filename,

            status=job.status.value,

            error=str(error),

        )

    # =====================================================
    # PROGRESSO
    # =====================================================

    async def progress(

        self,

        job,

        current: int,

        total: int,

    ):

        percent = 0

        if total > 0:

            percent = round(

                current * 100 / total,

                2,

            )

        await self.send(

            Event.PROGRESS,

            job_id=job.job_id,

            page=current,

            total=total,

            percent=percent,

        )

    # =====================================================
    # PÁGINAS
    # =====================================================

    async def page_started(

        self,

        job,

        page: int,

    ):

        await self.send(

            Event.PAGE_STARTED,

            job_id=job.job_id,

            page=page,

        )

    async def page_finished(

        self,

        job,

        page: int,

    ):

        await self.send(

            Event.PAGE_FINISHED,

            job_id=job.job_id,

            page=page,

        )

    # =====================================================
    # OCR
    # =====================================================

    async def ocr_started(

        self,

        job,

        page: int,

    ):

        await self.send(

            Event.OCR_STARTED,

            job_id=job.job_id,

            page=page,

        )

    async def ocr_finished(

        self,

        job,

        page: int,

    ):

        await self.send(

            Event.OCR_FINISHED,

            job_id=job.job_id,

            page=page,

        )

    # =====================================================
    # IA
    # =====================================================

    async def ai_started(

        self,

        job,

        page: int,

    ):

        await self.send(

            Event.AI_STARTED,

            job_id=job.job_id,

            page=page,

        )

    async def ai_finished(

        self,

        job,

        page: int,

    ):

        await self.send(

            Event.AI_FINISHED,

            job_id=job.job_id,

            page=page,

        )

    # =====================================================
    # EXTRAÇÕES
    # =====================================================

    async def employee_found(

        self,

        job,

        employee: dict,

    ):

        await self.send(

            Event.EMPLOYEE_FOUND,

            job_id=job.job_id,

            employee=employee,

        )

    async def activity_found(

        self,

        job,

        activity: dict,

    ):

        await self.send(

            Event.ACTIVITY_FOUND,

            job_id=job.job_id,

            activity=activity,

        )

    async def photo_found(

        self,

        job,

        photo: dict,

    ):

        await self.send(

            Event.PHOTO_FOUND,

            job_id=job.job_id,

            photo=photo,

        )

    # =====================================================
    # RESULTADOS
    # =====================================================

    async def page_image(

        self,

        job,

        page: int,

        image: str,

    ):

        await self.send(

            Event.PAGE_IMAGE,

            job_id=job.job_id,

            page=page,

            image=image,

        )

    async def crop_found(

        self,

        job,

        crop: dict,

    ):

        await self.send(

            Event.CROP_FOUND,

            job_id=job.job_id,

            crop=crop,

        )

    async def json(

        self,

        job,

        data: dict,

    ):

        await self.send(

            Event.JSON,

            job_id=job.job_id,

            json=data,

        )

    async def statistics(

        self,

        job,

        statistics: dict,

    ):

        await self.send(

            Event.STATISTICS,

            job_id=job.job_id,

            **statistics,

        )

    # =====================================================
    # LOG
    # =====================================================

    async def log(

        self,

        job,

        level: str,

        message: str,

    ):

        await self.send(

            Event.LOG,

            job_id=job.job_id,

            level=level,

            message=message,

        )

    # =====================================================
    # GPU
    # =====================================================

    async def gpu(

        self,

        usage: float,

        memory: float,

        temperature: float,

    ):

        await self.send(

            Event.GPU,

            usage=usage,

            memory=memory,

            temperature=temperature,

        )


sender = WebSocketSender()