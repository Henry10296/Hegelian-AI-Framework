"""
Configuration settings for the Hegelian AI Framework
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Dict, Any
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Basic settings
    app_name: str = "Hegelian AI Framework"
    version: str = "1.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    
    # Server settings
    host: str = Field(default="localhost", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # CORS settings
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        env="ALLOWED_ORIGINS"
    )
    
    # Database settings
    database_url: str = Field(
        default="sqlite:///./hegelian_ai.db",
        env="DATABASE_URL"
    )
    
    # Neo4j settings
    neo4j_config: Dict[str, Any] = Field(
        default={
            "uri": "bolt://localhost:7687",
            "username": "neo4j",
            "password": "password"
        }
    )
    
    # Redis settings
    redis_url: str = Field(
        default="redis://localhost:6379",
        env="REDIS_URL"
    )
    
    # JWT settings
    jwt_secret_key: str = Field(
        default="your-secret-key-here",
        env="JWT_SECRET_KEY"
    )
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # AI Model settings
    model_cache_dir: str = Field(
        default="./models",
        env="MODEL_CACHE_DIR"
    )
    
    # Logging settings
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/app.log", env="LOG_FILE")
    
    # Monitoring settings
    prometheus_port: int = Field(default=9090, env="PROMETHEUS_PORT")
    metrics_enabled: bool = Field(default=True, env="METRICS_ENABLED")
    
    # API Rate limiting
    rate_limit_per_minute: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    
    # Security settings
    encryption_key: str = Field(
        default="your-encryption-key-here",
        env="ENCRYPTION_KEY"
    )
    
    # Feature flags
    enable_adversarial_training: bool = Field(default=True, env="ENABLE_ADVERSARIAL_TRAINING")
    enable_multi_agent_system: bool = Field(default=True, env="ENABLE_MULTI_AGENT_SYSTEM")
    enable_blockchain_logging: bool = Field(default=False, env="ENABLE_BLOCKCHAIN_LOGGING")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()

# Environment-specific configurations
class DevelopmentSettings(Settings):
    """Development environment settings"""
    debug: bool = True
    log_level: str = "DEBUG"
    
class ProductionSettings(Settings):
    """Production environment settings"""
    debug: bool = False
    log_level: str = "INFO"
    
class TestingSettings(Settings):
    """Testing environment settings"""
    debug: bool = True
    database_url: str = "sqlite:///:memory:"
    
def get_settings() -> Settings:
    """Get settings based on environment"""
    environment = os.getenv("ENVIRONMENT", "development").lower()
    
    if environment == "production":
        return ProductionSettings()
    elif environment == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()