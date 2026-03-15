from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  model_config = SettingsConfigDict(
      env_file=".env",
      env_file_encoding="utf-8",
      extra="ignore",
  )

  app_name: str = Field(
      default="MDLand Eligibility Prototype API",
      validation_alias="APP_NAME",
  )
  app_version: str = Field(default="0.1.0", validation_alias="APP_VERSION")
  app_env: str = Field(default="development", validation_alias="APP_ENV")
  app_host: str = Field(default="0.0.0.0", validation_alias="APP_HOST")
  app_port: int = Field(default=8000, validation_alias="APP_PORT")
  api_prefix: str = Field(default="/api", validation_alias="API_PREFIX")
  debug: bool = Field(default=True, validation_alias="APP_DEBUG")
  upload_dir: str = Field(default="./uploads", validation_alias="UPLOAD_DIR")
  cors_origins: str = Field(
      default="http://localhost:5173",
      validation_alias="CORS_ORIGINS",
  )
  log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")

  @property
  def cors_origin_list(self) -> list[str]:
      return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
  return Settings()
