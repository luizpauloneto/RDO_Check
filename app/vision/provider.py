from __future__ import annotations

from abc import ABC, abstractmethod

from app.vision.vision_result import VisionResult
from app.vision.vision_task import VisionTask


class VisionProvider(ABC):
    """
    Interface para qualquer modelo multimodal.

    GPT

    Qwen

    Pixtral

    Llama Vision

    Claude Vision
    """

    @abstractmethod
    def execute(
        self,
        task: VisionTask
    ) -> VisionResult:
        ...