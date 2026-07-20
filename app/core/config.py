from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # ==========================================================
    # Aplicação
    # ==========================================================

    APP_NAME: str = "RDO Check AI"

    VERSION: str = "2.0.0"

    DEBUG: bool = True

    # ==========================================================
    # Diretórios
    # ==========================================================

    ROOT_DIR: Path = Path(__file__).resolve().parents[2]

    APP_DIR: Path = ROOT_DIR / "app"

    UPLOAD_DIR: Path = ROOT_DIR / "uploads"

    PAGE_DIR: Path = ROOT_DIR / "pages"

    OUTPUT_DIR: Path = ROOT_DIR / "output"

    LOG_DIR: Path = ROOT_DIR / "logs"

    MODEL_DIR: Path = ROOT_DIR / "models"

    TEMPLATE_DIR: Path = APP_DIR / "templates"

    STATIC_DIR: Path = APP_DIR / "static"

    # ==========================================================
    # Upload
    # ==========================================================

    MAX_UPLOAD_MB: int = 100

    # ==========================================================
    # Ollama
    # ==========================================================

    OLLAMA_HOST: str = "http://127.0.0.1:11434"

    OLLAMA_MODEL: str = "qwen2.5vl:7b"

    OLLAMA_TIMEOUT: int = 600

    # ==========================================================
    # Vision
    # ==========================================================

    MAX_IMAGE_SIZE: int = 2048

    IMAGE_DPI: int = 300

    # ==========================================================
    # PDF
    # ==========================================================

    PDF_DPI: int = 300

    # ==========================================================
    # Pydantic
    # ==========================================================

    class Config:

        env_file = ".env"

        case_sensitive = False


settings = Settings()


# ==========================================================
# Criar diretórios
# ==========================================================

for directory in (

    settings.UPLOAD_DIR,

    settings.PAGE_DIR,

    settings.OUTPUT_DIR,

    settings.LOG_DIR,

    settings.MODEL_DIR,

):

    directory.mkdir(

        parents=True,

        exist_ok=True

    )