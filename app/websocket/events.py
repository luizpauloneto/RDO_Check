from __future__ import annotations

from enum import Enum


class Event(str, Enum):

    # =====================================================
    # Sistema
    # =====================================================

    CONNECTED = "connected"

    DISCONNECTED = "disconnected"

    HEARTBEAT = "heartbeat"

    ERROR = "error"

    # =====================================================
    # Job
    # =====================================================

    JOB_CREATED = "job_created"

    JOB_STARTED = "job_started"

    JOB_FINISHED = "job_finished"

    JOB_FAILED = "job_failed"

    JOB_CANCELLED = "job_cancelled"

    # =====================================================
    # Documento
    # =====================================================

    DOCUMENT_OPENED = "document_opened"

    DOCUMENT_FINISHED = "document_finished"

    # =====================================================
    # Página
    # =====================================================

    PAGE_STARTED = "page_started"

    PAGE_FINISHED = "page_finished"

    PAGE_ERROR = "page_error"

    # =====================================================
    # OCR
    # =====================================================

    OCR_STARTED = "ocr_started"

    OCR_FINISHED = "ocr_finished"

    # =====================================================
    # IA
    # =====================================================

    AI_STARTED = "ai_started"

    AI_FINISHED = "ai_finished"

    # =====================================================
    # Layout
    # =====================================================
    
    PAGE_IMAGE = "page_image"

    CROP_FOUND = "crop_found"

    BLOCK_FOUND = "block_found"

    # =====================================================
    # Extrações
    # =====================================================

    EMPLOYEE_FOUND = "employee_found"

    ACTIVITY_FOUND = "activity_found"

    PHOTO_FOUND = "photo_found"

    EQUIPMENT_FOUND = "equipment_found"

    SIGNATURE_FOUND = "signature_found"

    # =====================================================
    # Dashboard
    # =====================================================

    PROGRESS = "progress"

    STATUS = "status"

    LOG = "log"

    GPU = "gpu"
    
    JSON = "json"

    STATISTICS = "statistics"