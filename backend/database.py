"""
Database management for the Hegelian AI Framework
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import uuid

try:
    import asyncpg
    ASYNCPG_AVAILABLE = True
except ImportError:
    ASYNCPG_AVAILABLE = False

import aiosqlite
from sqlalchemy import create_engine, MetaData, Table, Column, String, Text, Float, DateTime, JSON
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa

from .config import Settings

logger = logging.getLogger(__name__)

# SQLAlchemy Base
Base = declarative_base()

class EthicalCaseModel(Base):
    """SQLAlchemy model for ethical cases"""
    __tablename__ = "ethical_cases"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    case_type = Column(String(50))
    complexity_level = Column(String(20))
    cultural_context = Column(String(50))
    stakeholders = Column(JSON)
    ethical_dimensions = Column(JSON)
    contextual_factors = Column(JSON)
    available_options = Column(JSON)
    constraints = Column(JSON)
    time_sensitivity = Column(Float, default=0.5)
    long_term_impact = Column(Float, default=0.5)
    uncertainty_level = Column(Float, default=0.5)
    ambiguity_level = Column(Float, default=0.5)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(255))
    tags = Column(JSON)
    related_cases = Column(JSON)
    metadata_info = Column(JSON)

class DecisionResultModel(Base):
    """SQLAlchemy model for decision results"""
    __tablename__ = "decision_results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), nullable=False)
    final_decision = Column(Text)
    confidence_score = Column(Float)
    reasoning_path = Column(JSON)
    processing_time = Column(Float)
    decision_type = Column(String(50))
    thesis_result = Column(JSON)
    antithesis_result = Column(JSON)
    synthesis_result = Column(JSON)
    ethical_impact_assessment = Column(JSON)
    stakeholder_impact_analysis = Column(JSON)
    risk_assessment = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata_info = Column(JSON)

class DatabaseManager:
    """
    Database manager for the Hegelian AI Framework
    """
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = None
        self.session_factory = None
        self._initialized = False
        
        # Determine database type
        if database_url.startswith("postgresql"):
            if not ASYNCPG_AVAILABLE:
                raise ValueError("PostgreSQL requires asyncpg package. Install with: pip install asyncpg")
            self.db_type = "postgresql"
        elif database_url.startswith("sqlite"):
            self.db_type = "sqlite"
        else:
            raise ValueError(f"Unsupported database type: {database_url}")
    
    async def initialize(self):
        """Initialize the database connection and create tables"""
        try:
            if self.db_type == "postgresql":
                self.engine = create_async_engine(
                    self.database_url,
                    echo=False,
                    pool_pre_ping=True,
                    pool_recycle=3600
                )
            else:  # SQLite
                self.engine = create_async_engine(
                    self.database_url,
                    echo=False,
                    connect_args={"check_same_thread": False}
                )
            
            # Create session factory
            self.session_factory = sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            # Create tables
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            
            self._initialized = True
            logger.info(f"Database initialized successfully: {self.db_type}")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    async def get_session(self) -> AsyncSession:
        """Get a database session"""
        if not self._initialized:
            await self.initialize()
        return self.session_factory()
    
    async def save_ethical_case(self, case_data: Dict[str, Any]) -> str:
        """
        Save an ethical case to the database
        
        Args:
            case_data: Case data dictionary
            
        Returns:
            Case ID
        """
        try:
            async with self.get_session() as session:
                # Create case model
                case = EthicalCaseModel(
                    title=case_data.get("title"),
                    description=case_data.get("description"),
                    case_type=case_data.get("case_type"),
                    complexity_level=case_data.get("complexity_level"),
                    cultural_context=case_data.get("cultural_context"),
                    stakeholders=case_data.get("stakeholders", []),
                    ethical_dimensions=case_data.get("ethical_dimensions", []),
                    contextual_factors=case_data.get("contextual_factors", []),
                    available_options=case_data.get("available_options", []),
                    constraints=case_data.get("constraints", []),
                    time_sensitivity=case_data.get("time_sensitivity", 0.5),
                    long_term_impact=case_data.get("long_term_impact", 0.5),
                    uncertainty_level=case_data.get("uncertainty_level", 0.5),
                    ambiguity_level=case_data.get("ambiguity_level", 0.5),
                    created_by=case_data.get("created_by"),
                    tags=case_data.get("tags", []),
                    related_cases=case_data.get("related_cases", []),
                    metadata_info=case_data.get("metadata", {})
                )
                
                session.add(case)
                await session.commit()
                await session.refresh(case)
                
                logger.info(f"Saved ethical case: {case.id}")
                return str(case.id)
                
        except Exception as e:
            logger.error(f"Error saving ethical case: {e}")
            raise
    
    async def get_ethical_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an ethical case by ID
        
        Args:
            case_id: Case ID
            
        Returns:
            Case data or None if not found
        """
        try:
            async with self.get_session() as session:
                result = await session.get(EthicalCaseModel, uuid.UUID(case_id))
                
                if result:
                    return {
                        "id": str(result.id),
                        "title": result.title,
                        "description": result.description,
                        "case_type": result.case_type,
                        "complexity_level": result.complexity_level,
                        "cultural_context": result.cultural_context,
                        "stakeholders": result.stakeholders,
                        "ethical_dimensions": result.ethical_dimensions,
                        "contextual_factors": result.contextual_factors,
                        "available_options": result.available_options,
                        "constraints": result.constraints,
                        "time_sensitivity": result.time_sensitivity,
                        "long_term_impact": result.long_term_impact,
                        "uncertainty_level": result.uncertainty_level,
                        "ambiguity_level": result.ambiguity_level,
                        "created_at": result.created_at.isoformat(),
                        "updated_at": result.updated_at.isoformat(),
                        "created_by": result.created_by,
                        "tags": result.tags,
                        "related_cases": result.related_cases,
                        "metadata": result.metadata_info
                    }
                return None
                
        except Exception as e:
            logger.error(f"Error getting ethical case {case_id}: {e}")
            raise
    
    async def list_ethical_cases(
        self, 
        limit: int = 100, 
        offset: int = 0,
        case_type: Optional[str] = None,
        complexity_level: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List ethical cases with optional filtering
        
        Args:
            limit: Maximum number of cases to return
            offset: Number of cases to skip
            case_type: Filter by case type
            complexity_level: Filter by complexity level
            
        Returns:
            List of case data
        """
        try:
            async with self.get_session() as session:
                query = session.query(EthicalCaseModel)
                
                # Apply filters
                if case_type:
                    query = query.filter(EthicalCaseModel.case_type == case_type)
                if complexity_level:
                    query = query.filter(EthicalCaseModel.complexity_level == complexity_level)
                
                # Apply pagination
                query = query.offset(offset).limit(limit)
                
                # Execute query
                result = await query.all()
                
                # Convert to dictionaries
                cases = []
                for case in result:
                    cases.append({
                        "id": str(case.id),
                        "title": case.title,
                        "description": case.description,
                        "case_type": case.case_type,
                        "complexity_level": case.complexity_level,
                        "cultural_context": case.cultural_context,
                        "created_at": case.created_at.isoformat(),
                        "created_by": case.created_by,
                        "tags": case.tags
                    })
                
                return cases
                
        except Exception as e:
            logger.error(f"Error listing ethical cases: {e}")
            raise
    
    async def save_decision_result(self, result_data: Dict[str, Any]) -> str:
        """
        Save a decision result to the database
        
        Args:
            result_data: Decision result data
            
        Returns:
            Result ID
        """
        try:
            async with self.get_session() as session:
                # Create decision result model
                result = DecisionResultModel(
                    case_id=uuid.UUID(result_data["case_id"]),
                    final_decision=result_data.get("final_decision"),
                    confidence_score=result_data.get("confidence_score"),
                    reasoning_path=result_data.get("reasoning_path"),
                    processing_time=result_data.get("processing_time"),
                    decision_type=result_data.get("decision_type"),
                    thesis_result=result_data.get("thesis_result"),
                    antithesis_result=result_data.get("antithesis_result"),
                    synthesis_result=result_data.get("synthesis_result"),
                    ethical_impact_assessment=result_data.get("ethical_impact_assessment"),
                    stakeholder_impact_analysis=result_data.get("stakeholder_impact_analysis"),
                    risk_assessment=result_data.get("risk_assessment"),
                    metadata_info=result_data.get("metadata", {})
                )
                
                session.add(result)
                await session.commit()
                await session.refresh(result)
                
                logger.info(f"Saved decision result: {result.id}")
                return str(result.id)
                
        except Exception as e:
            logger.error(f"Error saving decision result: {e}")
            raise
    
    async def get_decision_result(self, result_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a decision result by ID
        
        Args:
            result_id: Result ID
            
        Returns:
            Decision result data or None if not found
        """
        try:
            async with self.get_session() as session:
                result = await session.get(DecisionResultModel, uuid.UUID(result_id))
                
                if result:
                    return {
                        "id": str(result.id),
                        "case_id": str(result.case_id),
                        "final_decision": result.final_decision,
                        "confidence_score": result.confidence_score,
                        "reasoning_path": result.reasoning_path,
                        "processing_time": result.processing_time,
                        "decision_type": result.decision_type,
                        "thesis_result": result.thesis_result,
                        "antithesis_result": result.antithesis_result,
                        "synthesis_result": result.synthesis_result,
                        "ethical_impact_assessment": result.ethical_impact_assessment,
                        "stakeholder_impact_analysis": result.stakeholder_impact_analysis,
                        "risk_assessment": result.risk_assessment,
                        "created_at": result.created_at.isoformat(),
                        "metadata": result.metadata_info
                    }
                return None
                
        except Exception as e:
            logger.error(f"Error getting decision result {result_id}: {e}")
            raise
    
    async def get_decisions_by_case(self, case_id: str) -> List[Dict[str, Any]]:
        """
        Get all decision results for a specific case
        
        Args:
            case_id: Case ID
            
        Returns:
            List of decision results
        """
        try:
            async with self.get_session() as session:
                query = session.query(DecisionResultModel).filter(
                    DecisionResultModel.case_id == uuid.UUID(case_id)
                )
                
                results = await query.all()
                
                decisions = []
                for result in results:
                    decisions.append({
                        "id": str(result.id),
                        "case_id": str(result.case_id),
                        "final_decision": result.final_decision,
                        "confidence_score": result.confidence_score,
                        "processing_time": result.processing_time,
                        "decision_type": result.decision_type,
                        "created_at": result.created_at.isoformat()
                    })
                
                return decisions
                
        except Exception as e:
            logger.error(f"Error getting decisions for case {case_id}: {e}")
            raise
    
    async def check_health(self) -> bool:
        """
        Check database health
        
        Returns:
            True if database is healthy
        """
        try:
            async with self.get_session() as session:
                # Simple query to check connection
                await session.execute(sa.text("SELECT 1"))
                return True
                
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    async def get_analytics_data(self) -> Dict[str, Any]:
        """
        Get analytics data from the database
        
        Returns:
            Analytics data
        """
        try:
            async with self.get_session() as session:
                # Count total cases
                total_cases = await session.scalar(
                    sa.select(sa.func.count(EthicalCaseModel.id))
                )
                
                # Count total decisions
                total_decisions = await session.scalar(
                    sa.select(sa.func.count(DecisionResultModel.id))
                )
                
                # Average confidence score
                avg_confidence = await session.scalar(
                    sa.select(sa.func.avg(DecisionResultModel.confidence_score))
                )
                
                # Average processing time
                avg_processing_time = await session.scalar(
                    sa.select(sa.func.avg(DecisionResultModel.processing_time))
                )
                
                # Cases by type
                cases_by_type = await session.execute(
                    sa.select(
                        EthicalCaseModel.case_type,
                        sa.func.count(EthicalCaseModel.id).label('count')
                    ).group_by(EthicalCaseModel.case_type)
                )
                
                # Cases by complexity
                cases_by_complexity = await session.execute(
                    sa.select(
                        EthicalCaseModel.complexity_level,
                        sa.func.count(EthicalCaseModel.id).label('count')
                    ).group_by(EthicalCaseModel.complexity_level)
                )
                
                return {
                    "total_cases": total_cases or 0,
                    "total_decisions": total_decisions or 0,
                    "average_confidence": float(avg_confidence) if avg_confidence else 0.0,
                    "average_processing_time": float(avg_processing_time) if avg_processing_time else 0.0,
                    "cases_by_type": {row.case_type: row.count for row in cases_by_type},
                    "cases_by_complexity": {row.complexity_level: row.count for row in cases_by_complexity}
                }
                
        except Exception as e:
            logger.error(f"Error getting analytics data: {e}")
            raise
    
    async def shutdown(self):
        """Shutdown the database connection"""
        try:
            if self.engine:
                await self.engine.dispose()
                logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error shutting down database: {e}")
            raise