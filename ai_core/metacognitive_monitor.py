"""
元认知思维监控器 - 基于最新元认知和思维科学研究

核心理论基础：
1. Flavell, J. H. (1979). Metacognition and cognitive monitoring. 
   American Psychologist, 34(10), 906-911.
   - 元认知的三个组成部分：元认知知识、元认知体验、元认知策略

2. Nelson, T. O., & Narens, L. (1990). Metamemory: A theoretical framework and new findings.
   Psychology of Learning and Motivation, 26, 125-173.
   - 元认知的监控和控制模型

3. Schraw, G., & Dennison, R. S. (1994). Assessing metacognitive awareness.
   Contemporary Educational Psychology, 19(4), 460-475.
   - 元认知意识量表(MAI)的开发

4. Veenman, M. V., Van Hout-Wolters, B. H., & Afflerbach, P. (2006). 
   Metacognition and learning: Conceptual and methodological considerations.
   Metacognition and Learning, 1(1), 3-14.
   - 元认知与学习的关系

5. Dunlosky, J., & Metcalfe, J. (2009). Metacognition. Sage Publications.
   - 元认知的综合理论框架

6. Efklides, A. (2008). Metacognition: Defining its facets and levels of functioning
   in relation to self-regulation and co-regulation. European Psychologist, 13(4), 277-287.
   - 元认知的多层次模型

7. Pintrich, P. R. (2002). The role of metacognitive knowledge in learning, teaching, and assessing.
   Theory Into Practice, 41(4), 219-225.
   - 元认知知识在学习中的作用

8. Winne, P. H., & Hadwin, A. F. (1998). Studying as self-regulated learning.
   Metacognition in Educational Theory and Practice, 277-304.
   - 自我调节学习中的元认知

9. Zimmerman, B. J. (2002). Becoming a self-regulated learner: An overview.
   Theory Into Practice, 41(2), 64-70.
   - 自我调节学习的发展

10. Brown, A. L. (1987). Metacognition, executive control, self-regulation, and other
    more mysterious mechanisms. Metacognition, Motivation, and Understanding, 65-116.
    - 元认知与执行控制的关系
"""

import logging
import time
import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import json
from collections import defaultdict, deque

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetacognitiveProcess(Enum):
    """元认知过程类型"""
    MONITORING = "monitoring"  # 监控
    CONTROL = "control"       # 控制
    EVALUATION = "evaluation" # 评估
    PLANNING = "planning"     # 规划
    REFLECTION = "reflection" # 反思

class ThinkingQuality(Enum):
    """思维质量等级"""
    EXCELLENT = "excellent"   # 优秀
    GOOD = "good"            # 良好
    ADEQUATE = "adequate"    # 充分
    POOR = "poor"           # 不足
    CRITICAL = "critical"   # 严重不足

class CognitiveLoad(Enum):
    """认知负荷水平"""
    LOW = "low"         # 低负荷
    MODERATE = "moderate" # 中等负荷
    HIGH = "high"       # 高负荷
    OVERLOAD = "overload" # 过载

@dataclass
class ThinkingState:
    """思维状态的完整表示"""
    current_focus: str
    cognitive_load: CognitiveLoad
    confidence_level: float  # 0.0-1.0
    thinking_quality: ThinkingQuality
    active_strategies: List[str]
    detected_biases: List[str]
    time_spent: float  # 秒
    progress_indicators: Dict[str, float]
    meta_awareness: float  # 元认知意识水平 0.0-1.0

@dataclass
class MetacognitiveIntervention:
    """元认知干预措施"""
    intervention_type: str
    trigger_condition: str
    action: str
    expected_outcome: str
    priority: int  # 1-10, 10为最高优先级
    cognitive_cost: float  # 执行该干预的认知成本

@dataclass
class ThinkingEpisode:
    """思维片段记录"""
    episode_id: str
    start_time: float
    end_time: float
    initial_state: ThinkingState
    final_state: ThinkingState
    interventions_applied: List[MetacognitiveIntervention]
    outcome_quality: float
    lessons_learned: List[str]

