from __future__ import annotations

import json
import time

from app.ai.prompt_manager import PromptManager
from app.ai.qwen_client import QwenClient

from app.vision.provider import VisionProvider
from app.vision.vision_result import VisionResult
from app.vision.vision_task import VisionTask


class QwenProvider(VisionProvider):

    def __init__(self):

        self.client = QwenClient()

        self.prompts = PromptManager()

    def execute(
        self,
        task: VisionTask
    ) -> VisionResult:

        inicio = time.time()

        prompt = self.prompts.load(

            task.prompt_name

        )

        resposta = self.client.chat_image(

            prompt,

            task.image

        )

        try:

            dados = json.loads(

                resposta

            )

            ok = True

        except Exception:

            dados = None

            ok = False

        return VisionResult(

            success=ok,

            task_type=task.task_type,

            page=task.page,

            json=dados,

            raw=resposta,

            elapsed=time.time() - inicio

        )