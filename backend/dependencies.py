"""
FastAPI dependency injection
"""

from fastapi import Depends, HTTPException, Request
from typing import Optional
import logging

from .database import DatabaseManager
from .monitoring import MetricsCollector
from ai_core.dialectical_engine import DialecticalEngine
from ai_core.knowledge_graph import KnowledgeGraphManager

logger = logging.getLogger(__name__)

def get_database_manager(request: Request) -> DatabaseManager:
    """
    Get database manager instance from app state
    """
    try:
        return request.app.state.database_manager
    except AttributeError:
        logger.error("Database manager not found in app state")
        raise HTTPException(status_code=500, detail="Database not available")

def get_metrics_collector(request: Request) -> MetricsCollector:
    """
    Get metrics collector instance from app state
    """
    try:
        return request.app.state.metrics_collector
    except AttributeError:
        logger.error("Metrics collector not found in app state")
        raise HTTPException(status_code=500, detail="Metrics collector not available")

def get_dialectical_engine(request: Request) -> DialecticalEngine:
    """
    Get dialectical engine instance from app state
    """
    try:
        return request.app.state.dialectical_engine
    except AttributeError:
        logger.error("Dialectical engine not found in app state")
        raise HTTPException(status_code=500, detail="Dialectical engine not available")

def get_knowledge_graph_manager(request: Request) -> KnowledgeGraphManager:
    """
    Get knowledge graph manager instance from app state
    """
    try:
        return request.app.state.knowledge_graph_manager
    except AttributeError:
        logger.error("Knowledge graph manager not found in app state")
        raise HTTPException(status_code=500, detail="Knowledge graph not available")

def get_current_user(request: Request) -> Optional[dict]:
    """
    Get current user from request (placeholder for authentication)
    """
    # TODO: Implement actual user authentication
    # For now, return a mock user
    return {
        "id": "anonymous",
        "name": "Anonymous User",
        "role": "user",
        "permissions": ["read", "write"]
    }

def require_authentication(user: dict = Depends(get_current_user)) -> dict:
    """
    Require user authentication
    """
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

def require_admin_role(user: dict = Depends(require_authentication)) -> dict:
    """
    Require admin role
    """
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    return user

def get_request_id(request: Request) -> str:
    """
    Get or generate request ID for tracing
    """
    return request.headers.get("X-Request-ID", "unknown")

def validate_content_type(request: Request, expected_type: str = "application/json"):
    """
    Validate request content type
    """
    content_type = request.headers.get("content-type", "")
    if expected_type not in content_type:
        raise HTTPException(
            status_code=415,
            detail=f"Content-Type must be {expected_type}"
        )

def check_rate_limit(request: Request) -> bool:
    """
    Check rate limiting (placeholder implementation)
    """
    # TODO: Implement actual rate limiting
    # For now, always return True
    return True

def get_pagination_params(
    limit: int = 20,
    offset: int = 0
) -> dict:
    """
    Get pagination parameters with validation
    """
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100"
        )
    
    if offset < 0:
        raise HTTPException(
            status_code=400,
            detail="Offset must be non-negative"
        )
    
    return {"limit": limit, "offset": offset}

def get_query_filters(request: Request) -> dict:
    """
    Extract query filters from request
    """
    filters = {}
    
    # Extract common filter parameters
    if "case_type" in request.query_params:
        filters["case_type"] = request.query_params["case_type"]
    
    if "complexity" in request.query_params:
        filters["complexity"] = request.query_params["complexity"]
    
    if "cultural_context" in request.query_params:
        filters["cultural_context"] = request.query_params["cultural_context"]
    
    if "created_by" in request.query_params:
        filters["created_by"] = request.query_params["created_by"]
    
    # Date range filters
    if "start_date" in request.query_params:
        filters["start_date"] = request.query_params["start_date"]
    
    if "end_date" in request.query_params:
        filters["end_date"] = request.query_params["end_date"]
    
    return filters