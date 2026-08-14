"""Recall AI 智能错题本 - 应用配置"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    APP_NAME: str = "Recall API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./recall.db"

    # DeepSeek API（通过硅基流动 SiliconFlow 调用，密钥放在后端）
    DEEPSEEK_API_KEY: str = "sk-uelextdricugtbjxnfkdiqfcbzhnfdermkyvrqwmlzbljfdl"
    DEEPSEEK_BASE_URL: str = "https://api.siliconflow.cn/v1"
    DEEPSEEK_MODEL: str = "deepseek-ai/DeepSeek-V4-Flash"

    # ChromaDB
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    CHROMA_COLLECTION: str = "mistakes"

    # OCR
    OCR_LANG: str = "ch"

    # Export
    EXPORT_DIR: str = "./exports"

    # CORS（开发环境放开，生产请收紧到具体域名）
    CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Ensure directories exist
Path(settings.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.EXPORT_DIR).mkdir(parents=True, exist_ok=True)
