from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    google_api_key: str
    environment: str = "development"
    log_level: str = "INFO"
    cors_origins: str = "*"
    
    @property
    def cors_origins_list(self) -> List[str]:
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()



