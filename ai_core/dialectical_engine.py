"""
Dialectical Engine - Core implementation of Hegelian dialectical reasoning
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json

from .models.ethical_case import EthicalCase
from .models.decision_result import DecisionResult, ThesisResult, AntithesisResult, SynthesisResult
from .thesis_engine import ThesisEngine
from .antithesis_engine import AntithesisEngine
from .synthesis_engine import SynthesisEngine
from .knowledge_graph import KnowledgeGraphManager
from .monitoring import PerformanceMonitor

logger = logging.getLogger(__name__)

class DialecticalStage(Enum):
    """Dialectical reasoning stages"""
    THESIS = "thesis"
    ANTITHESIS = "antithesis"
    SYNTHESIS = "synthesis"
    COMPLETED = "completed"

@dataclass
class DialecticalProcess:
    """Represents a dialectical reasoning process"""
    case_id: str
    stage: DialecticalStage
    thesis_result: Optional[ThesisResult] = None
    antithesis_result: Optional[AntithesisResult] = None
    synthesis_result: Optional[SynthesisResult] = None
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class DialecticalEngine:
    """
    Main dialectical reasoning engine implementing Hegelian dialectics
    """
    
    def __init__(self, knowledge_graph_manager: KnowledgeGraphManager, database_manager):
        self.knowledge_graph_manager = knowledge_graph_manager
        self.database_manager = database_manager
        
        # Initialize sub-engines
        self.thesis_engine = ThesisEngine(knowledge_graph_manager)
        self.antithesis_engine = AntithesisEngine(knowledge_graph_manager)
        self.synthesis_engine = SynthesisEngine(knowledge_graph_manager)
        
        # Performance monitoring
        self.performance_monitor = PerformanceMonitor()
        
        # Active processes
        self.active_processes: Dict[str, DialecticalProcess] = {}
        
        # Configuration
        self.config = {
            "max_concurrent_processes": 10,
            "timeout_seconds": 300,
            "enable_caching": True,
            "enable_learning": True
        }
        
        logger.info("Dialectical Engine initialized")
    
    async def initialize(self):
        """Initialize the dialectical engine"""
        try:
            # Initialize sub-engines
            await self.thesis_engine.initialize()
            await self.antithesis_engine.initialize()
            await self.synthesis_engine.initialize()
            
            # Initialize performance monitoring
            await self.performance_monitor.initialize()
            
            logger.info("Dialectical Engine initialization completed")
            
        except Exception as e:
            logger.error(f"Failed to initialize Dialectical Engine: {e}")
            raise
    
    async def process_ethical_case(self, case: EthicalCase) -> DecisionResult:
        """
        Process an ethical case through dialectical reasoning
        
        Args:
            case: The ethical case to process
            
        Returns:
            DecisionResult: The final decision result
        """
        process_id = f"process_{case.case_id}_{datetime.now().timestamp()}"
        
        try:
            # Create dialectical process
            process = DialecticalProcess(
                case_id=case.case_id,
                stage=DialecticalStage.THESIS,
                metadata={
                    "case_type": case.case_type,
                    "complexity": case.complexity,
                    "cultural_context": case.cultural_context
                }
            )
            
            self.active_processes[process_id] = process
            
            # Start performance monitoring
            await self.performance_monitor.start_process(process_id)
            
            # Stage 1: Thesis - Analyze current ethical norms
            logger.info(f"Starting thesis stage for case {case.case_id}")
            thesis_result = await self._execute_thesis_stage(case, process)
            process.thesis_result = thesis_result
            process.stage = DialecticalStage.ANTITHESIS
            
            # Stage 2: Antithesis - Generate opposing views
            logger.info(f"Starting antithesis stage for case {case.case_id}")
            antithesis_result = await self._execute_antithesis_stage(case, thesis_result, process)
            process.antithesis_result = antithesis_result
            process.stage = DialecticalStage.SYNTHESIS
            
            # Stage 3: Synthesis - Integrate and resolve
            logger.info(f"Starting synthesis stage for case {case.case_id}")
            synthesis_result = await self._execute_synthesis_stage(
                case, thesis_result, antithesis_result, process
            )
            process.synthesis_result = synthesis_result
            process.stage = DialecticalStage.COMPLETED
            process.end_time = datetime.now()
            
            # Create final decision result
            decision_result = DecisionResult(
                case_id=case.case_id,
                thesis_result=thesis_result,
                antithesis_result=antithesis_result,
                synthesis_result=synthesis_result,
                final_decision=synthesis_result.decision,
                confidence_score=synthesis_result.confidence,
                reasoning_path=self._construct_reasoning_path(process),
                processing_time=(process.end_time - process.start_time).total_seconds(),
                metadata=process.metadata
            )
            
            # End performance monitoring
            await self.performance_monitor.end_process(process_id)
            
            # Save to database
            await self._save_decision_result(decision_result)
            
            # Learn from this case
            if self.config["enable_learning"]:
                await self._learn_from_case(case, decision_result)
            
            # Clean up
            del self.active_processes[process_id]
            
            logger.info(f"Dialectical processing completed for case {case.case_id}")
            return decision_result
            
        except Exception as e:
            logger.error(f"Error processing ethical case {case.case_id}: {e}")
            
            # Clean up on error
            if process_id in self.active_processes:
                del self.active_processes[process_id]
            
            await self.performance_monitor.record_error(process_id, str(e))
            raise
    
    async def _execute_thesis_stage(self, case: EthicalCase, process: DialecticalProcess) -> ThesisResult:
        """Execute the thesis stage of dialectical reasoning"""
        try:
            # Measure performance
            start_time = datetime.now()
            
            # Execute thesis reasoning
            thesis_result = await self.thesis_engine.analyze_case(case)
            
            # Record metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            await self.performance_monitor.record_stage_metrics(
                process.case_id, "thesis", processing_time, thesis_result.confidence
            )
            
            return thesis_result
            
        except Exception as e:
            logger.error(f"Error in thesis stage: {e}")
            raise
    
    async def _execute_antithesis_stage(
        self, 
        case: EthicalCase, 
        thesis_result: ThesisResult, 
        process: DialecticalProcess
    ) -> AntithesisResult:
        """Execute the antithesis stage of dialectical reasoning"""
        try:
            # Measure performance
            start_time = datetime.now()
            
            # Execute antithesis reasoning
            antithesis_result = await self.antithesis_engine.generate_antithesis(thesis_result)
            
            # Record metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            await self.performance_monitor.record_stage_metrics(
                process.case_id, "antithesis", processing_time, antithesis_result.strength
            )
            
            return antithesis_result
            
        except Exception as e:
            logger.error(f"Error in antithesis stage: {e}")
            raise
    
    async def _execute_synthesis_stage(
        self, 
        case: EthicalCase, 
        thesis_result: ThesisResult, 
        antithesis_result: AntithesisResult,
        process: DialecticalProcess
    ) -> SynthesisResult:
        """Execute the synthesis stage of dialectical reasoning"""
        try:
            # Measure performance
            start_time = datetime.now()
            
            # Execute synthesis reasoning
            synthesis_result = await self.synthesis_engine.synthesize(
                case, thesis_result, antithesis_result
            )
            
            # Record metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            await self.performance_monitor.record_stage_metrics(
                process.case_id, "synthesis", processing_time, synthesis_result.confidence
            )
            
            return synthesis_result
            
        except Exception as e:
            logger.error(f"Error in synthesis stage: {e}")
            raise
    
    def _construct_reasoning_path(self, process: DialecticalProcess) -> List[Dict[str, Any]]:
        """Construct the reasoning path for explainability"""
        reasoning_path = []
        
        # Thesis stage
        if process.thesis_result:
            reasoning_path.append({
                "stage": "thesis",
                "description": "Analysis of current ethical norms and precedents",
                "key_findings": process.thesis_result.key_principles,
                "confidence": process.thesis_result.confidence,
                "reasoning": process.thesis_result.reasoning_path
            })
        
        # Antithesis stage
        if process.antithesis_result:
            reasoning_path.append({
                "stage": "antithesis",
                "description": "Generation of opposing viewpoints and challenges",
                "key_findings": process.antithesis_result.challenges,
                "strength": process.antithesis_result.strength,
                "conflicts": process.antithesis_result.conflicts
            })
        
        # Synthesis stage
        if process.synthesis_result:
            reasoning_path.append({
                "stage": "synthesis",
                "description": "Integration and resolution of dialectical tension",
                "key_findings": process.synthesis_result.integrated_principles,
                "confidence": process.synthesis_result.confidence,
                "resolution": process.synthesis_result.resolution_strategy
            })
        
        return reasoning_path
    
    async def _save_decision_result(self, decision_result: DecisionResult):
        """Save decision result to database"""
        try:
            # Convert to dictionary for database storage
            result_data = {
                "case_id": decision_result.case_id,
                "final_decision": decision_result.final_decision,
                "confidence_score": decision_result.confidence_score,
                "reasoning_path": json.dumps(decision_result.reasoning_path),
                "processing_time": decision_result.processing_time,
                "metadata": json.dumps(decision_result.metadata),
                "created_at": datetime.now()
            }
            
            await self.database_manager.save_decision_result(result_data)
            
        except Exception as e:
            logger.error(f"Error saving decision result: {e}")
            # Don't raise - saving failure shouldn't stop processing
    
    async def _learn_from_case(self, case: EthicalCase, decision_result: DecisionResult):
        """Learn from processed case to improve future decisions"""
        try:
            # Update knowledge graph with new insights
            await self.knowledge_graph_manager.add_case_insights(case, decision_result)
            
            # Update model weights based on feedback
            await self.thesis_engine.update_from_result(case, decision_result)
            await self.antithesis_engine.update_from_result(case, decision_result)
            await self.synthesis_engine.update_from_result(case, decision_result)
            
        except Exception as e:
            logger.error(f"Error learning from case: {e}")
            # Don't raise - learning failure shouldn't stop processing
    
    async def get_active_processes(self) -> Dict[str, Dict[str, Any]]:
        """Get information about active dialectical processes"""
        active_info = {}
        
        for process_id, process in self.active_processes.items():
            active_info[process_id] = {
                "case_id": process.case_id,
                "stage": process.stage.value,
                "start_time": process.start_time.isoformat(),
                "elapsed_time": (datetime.now() - process.start_time).total_seconds(),
                "metadata": process.metadata
            }
        
        return active_info
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for the dialectical engine"""
        return await self.performance_monitor.get_metrics()
    
    def is_healthy(self) -> bool:
        """Check if the dialectical engine is healthy"""
        try:
            # Check if sub-engines are healthy
            thesis_healthy = self.thesis_engine.is_healthy()
            antithesis_healthy = self.antithesis_engine.is_healthy()
            synthesis_healthy = self.synthesis_engine.is_healthy()
            
            # Check if we're not overloaded
            process_count_ok = len(self.active_processes) < self.config["max_concurrent_processes"]
            
            return thesis_healthy and antithesis_healthy and synthesis_healthy and process_count_ok
            
        except Exception as e:
            logger.error(f"Error checking engine health: {e}")
            return False
    
    async def shutdown(self):
        """Shutdown the dialectical engine"""
        try:
            logger.info("Shutting down Dialectical Engine...")
            
            # Wait for active processes to complete (with timeout)
            if self.active_processes:
                logger.info(f"Waiting for {len(self.active_processes)} active processes to complete...")
                await asyncio.sleep(5)  # Give some time for processes to complete
            
            # Shutdown sub-engines
            await self.thesis_engine.shutdown()
            await self.antithesis_engine.shutdown()
            await self.synthesis_engine.shutdown()
            
            # Shutdown performance monitoring
            await self.performance_monitor.shutdown()
            
            # Clear active processes
            self.active_processes.clear()
            
            logger.info("Dialectical Engine shutdown completed")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            raise