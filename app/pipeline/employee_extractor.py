from __future__ import annotations

from pathlib import Path

from app.ai.vision_executor import VisionExecutor
from app.core.logger import logger
from app.pipeline.table_row_splitter import TableRowSplitter


class EmployeeExtractor:
    """
    Extrai colaboradores linha a linha da tabela de mão de obra.
    """

    def __init__(self):
        self.splitter = TableRowSplitter()
        self.vision = VisionExecutor()

    def extract(
        self,
        employees_image: Path,
        work_dir: Path,
    ) -> list[dict]:

        rows_dir = work_dir / "employee_rows"

        rows = self.splitter.split(
            image_path=employees_image,
            output_dir=rows_dir,
        )

        employees = []

        for row in rows:

            logger.info("Extraindo colaborador: %s", row.name)

            region = type(
                "Region",
                (),
                {
                    "prompt": "employees",
                    "region_type": "employee_row",
                    "image_path": row,
                    "bbox": None,
                },
            )()

            result = self.vision.execute(region)

            if isinstance(result, dict):

                if result.get("employees"):
                    employees.extend(result["employees"])

                elif result.get("employee"):
                    employees.append(result["employee"])

        logger.info(
            "%d colaborador(es) extraído(s).",
            len(employees),
        )

        return employees
