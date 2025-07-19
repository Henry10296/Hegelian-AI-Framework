"""
API routes for decision processing
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
import logging
import asyncio

from backend.models.requests import ProcessDecisionRequest, FeedbackRequest
from backend.models.responses import (
    DecisionResultResponse, ProcessingStatusResponse, 
    DecisionListResponse, FeedbackResponse
)
from backend.dependencies import (
    get_database_manager, get_metrics_collector, 
    get_dialectical_engine, get_current_user
)
from backend.database import DatabaseManager
from backend.monitoring import MetricsCollector
from ai_core.dialectical_engine import DialecticalEngine
from ai_core.models.ethical_case import EthicalCase

logger = logging.getLogger(__name__)

router = APIRouter()

# Store for active processing tasks
active_processes = {}

@router.post("/process", response_model=ProcessingStatusResponse)
async def process_decision(
    request: ProcessDecisionRequest,
    background_tasks: BackgroundTasks,
    db: DatabaseManager = Depends(get_database_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector),
    engine: DialecticalEngine = Depends(get_dialectical_engine),
    user: dict = Depends(get_current_user)
):
    """
    Start processing a decision for an ethical case
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/decisions/process", "method": "POST"})
        
        # Check if case exists
        case_data = await db.get_ethical_case(request.case_id)
        if not case_data:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Convert to EthicalCase object
        case = EthicalCase.from_dict(case_data)
        
        # Generate process ID
        import uuid
        process_id = str(uuid.uuid4())
        
        # Store process info
        active_processes[process_id] = {
            "case_id": request.case_id,
            "status": "pending",
            "stage": "initializing",
            "progress": 0.0,
            "started_at": metrics.get_timestamp(),
            "updated_at": metrics.get_timestamp(),
            "user_id": user.get("id"),
            "options": request.process_options or {}
        }
        
        # Start background processing
        background_tasks.add_task(
            process_decision_background,
            process_id,
            case,
            request,
            engine,
            db,
            metrics
        )
        
        return ProcessingStatusResponse(
            process_id=process_id,
            case_id=request.case_id,
            status="pending",
            stage="initializing",
            progress=0.0,
            started_at=active_processes[process_id]["started_at"],
            updated_at=active_processes[process_id]["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting decision processing: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/decisions/process", "method": "POST"})
        raise HTTPException(status_code=500, detail="Internal server error")

async def process_decision_background(
    process_id: str,
    case: EthicalCase,
    request: ProcessDecisionRequest,
    engine: DialecticalEngine,
    db: DatabaseManager,
    metrics: MetricsCollector
):
    """
    Background task for processing decision
    """
    try:
        # Update status
        active_processes[process_id]["status"] = "processing"
        active_processes[process_id]["stage"] = "thesis"
        active_processes[process_id]["progress"] = 0.1
        active_processes[process_id]["updated_at"] = metrics.get_timestamp()
        
        # Process the case through dialectical engine
        decision_result = await engine.process_ethical_case(case)
        
        # Update final status
        active_processes[process_id]["status"] = "completed"
        active_processes[process_id]["stage"] = "completed"
        active_processes[process_id]["progress"] = 1.0
        active_processes[process_id]["updated_at"] = metrics.get_timestamp()
        active_processes[process_id]["result"] = decision_result
        
        # Record metrics
        metrics.record_decision_processed(
            decision_result.processing_time,
            decision_result.confidence_score,
            case.case_type.value
        )
        
        logger.info(f"Decision processing completed for process {process_id}")
        
    except Exception as e:
        logger.error(f"Error in background decision processing: {e}")
        
        # Update error status
        active_processes[process_id]["status"] = "failed"
        active_processes[process_id]["error_message"] = str(e)
        active_processes[process_id]["updated_at"] = metrics.get_timestamp()
        
        metrics.increment_counter("decision_processing_errors_total", 1)

