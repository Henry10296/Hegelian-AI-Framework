"""
Request models for the API
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime

class StakeholderRequest(BaseModel):
    """Request model for stakeholder"""
    name: str = Field(..., min_length=1, max_length=255)
    role: str = Field(..., min_length=1, max_length=255)
    interests: List[str] = Field(..., min_items=1)
    power_level: float = Field(..., ge=0.0, le=1.0)
    impact_level: float = Field(..., ge=0.0, le=1.0)
    ethical_stance: Optional[str] = Field(None, max_length=500)

class EthicalDimensionRequest(BaseModel):
    """Request model for ethical dimension"""
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1, max_length=1000)
    weight: float = Field(..., ge=0.0, le=1.0)
    values: List[str] = Field(..., min_items=1)
    conflicts: Optional[List[str]] = Field(None)

class ContextualFactorRequest(BaseModel):
    """Request model for contextual factor"""
    factor_type: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=1000)
    influence_level: float = Field(..., ge=0.0, le=1.0)
    positive_impact: bool = Field(...)
    related_principles: Optional[List[str]] = Field(None)

class CreateEthicalCaseRequest(BaseModel):
    """Request model for creating an ethical case"""
    title: str = Field(..., min_length=1, max_length=255, description="Title of the ethical case")
    description: str = Field(..., min_length=1, max_length=5000, description="Detailed description of the case")
    case_type: str = Field(..., description="Type of ethical case (medical, autonomous_vehicle, etc.)")
    complexity: str = Field(default="medium", description="Complexity level (low, medium, high, extreme)")
    cultural_context: str = Field(default="universal", description="Cultural context for evaluation")
    
    # Optional fields
    stakeholders: Optional[List[StakeholderRequest]] = Field(None, description="List of stakeholders")
    ethical_dimensions: Optional[List[EthicalDimensionRequest]] = Field(None, description="List of ethical dimensions")
    contextual_factors: Optional[List[ContextualFactorRequest]] = Field(None, description="List of contextual factors")
    
    available_options: List[str] = Field(..., min_items=1, description="Available decision options")
    constraints: Optional[List[str]] = Field(None, description="Decision constraints")
    
    # Temporal and uncertainty factors
    time_sensitivity: float = Field(default=0.5, ge=0.0, le=1.0, description="Time sensitivity (0.0 to 1.0)")
    long_term_impact: float = Field(default=0.5, ge=0.0, le=1.0, description="Long-term impact (0.0 to 1.0)")
    uncertainty_level: float = Field(default=0.5, ge=0.0, le=1.0, description="Uncertainty level (0.0 to 1.0)")
    ambiguity_level: float = Field(default=0.5, ge=0.0, le=1.0, description="Ambiguity level (0.0 to 1.0)")
    
    # Metadata
    created_by: Optional[str] = Field(None, max_length=255, description="Creator of the case")
    tags: Optional[List[str]] = Field(None, description="Tags for categorization")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
    @validator('case_type')
    def validate_case_type(cls, v):
        valid_types = ['medical', 'autonomous_vehicle', 'ai_governance', 'business_ethics', 
                      'environmental', 'social_justice', 'privacy', 'research_ethics', 'general']
        if v not in valid_types:
            raise ValueError(f'case_type must be one of: {valid_types}')
        return v
    
    @validator('complexity')
    def validate_complexity(cls, v):
        valid_levels = ['low', 'medium', 'high', 'extreme']
        if v not in valid_levels:
            raise ValueError(f'complexity must be one of: {valid_levels}')
        return v
    
    @validator('cultural_context')
    def validate_cultural_context(cls, v):
        valid_contexts = ['western', 'eastern', 'islamic', 'african', 'indigenous', 'multicultural', 'universal']
        if v not in valid_contexts:
            raise ValueError(f'cultural_context must be one of: {valid_contexts}')
        return v

class UpdateEthicalCaseRequest(BaseModel):
    """Request model for updating an ethical case"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1, max_length=5000)
    case_type: Optional[str] = Field(None)
    complexity: Optional[str] = Field(None)
    cultural_context: Optional[str] = Field(None)
    
    stakeholders: Optional[List[StakeholderRequest]] = Field(None)
    ethical_dimensions: Optional[List[EthicalDimensionRequest]] = Field(None)
    contextual_factors: Optional[List[ContextualFactorRequest]] = Field(None)
    
    available_options: Optional[List[str]] = Field(None)
    constraints: Optional[List[str]] = Field(None)
    
    time_sensitivity: Optional[float] = Field(None, ge=0.0, le=1.0)
    long_term_impact: Optional[float] = Field(None, ge=0.0, le=1.0)
    uncertainty_level: Optional[float] = Field(None, ge=0.0, le=1.0)
    ambiguity_level: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    tags: Optional[List[str]] = Field(None)
    metadata: Optional[Dict[str, Any]] = Field(None)
    
    @validator('case_type')
    def validate_case_type(cls, v):
        if v is not None:
            valid_types = ['medical', 'autonomous_vehicle', 'ai_governance', 'business_ethics', 
                          'environmental', 'social_justice', 'privacy', 'research_ethics', 'general']
            if v not in valid_types:
                raise ValueError(f'case_type must be one of: {valid_types}')
        return v
    
    @validator('complexity')
    def validate_complexity(cls, v):
        if v is not None:
            valid_levels = ['low', 'medium', 'high', 'extreme']
            if v not in valid_levels:
                raise ValueError(f'complexity must be one of: {valid_levels}')
        return v
    
    @validator('cultural_context')
    def validate_cultural_context(cls, v):
        if v is not None:
            valid_contexts = ['western', 'eastern', 'islamic', 'african', 'indigenous', 'multicultural', 'universal']
            if v not in valid_contexts:
                raise ValueError(f'cultural_context must be one of: {valid_contexts}')
        return v

