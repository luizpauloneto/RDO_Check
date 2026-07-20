from __future__ import annotations

from pathlib import Path

from app.ai.vision_executor import VisionExecutor
from app.core.logger import logger
from app.pipeline.assignment_engine import AssignmentEngine
from app.pipeline.employee_extractor import EmployeeExtractor
from app.pipeline.page_analyzer import PageAnalyzer
from app.pipeline.page_result_builder import PageResultBuilder
from app.pipeline.prompt_router import PromptRouter
from app.pipeline.smart_cropper import SmartCropper
from app.pipeline.template_engine import TemplateEngine
from app.websocket.sender import sender


class PageProcessor:

    def __init__(self):

        self.analyzer = PageAnalyzer()

        self.templates = TemplateEngine()

        self.cropper = SmartCropper()

        self.router = PromptRouter()

        self.vision = VisionExecutor()

        self.builder = PageResultBuilder()

        self.assignment = AssignmentEngine()

        self.employee_extractor = EmployeeExtractor()

    async def process(

        self,

        job,

        image_path: Path,

        output_dir: Path,

        page: int,

    ):

        await sender.page_started(

            job,

            page,

        )

        await sender.log(

            job,

            "INFO",

            f"Analisando página {page}",

        )

        info = self.analyzer.analyze(

            image_path

        )
        
        await sender.page_image(

            job,

            page,

            f"/api/jobs/{job.job_id}/pages/{page}",

        )

        templates = self.templates.get(

            info.page_type

        )

        crops = self.cropper.crop(

            image_path=image_path,

            templates=templates,

            output_dir=output_dir / "crops",

        )
        
        for crop in crops:

            await sender.crop_found(

            job,

            {

                "id": crop.get("id") or crop["image_path"].stem,

                "name": crop["name"],

                "image": f"/api/jobs/{job.job_id}/crops/{crop['image_path'].name}",

                "bbox": crop["bbox"],

            },

        )

        await sender.log(

            job,

            "INFO",

            f"{len(crops)} regiões encontradas.",

        )

        results = []

        for crop in crops:

            region_name = crop["name"]

            # ==========================================
            # Colaboradores
            # ==========================================

            if region_name == "employees":

                logger.info(

                    "Extraindo colaboradores linha a linha..."

                )

                employees = self.employee_extractor.extract(

                    employees_image=crop["image_path"],

                    work_dir=output_dir,

                ) or []

                for employee in employees:

                    await sender.employee_found(

                        job,

                        employee,

                    )

                results.append(

                    {

                        "region": "employees",

                        "employees": employees,

                        "bbox": crop["bbox"],

                    }

                )

                continue

            # ==========================================
            # Prompt
            # ==========================================

            prompt = self.router.prompt_name(

                region_name

            )

            region = type(

                "Region",

                (),

                {

                    "prompt": prompt,

                    "region_type": region_name,

                    "image_path": crop["image_path"],

                    "bbox": crop["bbox"],

                },

            )()

            logger.info(

                "Executando %s (%s)",

                crop["image_path"].name,

                region_name,

            )

            await sender.ai_started(job, page)

            try:

                data = self.vision.execute(region)

            finally:

                await sender.ai_finished(job, page)

            if isinstance(

                data,

                dict,

            ) and "region" not in data:

                data["region"] = region_name

            if region_name == "activities" and isinstance(data, dict):

                await sender.activity_found(job, data)

            elif region_name == "photos" and isinstance(data, dict):

                await sender.photo_found(job, data)

            results.append(

                data

            )

        page_result = self.builder.build(

            page=page,

            page_type=info.page_type,

            width=info.width,

            height=info.height,

            results=results,

        )
        
        if info.page_type == "rdo":

            page_result = self.assignment.assign(

                page_result

            )        

        self.builder.save(

            page_result=page_result,

            output_dir=output_dir,

            page=page,

        )

        await sender.json(

            job,

            page_result,

        )    
        
        statistics = {

            "pages": page,

            "employees": len(
                page_result.get("employees", [])
            ),

            "activities": len(
                page_result.get("activities", [])
            ),

            "photos": len(
                page_result.get("photos", [])
            ),

        }

        await sender.statistics(

            job,

            statistics,

)

        await sender.page_finished(

            job,

            page,

        )

        await sender.log(

            job,

            "SUCCESS",

            f"Página {page} concluída.",

        )

        logger.info(

            "Página %s concluída (%s).",

            page,

            info.page_type,

        )

        return page_result