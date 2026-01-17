import os
from pydantic_settings import BaseSettings
 
class Settings(BaseSettings):
    # App
    APP_NAME: str = "OmniMind"
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # API
    PORT_BACKEND: int = int(os.getenv("PORT_BACKEND", 8000))
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/omnimind")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Encryption
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "dev-encryption-key-32-chars-minimum!")
    
    # External APIs
    NEWSAPI_KEY: str = os.getenv("NEWSAPI_KEY", "")
    GOOGLE_SCHOLAR_KEY: str = os.getenv("GOOGLE_SCHOLAR_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    SEMANTIC_SCHOLAR_API_KEY: str = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")
    NCBI_API_KEY: str = os.getenv("NCBI_API_KEY", "")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    ALPHA_VANTAGE_API_KEY: str = os.getenv("ALPHA_VANTAGE_API_KEY", "")
    AUTH0_CLIENT_ID: str = os.getenv("AUTH0_CLIENT_ID", "")
    AUTH0_CLIENT_SECRET: str = os.getenv("AUTH0_CLIENT_SECRET", "")
    AUTH0_DOMAIN: str = os.getenv("AUTH0_DOMAIN", "")
    
    # Search
    ELASTICSEARCH_HOST: str = os.getenv("ELASTICSEARCH_HOST", "localhost")
    ELASTICSEARCH_PORT: int = int(os.getenv("ELASTICSEARCH_PORT", 9200))
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
