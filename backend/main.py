"""
Hegelian AI Framework - Main Application Entry Point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
import logging
from typing import Dict, Any
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_core.dialectical_engine import DialecticalEngine
from ai_core.knowledge_graph import KnowledgeGraphManager
from backend.api.routes import ethical_cases, decisions, analytics
from backend.config import Settings
from backend.database import DatabaseManager
from backend.monitoring import MetricsCollector
from backend.logging_config import setup_logging

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize settings
settings = Settings()

# Global instances
dialectical_engine = None
knowledge_graph_manager = None
database_manager = None
metrics_collector = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global dialectical_engine, knowledge_graph_manager, database_manager, metrics_collector
    
    # Startup
    logger.info("Starting Hegelian AI Framework...")
    
    try:
        # Initialize database
        database_manager = DatabaseManager(settings.database_url)
        await database_manager.initialize()
        
        # Initialize knowledge graph
        knowledge_graph_manager = KnowledgeGraphManager(settings.neo4j_config)
        await knowledge_graph_manager.initialize()
        
        # Initialize dialectical engine
        dialectical_engine = DialecticalEngine(
            knowledge_graph_manager=knowledge_graph_manager,
            database_manager=database_manager
        )
        await dialectical_engine.initialize()
        
        # Initialize metrics collector
        metrics_collector = MetricsCollector()
        
        # Set global instances
        app.state.dialectical_engine = dialectical_engine
        app.state.knowledge_graph_manager = knowledge_graph_manager
        app.state.database_manager = database_manager
        app.state.metrics_collector = metrics_collector
        
        logger.info("Hegelian AI Framework started successfully")
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
    
    # Shutdown
    logger.info("Shutting down Hegelian AI Framework...")
    
    try:
        if dialectical_engine:
            await dialectical_engine.shutdown()
        if knowledge_graph_manager:
            await knowledge_graph_manager.shutdown()
        if database_manager:
            await database_manager.shutdown()
        if metrics_collector:
            await metrics_collector.shutdown()
            
        logger.info("Hegelian AI Framework shut down successfully")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

# Create FastAPI application
app = FastAPI(
    title="Hegelian AI Framework",
    description="A dialectical AI system for ethical decision making",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db_status = await database_manager.check_health() if database_manager else False
        
        # Check knowledge graph connection
        kg_status = await knowledge_graph_manager.check_health() if knowledge_graph_manager else False
        
        # Check dialectical engine
        engine_status = dialectical_engine.is_healthy() if dialectical_engine else False
        
        overall_status = db_status and kg_status and engine_status
        
        return {
            "status": "healthy" if overall_status else "unhealthy",
            "components": {
                "database": "healthy" if db_status else "unhealthy",
                "knowledge_graph": "healthy" if kg_status else "unhealthy",
                "dialectical_engine": "healthy" if engine_status else "unhealthy"
            },
            "timestamp": metrics_collector.get_timestamp() if metrics_collector else None
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

# API endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Hegelian AI Framework",
        "version": "1.0.0",
        "description": "A dialectical AI system for ethical decision making"
    }

@app.get("/api/v1/info")
async def get_system_info():
    """Get system information"""
    return {
        "name": "Hegelian AI Framework",
        "version": "1.0.0",
        "description": "A dialectical AI system for ethical decision making",
        "components": {
            "dialectical_engine": "Implements thesis-antithesis-synthesis reasoning",
            "knowledge_graph": "Dynamic ethical knowledge representation",
            "multi_agent_system": "Human-AI-Regulatory collaboration"
        },
        "endpoints": {
            "health": "/health",
            "cases": "/api/v1/cases",
            "decisions": "/api/v1/decisions",
            "analytics": "/api/v1/analytics"
        }
    }

# Include API routes
app.include_router(ethical_cases.router, prefix="/api/v1/cases", tags=["ethical_cases"])
app.include_router(decisions.router, prefix="/api/v1/decisions", tags=["decisions"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "timestamp": metrics_collector.get_timestamp()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "timestamp": metrics_collector.get_timestamp()}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )