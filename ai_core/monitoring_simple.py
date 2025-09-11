"""
Simplified Performance Monitor - Basic implementation for dialectical reasoning
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import asyncio

logger = logging.getLogger(__name__)

@dataclass
class ProcessMetrics:
    """Metrics for a single process"""
    process_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    stage_metrics: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    
    @property
    def duration(self) -> float:
        """Get process duration in seconds"""
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()

class SimplePerformanceMonitor:
    """
    Simplified performance monitor for dialectical reasoning processes
    """
    
    def __init__(self):
        self.active_processes: Dict[str, ProcessMetrics] = {}
        self.completed_processes: List[ProcessMetrics] = []
        self.global_metrics = {
            "total_processes": 0,
            "successful_processes": 0,
            "failed_processes": 0,
            "average_processing_time": 0.0,
            "total_processing_time": 0.0
        }
        
        # Keep only recent completed processes to prevent memory issues
        self.max_completed_processes = 100
        
        logger.info("Simple Performance Monitor initialized")
    
    async def initialize(self):
        """Initialize the performance monitor"""
        logger.info("Performance Monitor initialization completed")
    
    async def start_process(self, process_id: str):
        """Start monitoring a process"""
        metrics = ProcessMetrics(
            process_id=process_id,
            start_time=datetime.now()
        )
        
        self.active_processes[process_id] = metrics
        self.global_metrics["total_processes"] += 1
        
        logger.debug(f"Started monitoring process {process_id}")
    
    async def end_process(self, process_id: str):
        """End monitoring a process"""
        if process_id not in self.active_processes:
            logger.warning(f"Process {process_id} not found in active processes")
            return
        
        metrics = self.active_processes[process_id]
        metrics.end_time = datetime.now()
        
        # Move to completed processes
        self.completed_processes.append(metrics)
        del self.active_processes[process_id]
        
        # Update global metrics
        self.global_metrics["successful_processes"] += 1
        duration = metrics.duration
        self.global_metrics["total_processing_time"] += duration
        
        # Calculate average processing time
        total_completed = len(self.completed_processes)
        if total_completed > 0:
            self.global_metrics["average_processing_time"] = (
                self.global_metrics["total_processing_time"] / total_completed
            )
        
        # Maintain size limit
        if len(self.completed_processes) > self.max_completed_processes:
            # Remove oldest processes
            removed_count = len(self.completed_processes) - self.max_completed_processes
            self.completed_processes = self.completed_processes[removed_count:]
        
        logger.debug(f"Ended monitoring process {process_id} (duration: {duration:.2f}s)")
    
    async def record_stage_metrics(
        self, 
        process_id: str, 
        stage: str, 
        processing_time: float, 
        quality_score: float
    ):
        """Record metrics for a specific stage"""
        # Find the process by checking if process_id is contained in any active process key
        matching_process = None
        for active_id, metrics in self.active_processes.items():
            if process_id in active_id or active_id in process_id:
                matching_process = metrics
                break
        
        if not matching_process:
            logger.warning(f"Process {process_id} not found for stage metrics")
            return
        
        matching_process.stage_metrics[stage] = {
            "processing_time": processing_time,
            "quality_score": quality_score,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.debug(f"Recorded {stage} metrics for process {process_id}")
    
    async def record_error(self, process_id: str, error_message: str):
        """Record an error for a process"""
        if process_id in self.active_processes:
            metrics = self.active_processes[process_id]
            metrics.errors.append(f"{datetime.now().isoformat()}: {error_message}")
            
            # Move to completed as failed
            metrics.end_time = datetime.now()
            self.completed_processes.append(metrics)
            del self.active_processes[process_id]
            
            self.global_metrics["failed_processes"] += 1
        
        logger.error(f"Recorded error for process {process_id}: {error_message}")
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""
        # Calculate recent performance (last 10 processes)
        recent_processes = self.completed_processes[-10:] if self.completed_processes else []
        recent_avg_time = 0.0
        recent_success_rate = 0.0
        
        if recent_processes:
            recent_avg_time = sum(p.duration for p in recent_processes) / len(recent_processes)
            successful_recent = sum(1 for p in recent_processes if not p.errors)
            recent_success_rate = successful_recent / len(recent_processes)
        
        # Stage performance analysis
        stage_performance = {}
        for process in recent_processes:
            for stage, metrics in process.stage_metrics.items():
                if stage not in stage_performance:
                    stage_performance[stage] = {
                        "count": 0,
                        "total_time": 0.0,
                        "total_quality": 0.0
                    }
                
                stage_performance[stage]["count"] += 1
                stage_performance[stage]["total_time"] += metrics["processing_time"]
                stage_performance[stage]["total_quality"] += metrics["quality_score"]
        
        # Calculate averages for each stage
        for stage, perf in stage_performance.items():
            if perf["count"] > 0:
                perf["avg_time"] = perf["total_time"] / perf["count"]
                perf["avg_quality"] = perf["total_quality"] / perf["count"]
        
        return {
            "global_metrics": self.global_metrics.copy(),
            "active_processes": len(self.active_processes),
            "completed_processes": len(self.completed_processes),
            "recent_performance": {
                "avg_processing_time": recent_avg_time,
                "success_rate": recent_success_rate,
                "sample_size": len(recent_processes)
            },
            "stage_performance": stage_performance,
            "system_health": {
                "is_healthy": len(self.active_processes) < 50,  # Not overloaded
                "memory_usage": len(self.completed_processes),
                "error_rate": self.global_metrics["failed_processes"] / max(1, self.global_metrics["total_processes"])
            }
        }
    
    def get_active_process_info(self, process_id: str) -> Optional[Dict[str, Any]]:
        """Get information about an active process"""
        if process_id not in self.active_processes:
            return None
        
        metrics = self.active_processes[process_id]
        return {
            "process_id": process_id,
            "start_time": metrics.start_time.isoformat(),
            "duration": metrics.duration,
            "stages_completed": list(metrics.stage_metrics.keys()),
            "errors": metrics.errors
        }
    
    def get_process_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get history of recent processes"""
        recent_processes = self.completed_processes[-limit:] if self.completed_processes else []
        
        history = []
        for process in recent_processes:
            history.append({
                "process_id": process.process_id,
                "start_time": process.start_time.isoformat(),
                "end_time": process.end_time.isoformat() if process.end_time else None,
                "duration": process.duration,
                "stages": list(process.stage_metrics.keys()),
                "success": len(process.errors) == 0,
                "error_count": len(process.errors)
            })
        
        return history
    
    async def cleanup_old_data(self, max_age_hours: int = 24):
        """Clean up old performance data"""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        # Remove old completed processes
        original_count = len(self.completed_processes)
        self.completed_processes = [
            p for p in self.completed_processes 
            if p.end_time and p.end_time > cutoff_time
        ]
        
        removed_count = original_count - len(self.completed_processes)
        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} old process records")
    
    def is_healthy(self) -> bool:
        """Check if the performance monitor is healthy"""
        try:
            # Check if we're not overloaded
            if len(self.active_processes) > 100:
                return False
            
            # Check if we have reasonable error rates
            total_processes = self.global_metrics["total_processes"]
            if total_processes > 0:
                error_rate = self.global_metrics["failed_processes"] / total_processes
                if error_rate > 0.5:  # More than 50% failure rate
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking monitor health: {e}")
            return False
    
    async def shutdown(self):
        """Shutdown the performance monitor"""
        try:
            # Log final statistics
            metrics = await self.get_metrics()
            logger.info(f"Performance Monitor shutting down. Final stats: {metrics['global_metrics']}")
            
            # Clear data
            self.active_processes.clear()
            self.completed_processes.clear()
            
            logger.info("Performance Monitor shutdown completed")
            
        except Exception as e:
            logger.error(f"Error during monitor shutdown: {e}")
            raise