@router.get("/process/{process_id}/status", response_model=ProcessingStatusResponse)
async def get_processing_status(
    process_id: str,
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Get the status of a decision processing task
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/decisions/process/status", "method": "GET"})
        
        if process_id not in active_processes:
            raise HTTPException(status_code=404, detail="Process not found")
        
        process_info = active_processes[process_id]
        
        # Calculate estimated remaining time
        estimated_remaining_time = None
        if process_info["status"] == "processing":
            # Simple estimation based on progress
            if process_info["progress"] > 0:
                from datetime import datetime
                started = datetime.fromisoformat(process_info["started_at"])
                elapsed = (datetime.now() - started).total_seconds()
                estimated_total = elapsed / process_info["progress"]
                estimated_remaining_time = int(estimated_total - elapsed)
        
        return ProcessingStatusResponse(
            process_id=process_id,
            case_id=process_info["case_id"],
            status=process_info["status"],
            stage=process_info["stage"],
            progress=process_info["progress"],
            estimated_remaining_time=estimated_remaining_time,
            error_message=process_info.get("error_message"),
            started_at=process_info["started_at"],
            updated_at=process_info["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting process status: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/decisions/process/status", "method": "GET"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/process/{process_id}/result", response_model=DecisionResultResponse)
async def get_decision_result(
    process_id: str,
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Get the result of a completed decision processing task
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/decisions/process/result", "method": "GET"})
        
        if process_id not in active_processes:
            raise HTTPException(status_code=404, detail="Process not found")
        
        process_info = active_processes[process_id]
        
        if process_info["status"] != "completed":
            raise HTTPException(status_code=400, detail="Process not completed")
        
        if "result" not in process_info:
            raise HTTPException(status_code=404, detail="Result not found")
        
        decision_result = process_info["result"]
        
        # Convert to response model
        # Note: This is a simplified conversion - in a real implementation,
        # you would need to properly convert the decision result to the response model
        return DecisionResultResponse(
            id=str(decision_result.case_id),
            case_id=decision_result.case_id,
            final_decision=decision_result.final_decision,
            confidence_score=decision_result.confidence_score,
            reasoning_path=decision_result.reasoning_path,
            processing_time=decision_result.processing_time,
            decision_type="approve",  # Default value
            timestamp=metrics.get_timestamp(),
            # TODO: Add proper conversion for complex nested objects
            thesis_result=None,  # Placeholder
            antithesis_result=None,  # Placeholder
            synthesis_result=None,  # Placeholder
            metadata=decision_result.metadata
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting decision result: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/decisions/process/result", "method": "GET"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{decision_id}", response_model=DecisionResultResponse)
async def get_decision(
    decision_id: str,
    db: DatabaseManager = Depends(get_database_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Get a decision result by ID
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/decisions/{id}", "method": "GET"})
        
        decision_data = await db.get_decision_result(decision_id)
        
        if not decision_data:
            raise HTTPException(status_code=404, detail="Decision not found")
        
        # TODO: Convert decision_data to DecisionResultResponse
        # This is a placeholder implementation
        return DecisionResultResponse(
            id=decision_data["id"],
            case_id=decision_data["case_id"],
            final_decision=decision_data["final_decision"],
            confidence_score=decision_data["confidence_score"],
            reasoning_path=decision_data.get("reasoning_path", []),
            processing_time=decision_data["processing_time"],
            decision_type=decision_data.get("decision_type", "approve"),
            timestamp=decision_data["created_at"],
            thesis_result=None,  # Placeholder
            antithesis_result=None,  # Placeholder
            synthesis_result=None,  # Placeholder
            metadata=decision_data.get("metadata", {})
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting decision {decision_id}: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/decisions/{id}", "method": "GET"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/case/{case_id}", response_model=DecisionListResponse)
async def get_decisions_for_case(
    case_id: str,
    db: DatabaseManager = Depends(get_database_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Get all decisions for a specific case
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/decisions/case/{id}", "method": "GET"})
        
        decisions = await db.get_decisions_by_case(case_id)
        
        # Convert to response format
        from backend.models.responses import DecisionSummaryResponse
        decision_summaries = [
            DecisionSummaryResponse(
                id=decision["id"],
                case_id=decision["case_id"],
                final_decision=decision["final_decision"],
                decision_type=decision["decision_type"],
                confidence_score=decision["confidence_score"],
                confidence_level="medium",  # TODO: Calculate from score
                processing_time=decision["processing_time"],
                key_principles=[],  # TODO: Extract from decision
                main_challenges=[],  # TODO: Extract from decision
                resolution_strategy="synthesis",  # TODO: Extract from decision
                consensus_score=0.8,  # TODO: Extract from decision
                timestamp=decision["created_at"]
            )
            for decision in decisions
        ]
        
        return DecisionListResponse(
            decisions=decision_summaries,
            total=len(decision_summaries),
            limit=len(decision_summaries),
            offset=0
        )
        
    except Exception as e:
        logger.error(f"Error getting decisions for case {case_id}: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/decisions/case/{id}", "method": "GET"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{decision_id}/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    decision_id: str,
    request: FeedbackRequest,
    db: DatabaseManager = Depends(get_database_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector),
    user: dict = Depends(get_current_user)
):
    """
    Submit feedback for a decision
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/decisions/{id}/feedback", "method": "POST"})
        
        # Check if decision exists
        decision_data = await db.get_decision_result(decision_id)
        if not decision_data:
            raise HTTPException(status_code=404, detail="Decision not found")
        
        # Generate feedback ID
        import uuid
        feedback_id = str(uuid.uuid4())
        
        # TODO: Save feedback to database
        
        metrics.increment_counter("feedback_submitted_total", 1, {"feedback_type": request.feedback_type})
        
        return FeedbackResponse(
            feedback_id=feedback_id,
            decision_id=decision_id,
            feedback_type=request.feedback_type,
            rating=request.rating,
            comments=request.comments,
            reviewer_role=request.reviewer_role,
            status="pending",
            created_at=metrics.get_timestamp()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting feedback for decision {decision_id}: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/decisions/{id}/feedback", "method": "POST"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{decision_id}/explanation")
async def get_decision_explanation(
    decision_id: str,
    db: DatabaseManager = Depends(get_database_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Get detailed explanation for a decision
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/decisions/{id}/explanation", "method": "GET"})
        
        decision_data = await db.get_decision_result(decision_id)
        if not decision_data:
            raise HTTPException(status_code=404, detail="Decision not found")
        
        # Generate explanation
        explanation = {
            "decision_id": decision_id,
            "case_id": decision_data["case_id"],
            "final_decision": decision_data["final_decision"],
            "confidence_score": decision_data["confidence_score"],
            "reasoning_process": {
                "thesis_stage": "Analysis of existing ethical principles and norms",
                "antithesis_stage": "Generation of opposing viewpoints and challenges",
                "synthesis_stage": "Integration and resolution of conflicting perspectives"
            },
            "key_factors": [
                "Stakeholder interests and impacts",
                "Ethical principles and values",
                "Cultural context and norms",
                "Temporal considerations",
                "Uncertainty and ambiguity levels"
            ],
            "decision_rationale": decision_data.get("reasoning_path", []),
            "limitations": [
                "Based on available information at time of processing",
                "Subject to cultural and contextual biases",
                "Requires human oversight and validation"
            ],
            "recommendations": [
                "Review decision with relevant stakeholders",
                "Monitor implementation and outcomes",
                "Collect feedback for continuous improvement"
            ]
        }
        
        return explanation
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting explanation for decision {decision_id}: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/decisions/{id}/explanation", "method": "GET"})
        raise HTTPException(status_code=500, detail="Internal server error")