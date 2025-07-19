"""
Response models for the API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class StakeholderResponse(BaseModel):
    """Response model for stakeholder"""
    name: str
    role: str
    interests: List[str]
    power_level: float
    impact_level: float
    ethical_stance: Optional[str] = None

class EthicalDimensionResponse(BaseModel):
    """Response model for ethical dimension"""
    name: str
    description: str
    weight: float
    values: List[str]
    conflicts: List[str] = []

class ContextualFactorResponse(BaseModel):
    """Response model for contextual factor"""
    factor_type: str
    description: str
    influence_level: float
    positive_impact: bool
    related_principles: List[str] = []

class EthicalCaseResponse(BaseModel):
    """Response model for ethical case"""
    id: str
    title: str
    description: str
    case_type: str
    complexity: str
    cultural_context: str
    
    stakeholders: List[StakeholderResponse] = []
    ethical_dimensions: List[EthicalDimensionResponse] = []
    contextual_factors: List[ContextualFactorResponse] = []
    
    available_options: List[str]
    constraints: List[str] = []
    
    time_sensitivity: float
    long_term_impact: float
    uncertainty_level: float
    ambiguity_level: float
    
    created_at: str
    updated_at: Optional[str] = None
    created_by: Optional[str] = None
    tags: List[str] = []
    related_cases: List[str] = []
    metadata: Dict[str, Any] = {}

class EthicalCaseListResponse(BaseModel):
    """Response model for list of ethical cases"""
    cases: List[EthicalCaseResponse]
    total: int
    limit: int
    offset: int
    has_more: bool = Field(default=False)
    
    def __init__(self, **data):
        super().__init__(**data)
        self.has_more = (self.offset + self.limit) < self.total

class EthicalPrincipleResponse(BaseModel):
    """Response model for ethical principle"""
    name: str
    description: str
    weight: float
    relevance_score: float
    cultural_adaptation: Optional[str] = None

class ReasoningStepResponse(BaseModel):
    """Response model for reasoning step"""
    step_number: int
    description: str
    inputs: List[str]
    outputs: List[str]
    confidence: float
    reasoning_type: str

class ThesisResultResponse(BaseModel):
    """Response model for thesis result"""
    case_id: str
    key_principles: List[EthicalPrincipleResponse]
    applicable_norms: List[str]
    precedent_cases: List[str]
    confidence: float
    reasoning_path: List[ReasoningStepResponse]
    cultural_considerations: List[str] = []
    temporal_factors: List[str] = []
    stakeholder_analysis: Dict[str, Any] = {}

class EthicalChallengeResponse(BaseModel):
    """Response model for ethical challenge"""
    challenge_type: str
    description: str
    strength: float
    counter_arguments: List[str]
    affected_stakeholders: List[str]
    cultural_source: Optional[str] = None

class ConflictScenarioResponse(BaseModel):
    """Response model for conflict scenario"""
    scenario_id: str
    description: str
    conflicting_values: List[str]
    potential_outcomes: List[str]
    likelihood: float
    impact_severity: float

class AntithesisResultResponse(BaseModel):
    """Response model for antithesis result"""
    case_id: str
    challenges: List[EthicalChallengeResponse]
    alternative_perspectives: List[str]
    conflicts: List[ConflictScenarioResponse]
    devil_advocate_arguments: List[str]
    strength: float
    cultural_variations: Dict[str, List[str]] = {}
    minority_positions: List[str] = []

class ResolutionStrategyResponse(BaseModel):
    """Response model for resolution strategy"""
    strategy_type: str
    description: str
    steps: List[str]
    expected_outcomes: List[str]
    success_probability: float

class IntegratedPrincipleResponse(BaseModel):
    """Response model for integrated principle"""
    name: str
    description: str
    source_principles: List[str]
    integration_method: str
    weight: float
    consensus_level: float

class SynthesisResultResponse(BaseModel):
    """Response model for synthesis result"""
    case_id: str
    decision: str
    integrated_principles: List[IntegratedPrincipleResponse]
    resolution_strategy: ResolutionStrategyResponse
    confidence: float
    consensus_score: float
    trade_offs: List[str]
    implementation_guidelines: List[str]
    monitoring_requirements: List[str] = []
    fallback_options: List[str] = []

class DecisionResultResponse(BaseModel):
    """Response model for decision result"""
    id: str
    case_id: str
    thesis_result: ThesisResultResponse
    antithesis_result: AntithesisResultResponse
    synthesis_result: SynthesisResultResponse
    final_decision: str
    confidence_score: float
    reasoning_path: List[Dict[str, Any]]
    processing_time: float
    decision_type: str
    timestamp: str
    
    ethical_impact_assessment: Dict[str, Any] = {}
    stakeholder_impact_analysis: Dict[str, Any] = {}
    risk_assessment: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}

class DecisionSummaryResponse(BaseModel):
    """Response model for decision summary"""
    id: str
    case_id: str
    final_decision: str
    decision_type: str
    confidence_score: float
    confidence_level: str
    processing_time: float
    key_principles: List[str]
    main_challenges: List[str]
    resolution_strategy: str
    consensus_score: float
    timestamp: str

class DecisionListResponse(BaseModel):
    """Response model for list of decisions"""
    decisions: List[DecisionSummaryResponse]
    total: int
    limit: int
    offset: int
    has_more: bool = Field(default=False)
    
    def __init__(self, **data):
        super().__init__(**data)
        self.has_more = (self.offset + self.limit) < self.total

class ProcessingStatusResponse(BaseModel):
    """Response model for processing status"""
    process_id: str
    case_id: str
    status: str  # pending, processing, completed, failed
    stage: str   # thesis, antithesis, synthesis, completed
    progress: float  # 0.0 to 1.0
    estimated_remaining_time: Optional[int] = None
    error_message: Optional[str] = None
    started_at: str
    updated_at: str

class HealthCheckResponse(BaseModel):
    """Response model for health check"""
    status: str
    components: Dict[str, str]
    timestamp: str
    uptime: Optional[float] = None
    version: str = "1.0.0"

class SystemInfoResponse(BaseModel):
    """Response model for system information"""
    name: str
    version: str
    description: str
    components: Dict[str, str]
    endpoints: Dict[str, str]
    statistics: Optional[Dict[str, Any]] = None

class MetricsResponse(BaseModel):
    """Response model for metrics"""
    system: Dict[str, Any]
    business: Dict[str, Any]
    counters: Dict[str, int]
    gauges: Dict[str, float]
    histograms: Dict[str, Dict[str, float]]
    timestamp: str

class AnalyticsResponse(BaseModel):
    """Response model for analytics"""
    metric_type: str
    data: Dict[str, Any]
    summary: Dict[str, Any]
    time_range: Dict[str, str]
    filters_applied: Dict[str, Any] = {}
    generated_at: str

class ExportResponse(BaseModel):
    """Response model for export"""
    export_id: str
    export_type: str
    format: str
    status: str  # pending, processing, completed, failed
    download_url: Optional[str] = None
    file_size: Optional[int] = None
    record_count: Optional[int] = None
    created_at: str
    expires_at: Optional[str] = None
    error_message: Optional[str] = None

class FeedbackResponse(BaseModel):
    """Response model for feedback"""
    feedback_id: str
    decision_id: str
    feedback_type: str
    rating: Optional[float] = None
    comments: Optional[str] = None
    reviewer_role: Optional[str] = None
    status: str  # pending, reviewed, incorporated
    created_at: str
    reviewed_at: Optional[str] = None

class KnowledgeGraphStatsResponse(BaseModel):
    """Response model for knowledge graph statistics"""
    total_nodes: int
    total_relationships: int
    node_types: List[str]
    relationship_types: List[str]
    graph_type: str  # neo4j, mock
    last_updated: str

class ErrorResponse(BaseModel):
    """Response model for errors"""
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: str
    request_id: Optional[str] = None

class ValidationErrorResponse(BaseModel):
    """Response model for validation errors"""
    error_code: str = "validation_error"
    message: str = "Request validation failed"
    errors: List[Dict[str, Any]]
    timestamp: str