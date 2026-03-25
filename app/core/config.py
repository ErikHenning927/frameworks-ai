from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Agents Framework"
    VERSION: str = "1.0.0"
    OPENAI_API_KEY: str = "" # Fallback para dev. Configure a var de ambiente OPENAI_API_KEY

    class Config:
        env_file = ".env"

settings = Settings()
