"""
API routes for ethical cases management
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
import logging

from backend.models.requests import CreateEthicalCaseRequest, UpdateEthicalCaseRequest
from backend.models.responses import EthicalCaseResponse, EthicalCaseListResponse
from backend.dependencies import get_database_manager, get_metrics_collector
from backend.database import DatabaseManager
from backend.monitoring import MetricsCollector
from ai_core.models.ethical_case import EthicalCase, CaseType, ComplexityLevel, CulturalContext

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=EthicalCaseResponse)
async def create_ethical_case(
    request: CreateEthicalCaseRequest,
    db: DatabaseManager = Depends(get_database_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Create a new ethical case
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/cases", "method": "POST"})
        
        # Convert request to EthicalCase
        case = EthicalCase(
            title=request.title,
            description=request.description,
            case_type=CaseType(request.case_type),
            complexity=ComplexityLevel(request.complexity),
            cultural_context=CulturalContext(request.cultural_context),
            available_options=request.available_options,
            constraints=request.constraints or [],
            time_sensitivity=request.time_sensitivity,
            long_term_impact=request.long_term_impact,
            uncertainty_level=request.uncertainty_level,
            ambiguity_level=request.ambiguity_level,
            created_by=request.created_by,
            tags=request.tags or [],
            metadata=request.metadata or {}
        )
        
        # Add stakeholders
        for stakeholder_data in request.stakeholders or []:
            from ai_core.models.ethical_case import Stakeholder
            stakeholder = Stakeholder(
                name=stakeholder_data.name,
                role=stakeholder_data.role,
                interests=stakeholder_data.interests,
                power_level=stakeholder_data.power_level,
                impact_level=stakeholder_data.impact_level,
                ethical_stance=stakeholder_data.ethical_stance
            )
            case.add_stakeholder(stakeholder)
        
        # Add ethical dimensions
        for dimension_data in request.ethical_dimensions or []:
            from ai_core.models.ethical_case import EthicalDimension
            dimension = EthicalDimension(
                name=dimension_data.name,
                description=dimension_data.description,
                weight=dimension_data.weight,
                values=dimension_data.values,
                conflicts=dimension_data.conflicts or []
            )
            case.add_ethical_dimension(dimension)
        
        # Add contextual factors
        for factor_data in request.contextual_factors or []:
            from ai_core.models.ethical_case import ContextualFactor
            factor = ContextualFactor(
                factor_type=factor_data.factor_type,
                description=factor_data.description,
                influence_level=factor_data.influence_level,
                positive_impact=factor_data.positive_impact,
                related_principles=factor_data.related_principles or []
            )
            case.add_contextual_factor(factor)
        
        # Validate case
        validation_errors = case.validate()
        if validation_errors:
            raise HTTPException(status_code=400, detail={"errors": validation_errors})
        
        # Save to database
        case_id = await db.save_ethical_case(case.to_dict())
        
        # Get saved case
        saved_case_data = await db.get_ethical_case(case_id)
        
        metrics.increment_counter("ethical_cases_created_total", 1, {"case_type": case.case_type.value})
        
        return EthicalCaseResponse(
            id=case_id,
            **saved_case_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating ethical case: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/cases", "method": "POST"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{case_id}", response_model=EthicalCaseResponse)
async def get_ethical_case(
    case_id: str,
    db: DatabaseManager = Depends(get_database_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Get an ethical case by ID
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/cases/{id}", "method": "GET"})
        
        case_data = await db.get_ethical_case(case_id)
        
        if not case_data:
            raise HTTPException(status_code=404, detail="Case not found")
        
        return EthicalCaseResponse(**case_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting ethical case {case_id}: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/cases/{id}", "method": "GET"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=EthicalCaseListResponse)
async def list_ethical_cases(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    case_type: Optional[str] = Query(default=None),
    complexity: Optional[str] = Query(default=None),
    db: DatabaseManager = Depends(get_database_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    List ethical cases with optional filtering
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/cases", "method": "GET"})
        
        cases = await db.list_ethical_cases(
            limit=limit,
            offset=offset,
            case_type=case_type,
            complexity_level=complexity
        )
        
        return EthicalCaseListResponse(
            cases=[EthicalCaseResponse(**case) for case in cases],
            total=len(cases),
            limit=limit,
            offset=offset
        )
        
    except Exception as e:
        logger.error(f"Error listing ethical cases: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/cases", "method": "GET"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{case_id}", response_model=EthicalCaseResponse)
async def update_ethical_case(
    case_id: str,
    request: UpdateEthicalCaseRequest,
    db: DatabaseManager = Depends(get_database_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Update an ethical case
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/cases/{id}", "method": "PUT"})
        
        # Check if case exists
        existing_case = await db.get_ethical_case(case_id)
        if not existing_case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # For now, return the existing case (update logic would go here)
        # TODO: Implement actual update logic
        
        return EthicalCaseResponse(**existing_case)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating ethical case {case_id}: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/cases/{id}", "method": "PUT"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{case_id}")
async def delete_ethical_case(
    case_id: str,
    db: DatabaseManager = Depends(get_database_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Delete an ethical case
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/cases/{id}", "method": "DELETE"})
        
        # Check if case exists
        existing_case = await db.get_ethical_case(case_id)
        if not existing_case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # TODO: Implement actual deletion logic
        
        return {"message": "Case deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting ethical case {case_id}: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/cases/{id}", "method": "DELETE"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{case_id}/conflicts")
async def get_case_conflicts(
    case_id: str,
    db: DatabaseManager = Depends(get_database_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Get ethical conflicts for a specific case
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/cases/{id}/conflicts", "method": "GET"})
        
        # Check if case exists
        case_data = await db.get_ethical_case(case_id)
        if not case_data:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Convert to EthicalCase object
        case = EthicalCase.from_dict(case_data)
        
        # Get ethical tensions
        tensions = case.get_ethical_tensions()
        
        return {
            "case_id": case_id,
            "conflicts": tensions,
            "count": len(tensions)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conflicts for case {case_id}: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/cases/{id}/conflicts", "method": "GET"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{case_id}/complexity-score")
async def get_case_complexity_score(
    case_id: str,
    db: DatabaseManager = Depends(get_database_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Get complexity score for a specific case
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/cases/{id}/complexity-score", "method": "GET"})
        
        # Check if case exists
        case_data = await db.get_ethical_case(case_id)
        if not case_data:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Convert to EthicalCase object
        case = EthicalCase.from_dict(case_data)
        
        # Calculate complexity score
        complexity_score = case.get_complexity_score()
        
        return {
            "case_id": case_id,
            "complexity_score": complexity_score,
            "complexity_level": case.complexity.value,
            "factors": {
                "base_complexity": case.complexity.value,
                "stakeholder_count": len(case.stakeholders),
                "ethical_dimensions": len(case.ethical_dimensions),
                "uncertainty_level": case.uncertainty_level,
                "ambiguity_level": case.ambiguity_level
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting complexity score for case {case_id}: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/cases/{id}/complexity-score", "method": "GET"})
        raise HTTPException(status_code=500, detail="Internal server error")