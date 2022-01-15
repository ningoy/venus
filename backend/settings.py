from pydantic import BaseSettings


class Settings(BaseSettings):
    absolute_path: str = "/home/ningoy/projects/venus/file_storage"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
