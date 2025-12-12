from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_url: str
    master_db_name: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()