class MetacognitiveMonitor:
    """
    元认知思维监控器
    
    核心功能：
    1. 实时监控思维过程
    2. 检测认知偏误和思维陷阱
    3. 动态调节思维策略
    4. 评估思维质量
    5. 提供元认知反馈
    """
    
    def __init__(self, ai_config: Optional[Dict] = None):
        self.ai_config = ai_config or {}
        
        # 初始化监控参数
        self.monitoring_interval = 0.5  # 监控间隔（秒）
        self.quality_threshold = 0.6    # 质量阈值
        self.intervention_threshold = 0.4  # 干预阈值
        
        # 思维状态历史
        self.thinking_history: deque = deque(maxlen=100)
        self.episode_history: List[ThinkingEpisode] = []
        
        # 当前思维状态
        self.current_state: Optional[ThinkingState] = None
        self.current_episode: Optional[ThinkingEpisode] = None
        
        # 干预策略库
        self.intervention_strategies = self._initialize_intervention_strategies()
        
        # 偏误检测器
        self.bias_detectors = self._initialize_bias_detectors()
        
        # 质量评估器
        self.quality_assessor = ThinkingQualityAssessor()
        
        # 策略推荐器
        self.strategy_recommender = StrategyRecommender()
        
        logger.info("元认知监控器初始化完成")
    
    def start_monitoring(self, initial_context: Dict[str, Any]) -> str:
        """
        开始监控思维过程
        
        Args:
            initial_context: 初始思维上下文
            
        Returns:
            监控会话ID
        """
        episode_id = f"episode_{int(time.time() * 1000)}"
        
        # 创建初始思维状态
        initial_state = ThinkingState(
            current_focus=initial_context.get('focus', 'unknown'),
            cognitive_load=CognitiveLoad.LOW,
            confidence_level=0.5,
            thinking_quality=ThinkingQuality.ADEQUATE,
            active_strategies=[],
            detected_biases=[],
            time_spent=0.0,
            progress_indicators={},
            meta_awareness=0.5
        )
        
        # 创建思维片段
        self.current_episode = ThinkingEpisode(
            episode_id=episode_id,
            start_time=time.time(),
            end_time=0.0,
            initial_state=initial_state,
            final_state=initial_state,
            interventions_applied=[],
            outcome_quality=0.0,
            lessons_learned=[]
        )
        
        self.current_state = initial_state
        
        logger.info(f"开始监控思维过程，会话ID: {episode_id}")
        return episode_id
    
    def update_thinking_state(self, context_update: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新思维状态并提供元认知反馈
        
        Args:
            context_update: 思维上下文更新
            
        Returns:
            元认知反馈和建议
        """
        if not self.current_state or not self.current_episode:
            return {'error': '监控未启动，请先调用start_monitoring'}
        
        # 更新思维状态
        self._update_current_state(context_update)
        
        # 记录到历史
        self.thinking_history.append(self.current_state)
        
        # 检测需要干预的情况
        interventions_needed = self._detect_intervention_needs()
        
        # 应用干预措施
        applied_interventions = []
        for intervention in interventions_needed:
            if self._should_apply_intervention(intervention):
                self._apply_intervention(intervention)
                applied_interventions.append(intervention)
        
        # 生成元认知反馈
        feedback = self._generate_metacognitive_feedback()
        
        # 更新当前片段
        self.current_episode.interventions_applied.extend(applied_interventions)
        self.current_episode.final_state = self.current_state
        
        return feedback
    
    def end_monitoring(self) -> Dict[str, Any]:
        """
        结束监控并生成总结报告
        
        Returns:
            思维过程总结报告
        """
        if not self.current_episode:
            return {'error': '没有活跃的监控会话'}
        
        # 完成当前片段
        self.current_episode.end_time = time.time()
        self.current_episode.outcome_quality = self._assess_episode_quality()
        self.current_episode.lessons_learned = self._extract_lessons_learned()
        
        # 添加到历史
        self.episode_history.append(self.current_episode)
        
        # 生成总结报告
        summary_report = self._generate_summary_report()
        
        # 重置当前状态
        self.current_state = None
        self.current_episode = None
        
        logger.info("思维监控结束，生成总结报告")
        return summary_report
    
    def _update_current_state(self, context_update: Dict[str, Any]):
        """更新当前思维状态"""
        if not self.current_state:
            return
        
        # 更新焦点
        if 'focus' in context_update:
            self.current_state.current_focus = context_update['focus']
        
        # 更新认知负荷
        self.current_state.cognitive_load = self._assess_cognitive_load(context_update)
        
        # 更新置信度
        if 'confidence' in context_update:
            self.current_state.confidence_level = context_update['confidence']
        
        # 评估思维质量
        self.current_state.thinking_quality = self.quality_assessor.assess_quality(
            context_update, self.thinking_history
        )
        
        # 检测认知偏误
        new_biases = self._detect_cognitive_biases(context_update)
        self.current_state.detected_biases.extend(new_biases)
        
        # 更新时间
        if self.current_episode:
            self.current_state.time_spent = time.time() - self.current_episode.start_time
        
        # 更新元认知意识
        self.current_state.meta_awareness = self._assess_meta_awareness(context_update)
    
    def _assess_cognitive_load(self, context: Dict[str, Any]) -> CognitiveLoad:
        """评估认知负荷"""
        load_indicators = 0
        
        # 检查复杂性指标
        if context.get('complexity_level', 0) > 0.7:
            load_indicators += 1
        
        # 检查并行任务数量
        active_tasks = context.get('active_tasks', [])
        if len(active_tasks) > 3:
            load_indicators += 1
        
        # 检查时间压力
        if context.get('time_pressure', False):
            load_indicators += 1
        
        # 检查信息量
        info_volume = len(str(context).split())
        if info_volume > 200:
            load_indicators += 1
        
        # 根据指标数量确定负荷水平
        if load_indicators >= 3:
            return CognitiveLoad.OVERLOAD
        elif load_indicators == 2:
            return CognitiveLoad.HIGH
        elif load_indicators == 1:
            return CognitiveLoad.MODERATE
        else:
            return CognitiveLoad.LOW
    
    def _detect_cognitive_biases(self, context: Dict[str, Any]) -> List[str]:
        """检测认知偏误"""
        detected_biases = []
        
        for bias_name, detector in self.bias_detectors.items():
            if detector(context, self.thinking_history):
                detected_biases.append(bias_name)
        
        return detected_biases
    
    def _assess_meta_awareness(self, context: Dict[str, Any]) -> float:
        """评估元认知意识水平"""
        awareness_score = 0.5  # 基础分数
        
        # 检查自我反思指标
        if 'self_reflection' in context:
            awareness_score += 0.2
        
        # 检查策略意识
        if 'strategy_awareness' in context:
            awareness_score += 0.2
        
        # 检查监控行为
        if 'monitoring_behavior' in context:
            awareness_score += 0.1
        
        return min(awareness_score, 1.0)
    
    def _detect_intervention_needs(self) -> List[MetacognitiveIntervention]:
        """检测需要干预的情况"""
        needed_interventions = []
        
        if not self.current_state:
            return needed_interventions
        
        # 检查思维质量
        if self.current_state.thinking_quality in [ThinkingQuality.POOR, ThinkingQuality.CRITICAL]:
            needed_interventions.append(self.intervention_strategies['improve_thinking_quality'])
        
        # 检查认知负荷
        if self.current_state.cognitive_load == CognitiveLoad.OVERLOAD:
            needed_interventions.append(self.intervention_strategies['reduce_cognitive_load'])
        
        # 检查置信度
        if self.current_state.confidence_level < 0.3:
            needed_interventions.append(self.intervention_strategies['boost_confidence'])
        elif self.current_state.confidence_level > 0.9:
            needed_interventions.append(self.intervention_strategies['check_overconfidence'])
        
        # 检查偏误
        if self.current_state.detected_biases:
            needed_interventions.append(self.intervention_strategies['address_biases'])
        
        # 检查元认知意识
        if self.current_state.meta_awareness < 0.4:
            needed_interventions.append(self.intervention_strategies['enhance_meta_awareness'])
        
        return needed_interventions
    
    def _should_apply_intervention(self, intervention: MetacognitiveIntervention) -> bool:
        """判断是否应该应用干预措施"""
        # 检查优先级
        if intervention.priority < 5:
            return False
        
        # 检查认知成本
        if intervention.cognitive_cost > 0.8 and self.current_state.cognitive_load == CognitiveLoad.HIGH:
            return False
        
        return True
    
    def _apply_intervention(self, intervention: MetacognitiveIntervention):
        """应用干预措施"""
        logger.info(f"应用元认知干预: {intervention.intervention_type}")
        
        # 根据干预类型执行相应操作
        if intervention.intervention_type == 'strategy_adjustment':
            self._adjust_thinking_strategy()
        elif intervention.intervention_type == 'bias_correction':
            self._correct_cognitive_bias()
        elif intervention.intervention_type == 'load_reduction':
            self._reduce_cognitive_load()
        elif intervention.intervention_type == 'awareness_enhancement':
            self._enhance_meta_awareness()
    
    def _adjust_thinking_strategy(self):
        """调整思维策略"""
        if self.current_state:
            recommended_strategies = self.strategy_recommender.recommend_strategies(self.current_state)
            self.current_state.active_strategies = recommended_strategies
    
    def _correct_cognitive_bias(self):
        """纠正认知偏误"""
        if self.current_state and self.current_state.detected_biases:
            # 简化实现：清除检测到的偏误标记
            self.current_state.detected_biases = []
    
    def _reduce_cognitive_load(self):
        """减少认知负荷"""
        if self.current_state:
            # 简化实现：降低负荷等级
            if self.current_state.cognitive_load == CognitiveLoad.OVERLOAD:
                self.current_state.cognitive_load = CognitiveLoad.HIGH
            elif self.current_state.cognitive_load == CognitiveLoad.HIGH:
                self.current_state.cognitive_load = CognitiveLoad.MODERATE
    
    def _enhance_meta_awareness(self):
        """增强元认知意识"""
        if self.current_state:
            self.current_state.meta_awareness = min(self.current_state.meta_awareness + 0.1, 1.0)
    
    def _generate_metacognitive_feedback(self) -> Dict[str, Any]:
        """生成元认知反馈"""
        if not self.current_state:
            return {}
        
        return {
            'current_state': {
                'focus': self.current_state.current_focus,
                'cognitive_load': self.current_state.cognitive_load.value,
                'confidence': self.current_state.confidence_level,
                'thinking_quality': self.current_state.thinking_quality.value,
                'meta_awareness': self.current_state.meta_awareness
            },
            'detected_issues': {
                'biases': self.current_state.detected_biases,
                'quality_concerns': self._identify_quality_concerns(),
                'load_warnings': self._identify_load_warnings()
            },
            'recommendations': {
                'strategies': self.strategy_recommender.recommend_strategies(self.current_state),
                'focus_adjustments': self._suggest_focus_adjustments(),
                'break_suggestions': self._suggest_breaks()
            },
            'progress_indicators': self.current_state.progress_indicators,
            'time_spent': self.current_state.time_spent
        }
    
    def _identify_quality_concerns(self) -> List[str]:
        """识别质量问题"""
        concerns = []
        if self.current_state:
            if self.current_state.thinking_quality == ThinkingQuality.POOR:
                concerns.append("思维质量较低，建议重新审视问题")
            elif self.current_state.thinking_quality == ThinkingQuality.CRITICAL:
                concerns.append("思维质量严重不足，建议暂停并寻求帮助")
        return concerns
    
    def _identify_load_warnings(self) -> List[str]:
        """识别负荷警告"""
        warnings = []
        if self.current_state:
            if self.current_state.cognitive_load == CognitiveLoad.HIGH:
                warnings.append("认知负荷较高，建议简化任务")
            elif self.current_state.cognitive_load == CognitiveLoad.OVERLOAD:
                warnings.append("认知过载，强烈建议休息")
        return warnings
    
    def _suggest_focus_adjustments(self) -> List[str]:
        """建议焦点调整"""
        suggestions = []
        if self.current_state:
            if self.current_state.confidence_level < 0.4:
                suggestions.append("将注意力转向更熟悉的方面")
            if len(self.current_state.detected_biases) > 2:
                suggestions.append("重新审视基本假设")
        return suggestions
    
    def _suggest_breaks(self) -> List[str]:
        """建议休息"""
        suggestions = []
        if self.current_state:
            if self.current_state.time_spent > 1800:  # 30分钟
                suggestions.append("建议短暂休息5-10分钟")
            if self.current_state.cognitive_load in [CognitiveLoad.HIGH, CognitiveLoad.OVERLOAD]:
                suggestions.append("建议立即休息以恢复认知资源")
        return suggestions
    
    def _assess_episode_quality(self) -> float:
        """评估片段质量"""
        if not self.current_episode:
            return 0.0
        
        # 基于多个维度评估
        quality_factors = []
        
        # 思维质量改善
        initial_quality = self.current_episode.initial_state.thinking_quality
        final_quality = self.current_episode.final_state.thinking_quality
        quality_improvement = self._quality_to_score(final_quality) - self._quality_to_score(initial_quality)
        quality_factors.append(max(0, quality_improvement))
        
        # 干预效果
        intervention_effectiveness = len(self.current_episode.interventions_applied) * 0.1
        quality_factors.append(min(intervention_effectiveness, 0.5))
        
        # 时间效率
        time_efficiency = max(0, 1 - (self.current_episode.final_state.time_spent / 3600))  # 1小时为基准
        quality_factors.append(time_efficiency * 0.3)
        
        return sum(quality_factors) / len(quality_factors) if quality_factors else 0.0
    
    def _quality_to_score(self, quality: ThinkingQuality) -> float:
        """将质量等级转换为分数"""
        quality_scores = {
            ThinkingQuality.CRITICAL: 0.0,
            ThinkingQuality.POOR: 0.2,
            ThinkingQuality.ADEQUATE: 0.5,
            ThinkingQuality.GOOD: 0.8,
            ThinkingQuality.EXCELLENT: 1.0
        }
        return quality_scores.get(quality, 0.5)
    
    def _extract_lessons_learned(self) -> List[str]:
        """提取学习到的经验"""
        lessons = []
        
        if not self.current_episode:
            return lessons
        
        # 基于干预效果提取经验
        if self.current_episode.interventions_applied:
            lessons.append(f"应用了{len(self.current_episode.interventions_applied)}个干预措施")
        
        # 基于质量变化提取经验
        if self.current_episode.outcome_quality > 0.7:
            lessons.append("本次思维过程质量较高，策略有效")
        elif self.current_episode.outcome_quality < 0.3:
            lessons.append("本次思维过程需要改进，建议调整策略")
        
        return lessons
    
    def _generate_summary_report(self) -> Dict[str, Any]:
        """生成总结报告"""
        if not self.current_episode:
            return {}
        
        return {
            'episode_summary': {
                'episode_id': self.current_episode.episode_id,
                'duration': self.current_episode.end_time - self.current_episode.start_time,
                'outcome_quality': self.current_episode.outcome_quality,
                'interventions_count': len(self.current_episode.interventions_applied)
            },
            'state_evolution': {
                'initial_state': {
                    'quality': self.current_episode.initial_state.thinking_quality.value,
                    'confidence': self.current_episode.initial_state.confidence_level,
                    'load': self.current_episode.initial_state.cognitive_load.value
                },
                'final_state': {
                    'quality': self.current_episode.final_state.thinking_quality.value,
                    'confidence': self.current_episode.final_state.confidence_level,
                    'load': self.current_episode.final_state.cognitive_load.value
                }
            },
            'interventions_applied': [
                {
                    'type': intervention.intervention_type,
                    'action': intervention.action,
                    'priority': intervention.priority
                }
                for intervention in self.current_episode.interventions_applied
            ],
            'lessons_learned': self.current_episode.lessons_learned,
            'recommendations_for_future': self._generate_future_recommendations()
        }
    
    def _generate_future_recommendations(self) -> List[str]:
        """生成未来建议"""
        recommendations = []
        
        if not self.current_episode:
            return recommendations
        
        # 基于历史模式生成建议
        if len(self.episode_history) > 0:
            avg_quality = sum(ep.outcome_quality for ep in self.episode_history) / len(self.episode_history)
            if self.current_episode.outcome_quality > avg_quality:
                recommendations.append("继续使用当前的思维策略")
            else:
                recommendations.append("考虑调整思维方法")
        
        # 基于常见问题生成建议
        if self.current_episode.final_state.cognitive_load in [CognitiveLoad.HIGH, CognitiveLoad.OVERLOAD]:
            recommendations.append("未来需要更好地管理认知负荷")
        
        if self.current_episode.final_state.meta_awareness < 0.5:
            recommendations.append("需要提高元认知意识")
        
        return recommendations
    
    def _initialize_intervention_strategies(self) -> Dict[str, MetacognitiveIntervention]:
        """初始化干预策略"""
        return {
            'improve_thinking_quality': MetacognitiveIntervention(
                intervention_type='strategy_adjustment',
                trigger_condition='thinking_quality < adequate',
                action='调整思维策略，采用更系统的方法',
                expected_outcome='提高思维质量',
                priority=8,
                cognitive_cost=0.3
            ),
            'reduce_cognitive_load': MetacognitiveIntervention(
                intervention_type='load_reduction',
                trigger_condition='cognitive_load == overload',
                action='简化任务，分解复杂问题',
                expected_outcome='降低认知负荷',
                priority=9,
                cognitive_cost=0.2
            ),
            'boost_confidence': MetacognitiveIntervention(
                intervention_type='confidence_boost',
                trigger_condition='confidence < 0.3',
                action='回顾已有知识，寻找支持证据',
                expected_outcome='提高置信度',
                priority=6,
                cognitive_cost=0.4
            ),
            'check_overconfidence': MetacognitiveIntervention(
                intervention_type='confidence_check',
                trigger_condition='confidence > 0.9',
                action='寻找反驳证据，考虑替代观点',
                expected_outcome='校准置信度',
                priority=7,
                cognitive_cost=0.5
            ),
            'address_biases': MetacognitiveIntervention(
                intervention_type='bias_correction',
                trigger_condition='detected_biases > 0',
                action='识别并纠正认知偏误',
                expected_outcome='减少偏误影响',
                priority=8,
                cognitive_cost=0.6
            ),
            'enhance_meta_awareness': MetacognitiveIntervention(
                intervention_type='awareness_enhancement',
                trigger_condition='meta_awareness < 0.4',
                action='增强对思维过程的意识',
                expected_outcome='提高元认知水平',
                priority=5,
                cognitive_cost=0.3
            )
        }
    
    def _initialize_bias_detectors(self) -> Dict[str, Callable]:
        """初始化偏误检测器"""
        def detect_confirmation_bias(context, history):
            # 简化实现：检查是否只寻找支持性证据
            return 'only_supporting_evidence' in str(context).lower()
        
        def detect_anchoring_bias(context, history):
            # 简化实现：检查是否过度依赖初始信息
            return 'first_impression' in str(context).lower()
        
        def detect_availability_bias(context, history):
            # 简化实现：检查是否过度依赖容易回忆的信息
            return 'recent_memory' in str(context).lower()
        
        return {
            'confirmation_bias': detect_confirmation_bias,
            'anchoring_bias': detect_anchoring_bias,
            'availability_bias': detect_availability_bias
        }

class ThinkingQualityAssessor:
    """思维质量评估器"""
    
    def assess_quality(self, context: Dict[str, Any], history: deque) -> ThinkingQuality:
        """评估思维质量"""
        quality_score = 0.5  # 基础分数
        
        # 检查逻辑一致性
        if self._has_logical_consistency(context):
            quality_score += 0.2
        
        # 检查证据质量
        if self._has_good_evidence(context):
            quality_score += 0.2
        
        # 检查多角度思考
        if self._has_multiple_perspectives(context):
            quality_score += 0.1
        
        # 转换为质量等级
        if quality_score >= 0.9:
            return ThinkingQuality.EXCELLENT
        elif quality_score >= 0.7:
            return ThinkingQuality.GOOD
        elif quality_score >= 0.5:
            return ThinkingQuality.ADEQUATE
        elif quality_score >= 0.3:
            return ThinkingQuality.POOR
        else:
            return ThinkingQuality.CRITICAL
    
    def _has_logical_consistency(self, context: Dict[str, Any]) -> bool:
        """检查逻辑一致性"""
        return 'logical' in str(context).lower()
    
    def _has_good_evidence(self, context: Dict[str, Any]) -> bool:
        """检查证据质量"""
        return 'evidence' in str(context).lower()
    
    def _has_multiple_perspectives(self, context: Dict[str, Any]) -> bool:
        """检查多角度思考"""
        return 'perspective' in str(context).lower()

class StrategyRecommender:
    """策略推荐器"""
    
    def recommend_strategies(self, state: ThinkingState) -> List[str]:
        """推荐思维策略"""
        strategies = []
        
        # 基于思维质量推荐
        if state.thinking_quality in [ThinkingQuality.POOR, ThinkingQuality.CRITICAL]:
            strategies.extend(['系统分析', '逻辑检查', '证据收集'])
        
        # 基于认知负荷推荐
        if state.cognitive_load == CognitiveLoad.HIGH:
            strategies.extend(['任务分解', '优先级排序'])
        elif state.cognitive_load == CognitiveLoad.LOW:
            strategies.extend(['深度思考', '创新探索'])
        
        # 基于置信度推荐
        if state.confidence_level < 0.4:
            strategies.extend(['知识回顾', '专家咨询'])
        elif state.confidence_level > 0.8:
            strategies.extend(['反驳寻找', '假设检验'])
        
        return list(set(strategies))  # 去重

# 使用示例
if __name__ == "__main__":
    # 创建元认知监控器
    monitor = MetacognitiveMonitor()
    
    # 开始监控
    session_id = monitor.start_monitoring({'focus': '伦理决策分析'})
    
    # 模拟思维过程更新
    feedback1 = monitor.update_thinking_state({
        'focus': '分析利益相关者',
        'complexity_level': 0.6,
        'confidence': 0.7
    })
    
    feedback2 = monitor.update_thinking_state({
        'focus': '评估道德后果',
        'complexity_level': 0.8,
        'confidence': 0.5,
        'active_tasks': ['分析', '评估', '比较', '决策']
    })
    
    # 结束监控
    summary = monitor.end_monitoring()
    
    print("=== 元认知监控示例 ===")
    print(f"会话ID: {session_id}")
    print(f"反馈1: {json.dumps(feedback1, ensure_ascii=False, indent=2)}")
    print(f"反馈2: {json.dumps(feedback2, ensure_ascii=False, indent=2)}")
    print(f"总结: {json.dumps(summary, ensure_ascii=False, indent=2)}")