"""
API routes for analytics and metrics
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from backend.models.requests import AnalyticsRequest
from backend.models.responses import (
    AnalyticsResponse, MetricsResponse, 
    KnowledgeGraphStatsResponse, SystemInfoResponse
)
from backend.dependencies import (
    get_database_manager, get_metrics_collector,
    get_knowledge_graph_manager, get_current_user
)
from backend.database import DatabaseManager
from backend.monitoring import MetricsCollector
from ai_core.knowledge_graph import KnowledgeGraphManager

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/metrics", response_model=MetricsResponse)
async def get_system_metrics(
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Get current system metrics
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/analytics/metrics", "method": "GET"})
        
        system_metrics = await metrics.get_metrics()
        
        return MetricsResponse(**system_metrics)
        
    except Exception as e:
        logger.error(f"Error getting system metrics: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/analytics/metrics", "method": "GET"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health-metrics")
async def get_health_metrics(
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Get health-related metrics
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/analytics/health-metrics", "method": "GET"})
        
        health_metrics = await metrics.get_health_metrics()
        
        return health_metrics
        
    except Exception as e:
        logger.error(f"Error getting health metrics: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/analytics/health-metrics", "method": "GET"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/database-stats")
async def get_database_statistics(
    db: DatabaseManager = Depends(get_database_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Get database statistics
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/analytics/database-stats", "method": "GET"})
        
        db_stats = await db.get_analytics_data()
        
        return {
            "database_statistics": db_stats,
            "timestamp": metrics.get_timestamp()
        }
        
    except Exception as e:
        logger.error(f"Error getting database statistics: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/analytics/database-stats", "method": "GET"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/knowledge-graph-stats", response_model=KnowledgeGraphStatsResponse)
async def get_knowledge_graph_statistics(
    kg: KnowledgeGraphManager = Depends(get_knowledge_graph_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Get knowledge graph statistics
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/analytics/knowledge-graph-stats", "method": "GET"})
        
        kg_stats = await kg.get_statistics()
        
        return KnowledgeGraphStatsResponse(
            total_nodes=kg_stats["total_nodes"],
            total_relationships=kg_stats["total_relationships"],
            node_types=kg_stats["node_types"],
            relationship_types=kg_stats["relationship_types"],
            graph_type=kg_stats["type"],
            last_updated=metrics.get_timestamp()
        )
        
    except Exception as e:
        logger.error(f"Error getting knowledge graph statistics: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/analytics/knowledge-graph-stats", "method": "GET"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/query", response_model=AnalyticsResponse)
async def query_analytics(
    request: AnalyticsRequest,
    db: DatabaseManager = Depends(get_database_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Query analytics data
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/analytics/query", "method": "POST"})
        
        # Get base analytics data
        db_stats = await db.get_analytics_data()
        
        # Process based on metric type
        if request.metric_type == "decision_accuracy":
            data = await _get_decision_accuracy_data(db, request)
        elif request.metric_type == "processing_time":
            data = await _get_processing_time_data(db, request)
        elif request.metric_type == "confidence_distribution":
            data = await _get_confidence_distribution_data(db, request)
        elif request.metric_type == "case_types":
            data = await _get_case_types_data(db, request)
        elif request.metric_type == "cultural_distribution":
            data = await _get_cultural_distribution_data(db, request)
        elif request.metric_type == "complexity_analysis":
            data = await _get_complexity_analysis_data(db, request)
        else:
            raise HTTPException(status_code=400, detail="Invalid metric type")
        
        # Calculate summary
        summary = _calculate_summary(data, request.metric_type)
        
        return AnalyticsResponse(
            metric_type=request.metric_type,
            data=data,
            summary=summary,
            time_range={
                "start": request.start_date.isoformat() if request.start_date else None,
                "end": request.end_date.isoformat() if request.end_date else None
            },
            filters_applied=request.filters or {},
            generated_at=metrics.get_timestamp()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error querying analytics: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/analytics/query", "method": "POST"})
        raise HTTPException(status_code=500, detail="Internal server error")

async def _get_decision_accuracy_data(db: DatabaseManager, request: AnalyticsRequest) -> dict:
    """Get decision accuracy data"""
    # This is a placeholder implementation
    # In a real system, you would query the database for accuracy metrics
    return {
        "overall_accuracy": 0.85,
        "accuracy_by_case_type": {
            "medical": 0.88,
            "autonomous_vehicle": 0.82,
            "business_ethics": 0.87,
            "general": 0.84
        },
        "accuracy_trend": [
            {"date": "2024-01-01", "accuracy": 0.80},
            {"date": "2024-02-01", "accuracy": 0.83},
            {"date": "2024-03-01", "accuracy": 0.85}
        ]
    }

async def _get_processing_time_data(db: DatabaseManager, request: AnalyticsRequest) -> dict:
    """Get processing time data"""
    return {
        "average_processing_time": 2.5,
        "median_processing_time": 2.1,
        "processing_time_distribution": {
            "0-1s": 25,
            "1-2s": 35,
            "2-5s": 30,
            "5-10s": 8,
            "10s+": 2
        },
        "processing_time_by_complexity": {
            "low": 1.2,
            "medium": 2.5,
            "high": 4.1,
            "extreme": 7.8
        }
    }

async def _get_confidence_distribution_data(db: DatabaseManager, request: AnalyticsRequest) -> dict:
    """Get confidence distribution data"""
    return {
        "average_confidence": 0.75,
        "confidence_distribution": {
            "0.0-0.2": 5,
            "0.2-0.4": 15,
            "0.4-0.6": 25,
            "0.6-0.8": 35,
            "0.8-1.0": 20
        },
        "confidence_by_case_type": {
            "medical": 0.78,
            "autonomous_vehicle": 0.72,
            "business_ethics": 0.76,
            "general": 0.73
        }
    }

async def _get_case_types_data(db: DatabaseManager, request: AnalyticsRequest) -> dict:
    """Get case types data"""
    db_stats = await db.get_analytics_data()
    
    return {
        "total_cases": db_stats["total_cases"],
        "cases_by_type": db_stats["cases_by_type"],
        "type_distribution": {
            case_type: (count / db_stats["total_cases"]) * 100 
            for case_type, count in db_stats["cases_by_type"].items()
        } if db_stats["total_cases"] > 0 else {}
    }

async def _get_cultural_distribution_data(db: DatabaseManager, request: AnalyticsRequest) -> dict:
    """Get cultural distribution data"""
    return {
        "cultural_contexts": {
            "universal": 45,
            "western": 25,
            "eastern": 15,
            "multicultural": 10,
            "other": 5
        },
        "cultural_accuracy": {
            "universal": 0.82,
            "western": 0.85,
            "eastern": 0.78,
            "multicultural": 0.73,
            "other": 0.70
        }
    }

async def _get_complexity_analysis_data(db: DatabaseManager, request: AnalyticsRequest) -> dict:
    """Get complexity analysis data"""
    db_stats = await db.get_analytics_data()
    
    return {
        "complexity_distribution": db_stats["cases_by_complexity"],
        "complexity_vs_accuracy": {
            "low": {"accuracy": 0.88, "confidence": 0.85},
            "medium": {"accuracy": 0.82, "confidence": 0.78},
            "high": {"accuracy": 0.75, "confidence": 0.70},
            "extreme": {"accuracy": 0.68, "confidence": 0.62}
        },
        "complexity_vs_processing_time": {
            "low": 1.2,
            "medium": 2.5,
            "high": 4.8,
            "extreme": 8.5
        }
    }

def _calculate_summary(data: dict, metric_type: str) -> dict:
    """Calculate summary statistics for analytics data"""
    if metric_type == "decision_accuracy":
        return {
            "key_insight": f"Overall accuracy: {data['overall_accuracy']:.1%}",
            "best_performing": max(data['accuracy_by_case_type'].items(), key=lambda x: x[1]),
            "improvement_areas": min(data['accuracy_by_case_type'].items(), key=lambda x: x[1])
        }
    elif metric_type == "processing_time":
        return {
            "key_insight": f"Average processing time: {data['average_processing_time']:.1f}s",
            "median_time": f"{data['median_processing_time']:.1f}s",
            "fastest_complexity": min(data['processing_time_by_complexity'].items(), key=lambda x: x[1])
        }
    elif metric_type == "confidence_distribution":
        return {
            "key_insight": f"Average confidence: {data['average_confidence']:.1%}",
            "high_confidence_cases": sum(
                count for range_key, count in data['confidence_distribution'].items() 
                if range_key.startswith(('0.6', '0.8'))
            ),
            "most_confident_type": max(data['confidence_by_case_type'].items(), key=lambda x: x[1])
        }
    else:
        return {"key_insight": "Summary not available for this metric type"}

@router.get("/dashboard")
async def get_dashboard_data(
    db: DatabaseManager = Depends(get_database_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector),
    kg: KnowledgeGraphManager = Depends(get_knowledge_graph_manager)
):
    """
    Get dashboard data for system overview
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/analytics/dashboard", "method": "GET"})
        
        # Get various statistics
        db_stats = await db.get_analytics_data()
        system_metrics = await metrics.get_metrics()
        kg_stats = await kg.get_statistics()
        
        # Calculate derived metrics
        uptime_hours = system_metrics["system"]["uptime_seconds"] / 3600
        decisions_per_hour = db_stats["total_decisions"] / uptime_hours if uptime_hours > 0 else 0
        
        dashboard_data = {
            "overview": {
                "total_cases": db_stats["total_cases"],
                "total_decisions": db_stats["total_decisions"],
                "average_confidence": db_stats["average_confidence"],
                "average_processing_time": db_stats["average_processing_time"],
                "system_uptime_hours": uptime_hours,
                "decisions_per_hour": decisions_per_hour
            },
            "case_distribution": {
                "by_type": db_stats["cases_by_type"],
                "by_complexity": db_stats["cases_by_complexity"]
            },
            "knowledge_graph": {
                "total_nodes": kg_stats["total_nodes"],
                "total_relationships": kg_stats["total_relationships"],
                "node_types": kg_stats["node_types"],
                "relationship_types": kg_stats["relationship_types"]
            },
            "system_health": {
                "error_rate": system_metrics["system"]["error_rate"],
                "request_rate": system_metrics["system"]["request_rate"],
                "active_connections": system_metrics["system"]["active_connections"]
            },
            "recent_activity": {
                "requests_last_hour": system_metrics["system"]["request_count"],
                "errors_last_hour": system_metrics["system"]["error_count"],
                "decisions_processed": system_metrics["business"]["decisions_processed"]
            },
            "timestamp": metrics.get_timestamp()
        }
        
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/analytics/dashboard", "method": "GET"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/time-series/{metric_name}")
async def get_time_series_data(
    metric_name: str,
    hours: int = Query(default=1, ge=1, le=24),
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Get time series data for a specific metric
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/analytics/time-series", "method": "GET"})
        
        time_window = timedelta(hours=hours)
        time_series = await metrics.get_time_series(metric_name, time_window)
        
        return {
            "metric_name": metric_name,
            "time_window_hours": hours,
            "data_points": len(time_series),
            "time_series": time_series,
            "timestamp": metrics.get_timestamp()
        }
        
    except Exception as e:
        logger.error(f"Error getting time series data: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/analytics/time-series", "method": "GET"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/performance-report")
async def get_performance_report(
    days: int = Query(default=7, ge=1, le=30),
    db: DatabaseManager = Depends(get_database_manager),
    metrics: MetricsCollector = Depends(get_metrics_collector)
):
    """
    Get comprehensive performance report
    """
    try:
        metrics.increment_counter("api_requests_total", 1, {"endpoint": "/analytics/performance-report", "method": "GET"})
        
        # Get system metrics
        system_metrics = await metrics.get_metrics()
        db_stats = await db.get_analytics_data()
        
        # Generate performance report
        report = {
            "report_period_days": days,
            "generated_at": metrics.get_timestamp(),
            "system_performance": {
                "uptime_seconds": system_metrics["system"]["uptime_seconds"],
                "total_requests": system_metrics["system"]["request_count"],
                "error_rate": system_metrics["system"]["error_rate"],
                "average_response_time": system_metrics["system"].get("average_response_time", 0)
            },
            "business_performance": {
                "total_cases_processed": db_stats["total_cases"],
                "total_decisions_made": db_stats["total_decisions"],
                "average_confidence": db_stats["average_confidence"],
                "average_processing_time": db_stats["average_processing_time"]
            },
            "efficiency_metrics": {
                "decisions_per_case": db_stats["total_decisions"] / db_stats["total_cases"] if db_stats["total_cases"] > 0 else 0,
                "requests_per_second": system_metrics["system"]["request_rate"],
                "errors_per_request": system_metrics["system"]["error_rate"]
            },
            "recommendations": _generate_performance_recommendations(system_metrics, db_stats)
        }
        
        return report
        
    except Exception as e:
        logger.error(f"Error generating performance report: {e}")
        metrics.increment_counter("api_errors_total", 1, {"endpoint": "/analytics/performance-report", "method": "GET"})
        raise HTTPException(status_code=500, detail="Internal server error")

def _generate_performance_recommendations(system_metrics: dict, db_stats: dict) -> list:
    """Generate performance recommendations based on metrics"""
    recommendations = []
    
    # Check error rate
    if system_metrics["system"]["error_rate"] > 0.05:
        recommendations.append({
            "type": "error_rate",
            "priority": "high",
            "message": "Error rate is above 5%. Consider investigating error causes and improving error handling."
        })
    
    # Check processing time
    if db_stats["average_processing_time"] > 5.0:
        recommendations.append({
            "type": "processing_time",
            "priority": "medium",
            "message": "Average processing time is above 5 seconds. Consider optimizing algorithms or scaling resources."
        })
    
    # Check confidence levels
    if db_stats["average_confidence"] < 0.7:
        recommendations.append({
            "type": "confidence",
            "priority": "medium",
            "message": "Average confidence is below 70%. Consider improving knowledge base or decision algorithms."
        })
    
    # Add positive feedback if performance is good
    if (system_metrics["system"]["error_rate"] < 0.01 and 
        db_stats["average_processing_time"] < 3.0 and 
        db_stats["average_confidence"] > 0.8):
        recommendations.append({
            "type": "performance",
            "priority": "info",
            "message": "System is performing well across all key metrics. Continue monitoring and maintain current practices."
        })
    
    return recommendations