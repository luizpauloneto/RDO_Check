from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class VisionTask:
    """
    Representa uma tarefa enviada ao modelo multimodal.
    """

    job_id: str = ""

    page: int = 0

    task_type: str = ""

    prompt_name: str = ""

    image: Path | None = None

    context: dict | None = None

    retry: int = 0

    priority: int = 0