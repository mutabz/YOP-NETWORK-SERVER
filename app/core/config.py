from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ======================
    # APPLICATION
    # ======================
    APP_NAME: str = "ERP"
    DEBUG: bool = True
    # ======================
    # DATABASE
    # ======================
    DATABASE_URL: str
    # ======================
    # REDIS
    # ======================
    REDIS_URL: str
    # ======================
    # SECURITY
    # ======================
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ALGORITHM: str = "HS256"
    # ======================
    # STORAGE
    # ======================
    STORAGE_PROVIDER: str = "MINIO"
    LOCAL_STORAGE_ROOT: str = "storage"
    # ======================
    # MINIO
    # ======================
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SECURE: bool = False
    MINIO_DEFAULT_BUCKET: str = "erp-storage"


    # ======================
    # MAIL
    # ======================
    MAIL_SERVER: str
    MAIL_PORT: int = 587

    MAIL_USE_TLS: bool = True
    MAIL_USE_SSL: bool = False

    MAIL_USERNAME: str
    MAIL_PASSWORD: str

    MAIL_DEFAULT_SENDER: str


    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()