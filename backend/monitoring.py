"""
Monitoring and metrics collection for the Hegelian AI Framework
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, deque
import json
import threading
from dataclasses import dataclass, field

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class MetricPoint:
    """Represents a single metric data point"""
    timestamp: datetime
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "labels": self.labels
        }

@dataclass
class MetricSeries:
    """Represents a time series of metric points"""
    name: str
    points: deque = field(default_factory=lambda: deque(maxlen=1000))
    
    def add_point(self, value: float, labels: Optional[Dict[str, str]] = None):
        """Add a new metric point"""
        point = MetricPoint(
            timestamp=datetime.now(),
            value=value,
            labels=labels or {}
        )
        self.points.append(point)
    
    def get_latest(self) -> Optional[MetricPoint]:
        """Get the latest metric point"""
        return self.points[-1] if self.points else None
    
    def get_average(self, time_window: timedelta = timedelta(minutes=5)) -> float:
        """Get average value within time window"""
        now = datetime.now()
        cutoff_time = now - time_window
        
        values = [
            point.value for point in self.points
            if point.timestamp >= cutoff_time
        ]
        
        return sum(values) / len(values) if values else 0.0
    
    def get_count(self, time_window: timedelta = timedelta(minutes=5)) -> int:
        """Get count of points within time window"""
        now = datetime.now()
        cutoff_time = now - time_window
        
        return len([
            point for point in self.points
            if point.timestamp >= cutoff_time
        ])

class MetricsCollector:
    """
    Metrics collector for monitoring system performance and business metrics
    """
    
    def __init__(self):
        self.metrics: Dict[str, MetricSeries] = {}
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = defaultdict(list)
        
        # System metrics
        self.start_time = datetime.now()
        self.request_count = 0
        self.error_count = 0
        self.active_connections = 0
        
        # Business metrics
        self.decisions_processed = 0
        self.average_confidence = 0.0
        self.average_processing_time = 0.0
        
        # Thread safety
        self._lock = threading.Lock()
        
        # Background tasks
        self._monitoring_task = None
        self._should_stop = False
    
    def increment_counter(self, name: str, value: int = 1, labels: Optional[Dict[str, str]] = None):
        """Increment a counter metric"""
        with self._lock:
            self.counters[name] += value
            
            # Also add to time series
            if name not in self.metrics:
                self.metrics[name] = MetricSeries(name)
            self.metrics[name].add_point(self.counters[name], labels)
    
    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Set a gauge metric"""
        with self._lock:
            self.gauges[name] = value
            
            # Also add to time series
            if name not in self.metrics:
                self.metrics[name] = MetricSeries(name)
            self.metrics[name].add_point(value, labels)
    
    def observe_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Observe a value in a histogram"""
        with self._lock:
            self.histograms[name].append(value)
            
            # Keep only last 1000 values
            if len(self.histograms[name]) > 1000:
                self.histograms[name] = self.histograms[name][-1000:]
            
            # Also add to time series
            if name not in self.metrics:
                self.metrics[name] = MetricSeries(name)
            self.metrics[name].add_point(value, labels)
    
    def record_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """Record an HTTP request"""
        with self._lock:
            self.request_count += 1
            
            labels = {
                "method": method,
                "endpoint": endpoint,
                "status_code": str(status_code)
            }
            
            self.increment_counter("http_requests_total", 1, labels)
            self.observe_histogram("http_request_duration_seconds", duration, labels)
            
            if status_code >= 400:
                self.error_count += 1
                self.increment_counter("http_requests_errors_total", 1, labels)
    
    def record_decision_processed(self, processing_time: float, confidence: float, case_type: str):
        """Record a decision processing event"""
        with self._lock:
            self.decisions_processed += 1
            
            labels = {"case_type": case_type}
            
            self.increment_counter("decisions_processed_total", 1, labels)
            self.observe_histogram("decision_processing_time_seconds", processing_time, labels)
            self.observe_histogram("decision_confidence_score", confidence, labels)
            
            # Update averages
            self.average_processing_time = (
                (self.average_processing_time * (self.decisions_processed - 1) + processing_time)
                / self.decisions_processed
            )
            
            self.average_confidence = (
                (self.average_confidence * (self.decisions_processed - 1) + confidence)
                / self.decisions_processed
            )
    
    def record_ai_inference(self, model_name: str, inference_time: float, success: bool):
        """Record an AI model inference"""
        labels = {
            "model_name": model_name,
            "success": str(success).lower()
        }
        
        self.increment_counter("ai_inferences_total", 1, labels)
        self.observe_histogram("ai_inference_time_seconds", inference_time, labels)
        
        if not success:
            self.increment_counter("ai_inference_errors_total", 1, labels)
    
    def record_database_query(self, query_type: str, duration: float, success: bool):
        """Record a database query"""
        labels = {
            "query_type": query_type,
            "success": str(success).lower()
        }
        
        self.increment_counter("database_queries_total", 1, labels)
        self.observe_histogram("database_query_duration_seconds", duration, labels)
        
        if not success:
            self.increment_counter("database_query_errors_total", 1, labels)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all current metrics"""
        with self._lock:
            uptime = (datetime.now() - self.start_time).total_seconds()
            
            # Calculate rates
            request_rate = self.request_count / uptime if uptime > 0 else 0
            error_rate = self.error_count / self.request_count if self.request_count > 0 else 0
            
            # Get histogram statistics
            histogram_stats = {}
            for name, values in self.histograms.items():
                if values:
                    histogram_stats[name] = {
                        "count": len(values),
                        "sum": sum(values),
                        "min": min(values),
                        "max": max(values),
                        "avg": sum(values) / len(values),
                        "p50": self._percentile(values, 50),
                        "p90": self._percentile(values, 90),
                        "p95": self._percentile(values, 95),
                        "p99": self._percentile(values, 99)
                    }
            
            return {
                "system": {
                    "uptime_seconds": uptime,
                    "start_time": self.start_time.isoformat(),
                    "request_count": self.request_count,
                    "error_count": self.error_count,
                    "request_rate": request_rate,
                    "error_rate": error_rate,
                    "active_connections": self.active_connections
                },
                "business": {
                    "decisions_processed": self.decisions_processed,
                    "average_confidence": self.average_confidence,
                    "average_processing_time": self.average_processing_time
                },
                "counters": dict(self.counters),
                "gauges": dict(self.gauges),
                "histograms": histogram_stats,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_health_metrics(self) -> Dict[str, Any]:
        """Get health-related metrics"""
        with self._lock:
            # Calculate recent error rates
            recent_errors = 0
            recent_requests = 0
            
            # Check metrics from last 5 minutes
            if "http_requests_total" in self.metrics:
                recent_requests = self.metrics["http_requests_total"].get_count(timedelta(minutes=5))
            
            if "http_requests_errors_total" in self.metrics:
                recent_errors = self.metrics["http_requests_errors_total"].get_count(timedelta(minutes=5))
            
            recent_error_rate = recent_errors / recent_requests if recent_requests > 0 else 0
            
            # Check average response times
            avg_response_time = 0.0
            if "http_request_duration_seconds" in self.metrics:
                avg_response_time = self.metrics["http_request_duration_seconds"].get_average(timedelta(minutes=5))
            
            # Determine health status
            health_status = "healthy"
            if recent_error_rate > 0.1:  # More than 10% errors
                health_status = "unhealthy"
            elif recent_error_rate > 0.05:  # More than 5% errors
                health_status = "warning"
            elif avg_response_time > 2.0:  # More than 2 seconds average
                health_status = "warning"
            
            return {
                "status": health_status,
                "recent_error_rate": recent_error_rate,
                "recent_requests": recent_requests,
                "recent_errors": recent_errors,
                "average_response_time": avg_response_time,
                "active_connections": self.active_connections,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_time_series(self, metric_name: str, time_window: timedelta = timedelta(hours=1)) -> List[Dict[str, Any]]:
        """Get time series data for a specific metric"""
        if metric_name not in self.metrics:
            return []
        
        now = datetime.now()
        cutoff_time = now - time_window
        
        series = self.metrics[metric_name]
        filtered_points = [
            point for point in series.points
            if point.timestamp >= cutoff_time
        ]
        
        return [point.to_dict() for point in filtered_points]
    
    def get_timestamp(self) -> str:
        """Get current timestamp as ISO string"""
        return datetime.now().isoformat()
    
    def _percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile of values"""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        index = (percentile / 100) * (len(sorted_values) - 1)
        
        if index.is_integer():
            return sorted_values[int(index)]
        else:
            lower_index = int(index)
            upper_index = lower_index + 1
            weight = index - lower_index
            
            return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight
    
    async def start_monitoring(self):
        """Start background monitoring tasks"""
        self._should_stop = False
        self._monitoring_task = asyncio.create_task(self._monitor_system())
        logger.info("Monitoring started")
    
    async def _monitor_system(self):
        """Background task to monitor system metrics"""
        if not PSUTIL_AVAILABLE:
            logger.warning("psutil not available, system monitoring disabled")
            return
        
        while not self._should_stop:
            try:
                # System metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory_percent = psutil.virtual_memory().percent
                disk_percent = psutil.disk_usage('/').percent
                
                self.set_gauge("system_cpu_percent", cpu_percent)
                self.set_gauge("system_memory_percent", memory_percent)
                self.set_gauge("system_disk_percent", disk_percent)
                
                # Process metrics
                process = psutil.Process()
                self.set_gauge("process_memory_mb", process.memory_info().rss / 1024 / 1024)
                self.set_gauge("process_cpu_percent", process.cpu_percent())
                
                await asyncio.sleep(10)  # Monitor every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in system monitoring: {e}")
                await asyncio.sleep(30)  # Wait longer on error
    
    async def shutdown(self):
        """Shutdown the metrics collector"""
        self._should_stop = True
        
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Metrics collector shut down")

# Global metrics collector instance
metrics_collector = MetricsCollector()

def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector instance"""
    return metrics_collector

# Decorators for automatic metrics collection
def monitor_performance(metric_name: str = None):
    """Decorator to monitor function performance"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            name = metric_name or f"{func.__module__}.{func.__name__}"
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                metrics_collector.observe_histogram(
                    f"{name}_duration_seconds", 
                    duration,
                    {"success": "true"}
                )
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                
                metrics_collector.observe_histogram(
                    f"{name}_duration_seconds", 
                    duration,
                    {"success": "false"}
                )
                
                metrics_collector.increment_counter(
                    f"{name}_errors_total",
                    1,
                    {"exception": type(e).__name__}
                )
                
                raise
        
        return wrapper
    return decorator

def monitor_async_performance(metric_name: str = None):
    """Decorator to monitor async function performance"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            name = metric_name or f"{func.__module__}.{func.__name__}"
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                
                metrics_collector.observe_histogram(
                    f"{name}_duration_seconds", 
                    duration,
                    {"success": "true"}
                )
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                
                metrics_collector.observe_histogram(
                    f"{name}_duration_seconds", 
                    duration,
                    {"success": "false"}
                )
                
                metrics_collector.increment_counter(
                    f"{name}_errors_total",
                    1,
                    {"exception": type(e).__name__}
                )
                
                raise
        
        return wrapper
    return decorator