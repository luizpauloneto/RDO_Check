from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class JobStatus(str, Enum):

    CREATED = "created"

    UPLOADED = "uploaded"

    CONVERTED = "converted"

    EXTRACTING = "extracting"

    MERGING = "merging"

    PARSING = "parsing"

    AGGREGATING = "aggregating"

    SUMMARIZING = "summarizing"

    COMPLETED = "completed"

    ERROR = "error"


class Job(BaseModel):
    """
    Representa uma execução completa do pipeline.
    """

    # =====================================================
    # Identificação
    # =====================================================

    job_id: str

    filename: str

    # =====================================================
    # Status
    # =====================================================

    status: JobStatus = JobStatus.CREATED

    # =====================================================
    # Documento
    # =====================================================

    pages: int = 0

    sha256: str = ""

    # =====================================================
    # Progresso
    # =====================================================

    current_page: int = 0

    total_pages: int = 0

    current_step: str = "created"

    progress: float = 0.0

    # =====================================================
    # Resultado
    # =====================================================

    pages_processed: int = 0

    pages_failed: int = 0

    collaborators_found: int = 0

    activities_found: int = 0

    os_found: int = 0

    # =====================================================
    # Erros
    # =====================================================

    error_message: str = ""

    # =====================================================
    # Tempo
    # =====================================================

    created_at: datetime = Field(
        default_factory=datetime.now
    )

    updated_at: datetime = Field(
        default_factory=datetime.now
    )

    started_at: datetime | None = None

    finished_at: datetime | None = None

    # =====================================================
    # Métodos
    # =====================================================

    def set_step(
        self,
        step: str
    ) -> None:

        self.current_step = step

        self.updated_at = datetime.now()

    # =====================================================

    def update_progress(
        self,
        page: int,
        total: int
    ) -> None:

        self.current_page = page

        self.total_pages = total

        if total > 0:

            self.progress = round(

                page * 100 / total,

                2

            )

        self.updated_at = datetime.now()

    # =====================================================

    def finish(self) -> None:

        self.status = JobStatus.COMPLETED

        self.progress = 100.0

        self.finished_at = datetime.now()

        self.updated_at = datetime.now()

    # =====================================================

    def fail(
        self,
        message: str
    ) -> None:

        self.status = JobStatus.ERROR

        self.error_message = message

        self.finished_at = datetime.now()

        self.updated_at = datetime.now()