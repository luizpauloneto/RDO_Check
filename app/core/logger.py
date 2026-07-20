from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from app.core.config import settings


logger = logging.getLogger("RDO_Check")

logger.setLevel(logging.INFO)

formatter = logging.Formatter(

    "%(asctime)s | %(levelname)-8s | %(message)s",

    "%d/%m/%Y %H:%M:%S"

)

console = logging.StreamHandler()

console.setFormatter(formatter)

logger.addHandler(console)

file = RotatingFileHandler(

    settings.LOG_DIR / "rdo_check.log",

    maxBytes=10 * 1024 * 1024,

    backupCount=5,

    encoding="utf-8"

)

file.setFormatter(formatter)

logger.addHandler(file)