class ProcessDecisionRequest(BaseModel):
    """Request model for processing a decision"""
    case_id: str = Field(..., description="ID of the case to process")
    process_options: Optional[Dict[str, Any]] = Field(None, description="Processing options")
    
    # Processing preferences
    use_cultural_adaptation: bool = Field(default=True, description="Use cultural adaptation")
    include_minority_perspectives: bool = Field(default=True, description="Include minority perspectives")
    generate_explanations: bool = Field(default=True, description="Generate explanations")
    
    # Timeout settings
    timeout_seconds: Optional[int] = Field(None, ge=10, le=300, description="Processing timeout in seconds")

class FeedbackRequest(BaseModel):
    """Request model for providing feedback on a decision"""
    decision_id: str = Field(..., description="ID of the decision to provide feedback on")
    feedback_type: str = Field(..., description="Type of feedback (positive, negative, suggestion)")
    rating: Optional[float] = Field(None, ge=0.0, le=5.0, description="Rating from 0.0 to 5.0")
    comments: Optional[str] = Field(None, max_length=2000, description="Additional comments")
    reviewer_role: Optional[str] = Field(None, max_length=100, description="Role of the reviewer")
    
    @validator('feedback_type')
    def validate_feedback_type(cls, v):
        valid_types = ['positive', 'negative', 'suggestion', 'clarification', 'correction']
        if v not in valid_types:
            raise ValueError(f'feedback_type must be one of: {valid_types}')
        return v

class AnalyticsRequest(BaseModel):
    """Request model for analytics queries"""
    metric_type: str = Field(..., description="Type of metric to query")
    start_date: Optional[datetime] = Field(None, description="Start date for the query")
    end_date: Optional[datetime] = Field(None, description="End date for the query")
    filters: Optional[Dict[str, Any]] = Field(None, description="Additional filters")
    
    @validator('metric_type')
    def validate_metric_type(cls, v):
        valid_types = ['decision_accuracy', 'processing_time', 'confidence_distribution', 
                      'case_types', 'cultural_distribution', 'complexity_analysis']
        if v not in valid_types:
            raise ValueError(f'metric_type must be one of: {valid_types}')
        return v
    
    @validator('start_date', 'end_date')
    def validate_dates(cls, v):
        if v is not None and v > datetime.now():
            raise ValueError('Date cannot be in the future')
        return v

class ExportRequest(BaseModel):
    """Request model for exporting data"""
    export_type: str = Field(..., description="Type of export (cases, decisions, analytics)")
    format: str = Field(default="json", description="Export format (json, csv, xlsx)")
    filters: Optional[Dict[str, Any]] = Field(None, description="Filters for export")
    include_metadata: bool = Field(default=True, description="Include metadata in export")
    
    @validator('export_type')
    def validate_export_type(cls, v):
        valid_types = ['cases', 'decisions', 'analytics', 'knowledge_graph']
        if v not in valid_types:
            raise ValueError(f'export_type must be one of: {valid_types}')
        return v
    
    @validator('format')
    def validate_format(cls, v):
        valid_formats = ['json', 'csv', 'xlsx', 'xml']
        if v not in valid_formats:
            raise ValueError(f'format must be one of: {valid_formats}')
        return v