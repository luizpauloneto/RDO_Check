from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from app.core.config import settings
from app.core.logger import logger
from app.models.job import Job
from app.models.job import JobStatus
from app.services.pdf_service import PDFService


class JobService:
    """
    Serviço responsável exclusivamente pelo ciclo de vida do Job.

    Responsabilidades:

        • Criar Job
        • Salvar job.json
        • Atualizar status
        • Atualizar progresso
        • Salvar PDF
        • Carregar Job

    Não possui dependência de WebSocket.
    """

    def __init__(self):

        self.pdf = PDFService()

        settings.UPLOAD_DIR.mkdir(

            parents=True,

            exist_ok=True

        )

    # ==========================================================
    # Criar Job
    # ==========================================================

    async def create_job(

        self,

        filename: str,

        pdf_temp: Path

    ) -> Job:

        job = Job(

            job_id=self._generate_id(),

            filename=filename,

            status=JobStatus.CREATED

        )

        upload_dir = self.get_upload_directory(

            job.job_id

        )

        upload_dir.mkdir(

            parents=True,

            exist_ok=True

        )

        shutil.copy2(

            pdf_temp,

            upload_dir / filename

        )

        job.sha256 = self.pdf.calculate_sha256(

            upload_dir / filename

        )

        self.save(job)

        logger.info(

            "Job criado: %s",

            job.job_id

        )

        return job

    # ==========================================================
    # Status
    # ==========================================================

    async def set_status(

        self,

        job: Job,

        status: JobStatus

    ):

        job.status = status

        job.updated_at = datetime.now()

        self.save(job)

    # ==========================================================
    # Etapa
    # ==========================================================

    async def set_step(

        self,

        job: Job,

        step: str

    ):

        job.current_step = step

        job.updated_at = datetime.now()

        self.save(job)

    # ==========================================================
    # Página
    # ==========================================================

    async def set_page(

        self,

        job: Job,

        page: int,

        total_pages: int

    ):

        job.current_page = page

        job.total_pages = total_pages

        if total_pages > 0:

            job.progress = round(

                page * 100 / total_pages,

                2

            )

        else:

            job.progress = 0

        job.updated_at = datetime.now()

        self.save(job)

    # ==========================================================
    # Finalizar
    # ==========================================================

    async def finish(

        self,

        job: Job

    ):

        job.finish()

        self.save(job)

        logger.info(

            "Job finalizado: %s",

            job.job_id

        )

    # ==========================================================
    # Falha
    # ==========================================================

    async def fail(

        self,

        job: Job,

        error: Exception

    ):

        job.status = JobStatus.ERROR

        job.current_step = str(error)

        job.updated_at = datetime.now()

        self.save(job)

        logger.exception(error)

    # ==========================================================
    # Persistência
    # ==========================================================

    def save(

        self,

        job: Job

    ):

        arquivo = (

            self.get_upload_directory(

                job.job_id

            )

            / "job.json"

        )

        # Um nome exclusivo impede que salvamentos concorrentes disputem job.tmp.
        tmp = arquivo.with_name(

            f".{arquivo.stem}.{uuid4().hex}.tmp"

        )

        payload = job.model_dump(

            mode="json"

        )

        # No Windows, leitores e antivírus podem manter job.json aberto por
        # instantes. A trava e as tentativas preservam a gravação atômica.
        with JOB_FILE_LOCK:

            try:

                with open(

                    tmp,

                    "w",

                    encoding="utf-8"

                ) as f:

                    json.dump(

                        payload,

                        f,

                        indent=4,

                        ensure_ascii=False,

                    )

                    f.flush()

                    os.fsync(f.fileno())

                for attempt in range(5):

                    try:

                        os.replace(

                            tmp,

                            arquivo

                        )

                        break

                    except PermissionError:

                        if attempt == 4:

                            raise

                        time.sleep(

                            0.05 * (2 ** attempt)

                        )

            finally:

                if tmp.exists():

                    try:

                        tmp.unlink()

                    except OSError:

                        pass

    def load(

        self,

        job_id: str

    ) -> Job:

        arquivo = (

            self.get_upload_directory(

                job_id

            )

            / "job.json"

        )

        with open(

            arquivo,

            encoding="utf-8"

        ) as f:

            dados = json.load(f)

        return Job.model_validate(

            dados

        )

    # ==========================================================
    # Diretórios
    # ==========================================================

    def get_upload_directory(

        self,

        job_id: str

    ) -> Path:

        path = settings.UPLOAD_DIR / job_id

        path.mkdir(

            parents=True,

            exist_ok=True

        )

        return path

    # ==========================================================
    # ID
    # ==========================================================

    def _generate_id(

        self

    ) -> str:

        return (

            datetime.now().strftime(

                "%Y%m%d_%H%M%S"

            )

            + "_"

            + uuid4().hex[:8]

        )
