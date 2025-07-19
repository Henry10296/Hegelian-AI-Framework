"""
Performance Monitoring Module for AI Core Components
"""

import asyncio
import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import json
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

@dataclass
class MetricPoint:
    """Represents a single metric measurement"""
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
class PerformanceMetrics:
    """Container for performance metrics"""
    component_name: str
    processing_time: float
    memory_usage: float
    cpu_usage: float
    success_rate: float
    error_count: int
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "component_name": self.component_name,
            "processing_time": self.processing_time,
            "memory_usage": self.memory_usage,
            "cpu_usage": self.cpu_usage,
            "success_rate": self.success_rate,
            "error_count": self.error_count,
            "timestamp": self.timestamp.isoformat()
        }

class PerformanceMonitor:
    """
    Performance monitoring system for AI core components
    """
    
    def __init__(self, max_history_size: int = 1000):
        self.max_history_size = max_history_size
        self.metrics_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_history_size))
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = defaultdict(float)
        self.histograms: Dict[str, List[float]] = defaultdict(list)
        self.timers: Dict[str, float] = {}
        self.start_time = time.time()
        self.is_running = False
        
        logger.info("Performance Monitor initialized")
    
    async def initialize(self):
        """Initialize the performance monitor"""
        try:
            self.is_running = True
            self.start_time = time.time()
            logger.info("Performance Monitor started")
        except Exception as e:
            logger.error(f"Failed to initialize Performance Monitor: {e}")
            raise
    
    def start_timer(self, operation_name: str) -> str:
        """Start a timer for an operation"""
        timer_id = f"{operation_name}_{time.time()}"
        self.timers[timer_id] = time.time()
        return timer_id
    
    def end_timer(self, timer_id: str) -> float:
        """End a timer and return elapsed time"""
        if timer_id not in self.timers:
            logger.warning(f"Timer {timer_id} not found")
            return 0.0
        
        elapsed = time.time() - self.timers[timer_id]
        del self.timers[timer_id]
        return elapsed
    
    def record_metric(self, metric_name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Record a metric value"""
        labels = labels or {}
        metric_point = MetricPoint(
            timestamp=datetime.now(),
            value=value,
            labels=labels
        )
        self.metrics_history[metric_name].append(metric_point)
    
    def increment_counter(self, counter_name: str, value: int = 1, labels: Optional[Dict[str, str]] = None):
        """Increment a counter"""
        full_name = self._get_metric_name(counter_name, labels)
        self.counters[full_name] += value
        self.record_metric(counter_name, self.counters[full_name], labels)
    
    def set_gauge(self, gauge_name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Set a gauge value"""
        full_name = self._get_metric_name(gauge_name, labels)
        self.gauges[full_name] = value
        self.record_metric(gauge_name, value, labels)
    
    def record_histogram(self, histogram_name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Record a value in a histogram"""
        full_name = self._get_metric_name(histogram_name, labels)
        self.histograms[full_name].append(value)
        self.record_metric(histogram_name, value, labels)
        
        # Keep only recent values
        if len(self.histograms[full_name]) > self.max_history_size:
            self.histograms[full_name] = self.histograms[full_name][-self.max_history_size:]
    
    def _get_metric_name(self, base_name: str, labels: Optional[Dict[str, str]]) -> str:
        """Generate metric name with labels"""
        if not labels:
            return base_name
        
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{base_name}[{label_str}]"
    
    async def record_component_performance(self, component_name: str, operation_time: float):
        """Record performance metrics for a component"""
        try:
            # Record processing time
            self.record_histogram(f"{component_name}_processing_time", operation_time)
            
            # Record operation count
            self.increment_counter(f"{component_name}_operations_total")
            
            # Calculate and record success rate (placeholder)
            success_rate = 0.95  # This would be calculated based on actual success/failure tracking
            self.set_gauge(f"{component_name}_success_rate", success_rate)
            
            logger.debug(f"Recorded performance metrics for {component_name}: {operation_time:.3f}s")
            
        except Exception as e:
            logger.error(f"Error recording component performance: {e}")
    
    async def record_decision_metrics(self, processing_time: float, confidence: float, case_type: str):
        """Record metrics specific to decision processing"""
        try:
            labels = {"case_type": case_type}
            
            # Record processing time
            self.record_histogram("decision_processing_time", processing_time, labels)
            
            # Record confidence score
            self.record_histogram("decision_confidence", confidence, labels)
            
            # Increment decision counter
            self.increment_counter("decisions_processed_total", 1, labels)
            
            # Calculate confidence level distribution
            confidence_level = self._get_confidence_level(confidence)
            self.increment_counter("confidence_level_distribution", 1, {
                "level": confidence_level,
                "case_type": case_type
            })
            
        except Exception as e:
            logger.error(f"Error recording decision metrics: {e}")
    
    def _get_confidence_level(self, confidence: float) -> str:
        """Convert confidence score to level"""
        if confidence >= 0.9:
            return "very_high"
        elif confidence >= 0.7:
            return "high"
        elif confidence >= 0.5:
            return "medium"
        elif confidence >= 0.3:
            return "low"
        else:
            return "very_low"
    
    async def get_metrics_summary(self) -> Dict[str, Any]:
        """Get a summary of all metrics"""
        try:
            uptime = time.time() - self.start_time
            
            summary = {
                "uptime_seconds": uptime,
                "total_metrics": len(self.metrics_history),
                "counters": dict(self.counters),
                "gauges": dict(self.gauges),
                "histograms": self._summarize_histograms(),
                "recent_activity": self._get_recent_activity(),
                "timestamp": datetime.now().isoformat()
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting metrics summary: {e}")
            return {}
    
    def _summarize_histograms(self) -> Dict[str, Dict[str, float]]:
        """Summarize histogram data"""
        summaries = {}
        
        for name, values in self.histograms.items():
            if not values:
                continue
            
            summaries[name] = {
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "mean": sum(values) / len(values),
                "p50": self._percentile(values, 50),
                "p95": self._percentile(values, 95),
                "p99": self._percentile(values, 99)
            }
        
        return summaries
    
    def _percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile value"""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        k = (len(sorted_values) - 1) * percentile / 100
        f = int(k)
        c = k - f
        
        if f == len(sorted_values) - 1:
            return sorted_values[f]
        
        return sorted_values[f] * (1 - c) + sorted_values[f + 1] * c
    
    def _get_recent_activity(self, minutes: int = 5) -> Dict[str, Any]:
        """Get recent activity summary"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_activity = {
            "time_window_minutes": minutes,
            "metrics_recorded": 0,
            "operations_count": 0,
            "error_count": 0
        }
        
        for metric_name, history in self.metrics_history.items():
            recent_count = sum(1 for point in history if point.timestamp > cutoff_time)
            recent_activity["metrics_recorded"] += recent_count
            
            if "operations_total" in metric_name:
                recent_activity["operations_count"] += recent_count
            elif "error" in metric_name:
                recent_activity["error_count"] += recent_count
        
        return recent_activity
    
    async def get_time_series(self, metric_name: str, time_window: timedelta) -> List[Dict[str, Any]]:
        """Get time series data for a metric"""
        try:
            cutoff_time = datetime.now() - time_window
            
            if metric_name not in self.metrics_history:
                return []
            
            time_series = []
            for point in self.metrics_history[metric_name]:
                if point.timestamp > cutoff_time:
                    time_series.append(point.to_dict())
            
            return sorted(time_series, key=lambda x: x["timestamp"])
            
        except Exception as e:
            logger.error(f"Error getting time series for {metric_name}: {e}")
            return []
    
    async def get_component_health(self, component_name: str) -> Dict[str, Any]:
        """Get health status for a specific component"""
        try:
            health = {
                "component": component_name,
                "status": "healthy",
                "metrics": {},
                "alerts": [],
                "timestamp": datetime.now().isoformat()
            }
            
            # Check processing time
            processing_time_metric = f"{component_name}_processing_time"
            if processing_time_metric in self.histograms:
                recent_times = self.histograms[processing_time_metric][-10:]  # Last 10 operations
                if recent_times:
                    avg_time = sum(recent_times) / len(recent_times)
                    health["metrics"]["avg_processing_time"] = avg_time
                    
                    # Alert if processing time is too high
                    if avg_time > 10.0:  # 10 seconds threshold
                        health["alerts"].append(f"High processing time: {avg_time:.2f}s")
                        health["status"] = "warning"
            
            # Check success rate
            success_rate_metric = f"{component_name}_success_rate"
            if success_rate_metric in self.gauges:
                success_rate = self.gauges[success_rate_metric]
                health["metrics"]["success_rate"] = success_rate
                
                if success_rate < 0.9:  # 90% threshold
                    health["alerts"].append(f"Low success rate: {success_rate:.1%}")
                    health["status"] = "warning"
                
                if success_rate < 0.5:  # 50% threshold
                    health["status"] = "unhealthy"
            
            # Check error count
            error_count = 0
            for counter_name in self.counters:
                if component_name in counter_name and "error" in counter_name:
                    error_count += self.counters[counter_name]
            
            health["metrics"]["error_count"] = error_count
            if error_count > 10:  # Error threshold
                health["alerts"].append(f"High error count: {error_count}")
                health["status"] = "warning"
            
            return health
            
        except Exception as e:
            logger.error(f"Error getting component health for {component_name}: {e}")
            return {"component": component_name, "status": "unknown", "error": str(e)}
    
    async def export_metrics(self, format_type: str = "json") -> str:
        """Export metrics in specified format"""
        try:
            metrics_data = await self.get_metrics_summary()
            
            if format_type.lower() == "json":
                return json.dumps(metrics_data, indent=2)
            elif format_type.lower() == "prometheus":
                return self._export_prometheus_format()
            else:
                raise ValueError(f"Unsupported export format: {format_type}")
                
        except Exception as e:
            logger.error(f"Error exporting metrics: {e}")
            return ""
    
    def _export_prometheus_format(self) -> str:
        """Export metrics in Prometheus format"""
        lines = []
        
        # Export counters
        for name, value in self.counters.items():
            clean_name = name.replace('[', '{').replace(']', '}').replace('=', '="').replace(',', '","') + '"'
            lines.append(f'# TYPE {name.split("[")[0]} counter')
            lines.append(f'{clean_name} {value}')
        
        # Export gauges
        for name, value in self.gauges.items():
            clean_name = name.replace('[', '{').replace(']', '}').replace('=', '="').replace(',', '","') + '"'
            lines.append(f'# TYPE {name.split("[")[0]} gauge')
            lines.append(f'{clean_name} {value}')
        
        return '\n'.join(lines)
    
    async def cleanup_old_metrics(self, max_age: timedelta = timedelta(hours=24)):
        """Clean up old metrics to prevent memory leaks"""
        try:
            cutoff_time = datetime.now() - max_age
            cleaned_count = 0
            
            for metric_name in list(self.metrics_history.keys()):
                history = self.metrics_history[metric_name]
                original_length = len(history)
                
                # Remove old entries
                while history and history[0].timestamp < cutoff_time:
                    history.popleft()
                
                cleaned_count += original_length - len(history)
                
                # Remove empty histories
                if not history:
                    del self.metrics_history[metric_name]
            
            if cleaned_count > 0:
                logger.info(f"Cleaned up {cleaned_count} old metric entries")
                
        except Exception as e:
            logger.error(f"Error cleaning up old metrics: {e}")
    
    def get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()
    
    def is_healthy(self) -> bool:
        """Check if the monitor itself is healthy"""
        try:
            return (
                self.is_running and
                len(self.metrics_history) < 10000 and  # Not too many metrics
                time.time() - self.start_time > 0  # Running for some time
            )
        except Exception:
            return False
    
    async def shutdown(self):
        """Shutdown the performance monitor"""
        try:
            self.is_running = False
            
            # Clean up resources
            self.metrics_history.clear()
            self.counters.clear()
            self.gauges.clear()
            self.histograms.clear()
            self.timers.clear()
            
            logger.info("Performance Monitor shut down")
            
        except Exception as e:
            logger.error(f"Error shutting down Performance Monitor: {e}")
            raise