from __future__ import annotations

import json
from pathlib import Path

from app.core.logger import logger


class DocumentResultBuilder:
    """
    Consolida o resultado final do processamento do documento.
    """

    def build(
        self,
        merged_json: Path,
        parsed_document: dict,
        output_dir: Path,
    ) -> Path:
        result = {
            "metadata": {
                "version": "2.0",
                "generator": "RDO_Check",
            },
            "document": parsed_document,
        }

        if merged_json.exists():
            with merged_json.open("r", encoding="utf-8") as fp:
                pages=json.load(fp)
                result["pages"]=pages.get("pages",[]) if isinstance(pages,dict) else []
        else:
            result["pages"] = []

        output_file = output_dir / "document.json"

        output_dir.mkdir(parents=True, exist_ok=True)

        with output_file.open("w", encoding="utf-8") as fp:
            json.dump(
                result,
                fp,
                indent=4,
                ensure_ascii=False,
            )

        logger.info("Documento consolidado salvo em %s", output_file)

        return output_file
