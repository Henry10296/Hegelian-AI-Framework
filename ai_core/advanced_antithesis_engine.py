"""
前沿思辨反题引擎 - 基于最新认知科学和论证理论研究

核心理论基础：
1. Mercier, H., & Sperber, D. (2017). The Enigma of Reason. Harvard University Press.
   - 论证推理的进化功能：人类推理主要用于论证而非独立思考
   - 确认偏误的适应性价值：在社会论证中维护立场的重要性

2. Walton, D., Reed, C., & Macagno, F. (2008). Argumentation Schemes. Cambridge University Press.
   - 25种基础论证模式的形式化表示
   - 批判性问题(Critical Questions)作为反驳生成的系统方法

3. Rahwan, I., & Simari, G. R. (2009). Argumentation in Artificial Intelligence. Springer.
   - 可废止推理(Defeasible Reasoning)在AI中的应用
   - 论证框架的计算实现

4. Bench-Capon, T., & Dunne, P. E. (2007). Argumentation in artificial intelligence. 
   Artificial Intelligence, 171(10-15), 619-641.
   - 抽象论证框架(Abstract Argumentation Frameworks)
   - 语义学方法：grounded, preferred, stable extensions

5. Dung, P. M. (1995). On the acceptability of arguments and its fundamental role in 
   nonmonotonic reasoning, logic programming and n-person games. 
   Artificial Intelligence, 77(2), 321-357.
   - Dung框架：论证的攻击关系和可接受性语义

6. Prakken, H. (2010). An abstract framework for argumentation with structured arguments. 
   Argument & Computation, 1(2), 93-124.
   - 结构化论证：前提、推理规则、结论的形式化

7. Besnard, P., & Hunter, A. (2008). Elements of Argumentation. MIT Press.
   - 论证的逻辑基础和不一致性处理
   - 论证强度的量化方法

8. Toulmin, S. E. (2003). The Uses of Argument. Cambridge University Press.
   - Toulmin模型：claim, data, warrant, backing, qualifier, rebuttal
   - 实用论证结构的六要素分析

9. van Eemeren, F. H., & Grootendorst, R. (2004). A Systematic Theory of Argumentation. 
   Cambridge University Press.
   - 语用辩证法理论：论证作为解决意见分歧的活动
   - 十条合理讨论规则

10. Kahneman, D. (2011). Thinking, Fast and Slow. Farrar, Straus and Giroux.
    - 系统1和系统2思维：直觉vs分析思维的双重过程理论
    - 认知偏误对论证质量的影响

11. Stanovich, K. E. (2016). The Comprehensive Assessment of Rational Thinking. 
    Educational Psychologist, 51(1), 23-34.
    - 理性思维的多维评估框架
    - 认知去偏(Cognitive Debiasing)技术

12. Klayman, J., & Ha, Y. W. (1987). Confirmation, disconfirmation, and information in 
    hypothesis testing. Psychological Review, 94(2), 211-228.
    - 假设检验中的确认偏误机制
    - 积极检验策略vs消极检验策略

13. Nickerson, R. S. (1998). Confirmation bias: A ubiquitous phenomenon in many guises. 
    Review of General Psychology, 2(2), 175-220.
    - 确认偏误的多种表现形式
    - 反驳生成的认知障碍

14. Hahn, U., & Oaksford, M. (2007). The rationality of informal argumentation: 
    A Bayesian approach to reasoning fallacies. Psychological Review, 114(3), 704-732.
    - 贝叶斯推理在非正式论证中的应用
    - 论证谬误的概率解释

15. Corner, A., Hahn, U., & Oaksford, M. (2011). The psychological mechanism of the 
    slippery slope argument. Journal of Memory and Language, 64(2), 133-152.
    - 滑坡论证的心理机制
    - 因果链推理的认知模型
16. Evan
s, J. S. B. T. (2008). Dual-process accounts of reasoning, judgment, and social cognition. 
    Annual Review of Psychology, 59, 255-278.
    - 双重过程理论在推理中的应用
    - 类型1和类型2处理的交互机制

17. Gigerenzer, G., & Gaissmaier, W. (2011). Heuristic decision making. 
    Annual Review of Psychology, 62, 451-482.
    - 启发式推理的生态理性
    - 快速节俭启发式(Fast-and-frugal heuristics)

18. Tetlock, P. E., & Gardner, D. (2015). Superforecasting: The Art and Science of Prediction. 
    Crown Publishers.
    - 超级预测者的认知特征
    - 积极开放思维(Actively Open-minded Thinking)

19. Baron, J. (2008). Thinking and Deciding. Cambridge University Press.
    - 理性决策的规范理论
    - 认知偏误的去偏技术

20. Keren, G., & Schul, Y. (2009). Two is not always better than one: A critical evaluation 
    of two-system theories. Perspectives on Psychological Science, 4(6), 533-550.
    - 双重过程理论的批判性评估
    - 单一过程模型的替代解释
"""

import logging
import random
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import numpy as np
from collections import defaultdict, Counter
import json

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArgumentationScheme(Enum):
    """
    基于Walton等人(2008)的论证模式分类
    """
    # 因果论证模式
    ARGUMENT_FROM_CAUSE_TO_EFFECT = "cause_to_effect"
    ARGUMENT_FROM_EFFECT_TO_CAUSE = "effect_to_cause"
    ARGUMENT_FROM_CORRELATION_TO_CAUSE = "correlation_to_cause"
    
    # 权威论证模式
    ARGUMENT_FROM_EXPERT_OPINION = "expert_opinion"
    ARGUMENT_FROM_POSITION_TO_KNOW = "position_to_know"
    ARGUMENT_FROM_WITNESS_TESTIMONY = "witness_testimony"
    
    # 类比论证模式
    ARGUMENT_FROM_ANALOGY = "analogy"
    ARGUMENT_FROM_PRECEDENT = "precedent"
    ARGUMENT_A_FORTIORI = "a_fortiori"
    
    # 符号论证模式
    ARGUMENT_FROM_SIGN = "sign"
    ARGUMENT_FROM_CLASSIFICATION = "classification"
    ARGUMENT_FROM_DEFINITION = "definition"
    
    # 实用论证模式
    PRACTICAL_REASONING = "practical_reasoning"
    ARGUMENT_FROM_CONSEQUENCES = "consequences"
    ARGUMENT_FROM_WASTE = "waste"
    
    # 道德论证模式
    ARGUMENT_FROM_VALUES = "values"
    ARGUMENT_FROM_COMMITMENT = "commitment"
    ARGUMENT_FROM_FAIRNESS = "fairness"

class CognitiveBias(Enum):
    """
    基于Kahneman(2011)和Nickerson(1998)的认知偏误分类
    """
    CONFIRMATION_BIAS = "confirmation_bias"
    AVAILABILITY_HEURISTIC = "availability_heuristic"
    ANCHORING_BIAS = "anchoring_bias"
    REPRESENTATIVENESS_HEURISTIC = "representativeness_heuristic"
    OVERCONFIDENCE_BIAS = "overconfidence_bias"
    HINDSIGHT_BIAS = "hindsight_bias"
    FRAMING_EFFECT = "framing_effect"
    SUNK_COST_FALLACY = "sunk_cost_fallacy"
    BASE_RATE_NEGLECT = "base_rate_neglect"
    CONJUNCTION_FALLACY = "conjunction_fallacy"

@dataclass
class CriticalQuestion:
    """
    基于Walton等人(2008)的批判性问题框架
    """
    question: str
    scheme: ArgumentationScheme
    attack_type: str  # "premise", "inference", "exception"
    cognitive_load: float  # 0.0-1.0, 问题的认知复杂度
    bias_target: Optional[CognitiveBias] = None

@dataclass
class ArgumentStructure:
    """
    基于Toulmin(2003)模型的论证结构
    """
    claim: str
    data: List[str]
    warrant: str
    backing: Optional[str] = None
    qualifier: Optional[str] = None
    rebuttal: Optional[str] = None
    strength: float = 0.5  # 0.0-1.0
    confidence: float = 0.5  # 0.0-1.0

@dataclass
class CounterArgument:
    """
    反驳论证的结构化表示
    """
    target_claim: str
    counter_claim: str
    attack_type: str  # "undercut", "rebut", "undermine"
    evidence: List[str]
    strength: float
    scheme: ArgumentationScheme
    critical_questions: List[CriticalQuestion]
    cognitive_biases_exploited: List[CognitiveBias] = field(default_factory=list)

class ArgumentAttackType(Enum):
    """
    基于Prakken(2010)的论证攻击类型
    """
    UNDERCUT = "undercut"  # 攻击推理规则
    REBUT = "rebut"       # 攻击结论
    UNDERMINE = "undermine"  # 攻击前提

class ReasoningMode(Enum):
    """
    基于Evans(2008)的双重过程理论
    """
    SYSTEM_1 = "system_1"  # 快速、直觉、自动
    SYSTEM_2 = "system_2"  # 慢速、分析、控制

class AdvancedAntithesisEngine:
    """
    基于前沿认知科学研究的高级反题生成引擎
    
    核心创新：
    1. 多层次论证攻击策略
    2. 认知偏误的系统性利用
    3. 元认知监控和调节
    4. 适应性反驳生成
    """
    
    def __init__(self, ai_config: Optional[Dict] = None):
        self.ai_config = ai_config or {}
        self.reasoning_mode = ReasoningMode.SYSTEM_2
        
        # 初始化论证模式库
        self.argumentation_schemes = self._initialize_argumentation_schemes()
        
        # 初始化批判性问题库
        self.critical_questions_db = self._initialize_critical_questions()
        
        # 初始化认知偏误检测器
        self.bias_detector = CognitiveBiasDetector()
        
        # 初始化元认知监控器
        self.metacognitive_monitor = MetacognitiveMonitor()
        
        # 论证历史记录
        self.argument_history: List[ArgumentStructure] = []
        self.counter_argument_history: List[CounterArgument] = []
        
        logger.info("高级反题引擎初始化完成")
    
    def generate_antithesis(self, thesis: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成系统性反题，基于多重认知科学理论
        
        Args:
            thesis: 包含原始论证的字典
            
        Returns:
            包含反题论证的字典
        """
        logger.info(f"开始生成反题，针对论题: {thesis.get('claim', 'Unknown')}")
        
        # 第一步：解析和结构化原始论证
        structured_thesis = self._parse_argument_structure(thesis)
        
        # 第二步：检测潜在的认知偏误
        detected_biases = self.bias_detector.detect_biases(structured_thesis)
        
        # 第三步：生成多层次反驳策略
        attack_strategies = self._generate_attack_strategies(structured_thesis, detected_biases)
        
        # 第四步：应用论证模式生成具体反驳
        counter_arguments = []
        for strategy in attack_strategies:
            counter_arg = self._apply_argumentation_scheme(strategy, structured_thesis)
            if counter_arg:
                counter_arguments.append(counter_arg)
        
        # 第五步：元认知评估和优化
        optimized_counter_args = self.metacognitive_monitor.evaluate_and_optimize(
            counter_arguments, structured_thesis
        )
        
        # 第六步：选择最强反驳
        best_counter_argument = self._select_strongest_counter_argument(optimized_counter_args)
        
        # 记录到历史
        self.argument_history.append(structured_thesis)
        if best_counter_argument:
            self.counter_argument_history.append(best_counter_argument)
        
        return self._format_antithesis_output(best_counter_argument, detected_biases)
    
    def _parse_argument_structure(self, thesis: Dict[str, Any]) -> ArgumentStructure:
        """
        基于Toulmin模型解析论证结构
        """
        claim = thesis.get('claim', thesis.get('conclusion', ''))
        premises = thesis.get('premises', thesis.get('reasons', []))
        
        # 提取warrant（推理规则）
        warrant = thesis.get('warrant', self._infer_warrant(claim, premises))
        
        # 评估论证强度
        strength = self._calculate_argument_strength(claim, premises, warrant)
        
        return ArgumentStructure(
            claim=claim,
            data=premises if isinstance(premises, list) else [premises],
            warrant=warrant,
            strength=strength,
            confidence=thesis.get('confidence', 0.7)
        )
    
    def _infer_warrant(self, claim: str, premises: List[str]) -> str:
        """
        推断隐含的推理规则（warrant）
        """
        # 简化实现：基于关键词匹配推断推理类型
        claim_lower = claim.lower()
        premises_text = ' '.join(premises).lower()
        
        if any(word in claim_lower for word in ['应该', 'should', '必须', 'must']):
            return "道德原则要求我们采取符合伦理的行动"
        elif any(word in premises_text for word in ['因为', 'because', '导致', 'cause']):
            return "因果关系表明前因决定后果"
        elif any(word in premises_text for word in ['专家', 'expert', '权威', 'authority']):
            return "专家意见在其专业领域内具有可信度"
        else:
            return "一般推理原则支持从前提到结论的推导"
    
    def _calculate_argument_strength(self, claim: str, premises: List[str], warrant: str) -> float:
        """
        基于多个维度计算论证强度
        """
        # 前提数量权重
        premise_weight = min(len(premises) * 0.2, 0.6)
        
        # 语言确定性权重
        certainty_words = ['确定', '肯定', '必然', 'certain', 'definitely', 'surely']
        uncertainty_words = ['可能', '也许', '大概', 'maybe', 'perhaps', 'possibly']
        
        text = (claim + ' ' + ' '.join(premises)).lower()
        certainty_score = sum(1 for word in certainty_words if word in text)
        uncertainty_score = sum(1 for word in uncertainty_words if word in text)
        
        certainty_weight = (certainty_score - uncertainty_score * 0.5) * 0.1
        certainty_weight = max(0, min(certainty_weight, 0.3))
        
        # 基础强度
        base_strength = 0.5
        
        return min(base_strength + premise_weight + certainty_weight, 1.0)
    
    def _generate_attack_strategies(self, thesis: ArgumentStructure, biases: List[CognitiveBias]) -> List[Dict]:
        """
        基于检测到的偏误生成攻击策略
        """
        strategies = []
        
        # 策略1：前提攻击（Undermine）
        for i, premise in enumerate(thesis.data):
            strategies.append({
                'type': ArgumentAttackType.UNDERMINE,
                'target': f"premise_{i}",
                'content': premise,
                'biases_to_exploit': [bias for bias in biases if self._bias_affects_premise(bias, premise)]
            })
        
        # 策略2：推理攻击（Undercut）
        strategies.append({
            'type': ArgumentAttackType.UNDERCUT,
            'target': 'warrant',
            'content': thesis.warrant,
            'biases_to_exploit': [bias for bias in biases if self._bias_affects_inference(bias)]
        })
        
        # 策略3：结论攻击（Rebut）
        strategies.append({
            'type': ArgumentAttackType.REBUT,
            'target': 'claim',
            'content': thesis.claim,
            'biases_to_exploit': biases
        })
        
        return strategies
    
    def _bias_affects_premise(self, bias: CognitiveBias, premise: str) -> bool:
        """
        判断认知偏误是否影响特定前提
        """
        premise_lower = premise.lower()
        
        if bias == CognitiveBias.AVAILABILITY_HEURISTIC:
            return any(word in premise_lower for word in ['最近', '经常', '记得', 'recent', 'often', 'remember'])
        elif bias == CognitiveBias.CONFIRMATION_BIAS:
            return any(word in premise_lower for word in ['证实', '支持', '证明', 'confirm', 'support', 'prove'])
        elif bias == CognitiveBias.ANCHORING_BIAS:
            return any(word in premise_lower for word in ['首先', '最初', '开始', 'first', 'initial', 'start'])
        
        return False
    
    def _bias_affects_inference(self, bias: CognitiveBias) -> bool:
        """
        判断认知偏误是否影响推理过程
        """
        inference_affecting_biases = {
            CognitiveBias.REPRESENTATIVENESS_HEURISTIC,
            CognitiveBias.BASE_RATE_NEGLECT,
            CognitiveBias.CONJUNCTION_FALLACY,
            CognitiveBias.FRAMING_EFFECT
        }
        return bias in inference_affecting_biases
    
    def _apply_argumentation_scheme(self, strategy: Dict, thesis: ArgumentStructure) -> Optional[CounterArgument]:
        """
        应用特定的论证模式生成反驳
        """
        attack_type = strategy['type']
        target = strategy['target']
        content = strategy['content']
        biases = strategy['biases_to_exploit']
        
        # 根据攻击类型选择合适的论证模式
        if attack_type == ArgumentAttackType.UNDERMINE:
            return self._generate_premise_attack(content, biases)
        elif attack_type == ArgumentAttackType.UNDERCUT:
            return self._generate_inference_attack(content, biases)
        elif attack_type == ArgumentAttackType.REBUT:
            return self._generate_conclusion_attack(content, biases)
        
        return None
    
    def _generate_premise_attack(self, premise: str, biases: List[CognitiveBias]) -> CounterArgument:
        """
        生成针对前提的攻击
        """
        # 选择合适的论证模式
        scheme = ArgumentationScheme.ARGUMENT_FROM_EXPERT_OPINION
        
        # 生成反驳声明
        counter_claim = f"前提'{premise}'存在以下问题："
        
        # 基于偏误生成具体攻击
        evidence = []
        for bias in biases:
            if bias == CognitiveBias.AVAILABILITY_HEURISTIC:
                evidence.append("该前提可能受到可得性启发式影响，过分依赖容易回忆的信息")
            elif bias == CognitiveBias.CONFIRMATION_BIAS:
                evidence.append("该前提可能存在确认偏误，只选择支持既定观点的证据")
            elif bias == CognitiveBias.ANCHORING_BIAS:
                evidence.append("该前提可能受到锚定效应影响，过分依赖初始信息")
        
        if not evidence:
            evidence.append("该前提缺乏充分的实证支持")
        
        # 生成批判性问题
        critical_questions = [
            CriticalQuestion(
                question="该前提的证据来源是否可靠？",
                scheme=scheme,
                attack_type="premise",
                cognitive_load=0.6
            ),
            CriticalQuestion(
                question="是否存在与该前提相矛盾的证据？",
                scheme=scheme,
                attack_type="premise",
                cognitive_load=0.7
            )
        ]
        
        return CounterArgument(
            target_claim=premise,
            counter_claim=counter_claim,
            attack_type="undermine",
            evidence=evidence,
            strength=0.7,
            scheme=scheme,
            critical_questions=critical_questions,
            cognitive_biases_exploited=biases
        )
    
    def _generate_inference_attack(self, warrant: str, biases: List[CognitiveBias]) -> CounterArgument:
        """
        生成针对推理规则的攻击
        """
        scheme = ArgumentationScheme.ARGUMENT_FROM_CLASSIFICATION
        
        counter_claim = f"推理规则'{warrant}'存在逻辑缺陷："
        
        evidence = [
            "该推理规则可能存在隐含假设",
            "从前提到结论的推导可能存在逻辑跳跃",
            "可能存在其他同样合理的推理路径"
        ]
        
        # 基于偏误添加特定攻击
        for bias in biases:
            if bias == CognitiveBias.REPRESENTATIVENESS_HEURISTIC:
                evidence.append("该推理可能忽略了基础概率信息")
            elif bias == CognitiveBias.FRAMING_EFFECT:
                evidence.append("该推理可能受到问题框架的不当影响")
        
        critical_questions = [
            CriticalQuestion(
                question="该推理规则是否在所有情况下都成立？",
                scheme=scheme,
                attack_type="inference",
                cognitive_load=0.8
            ),
            CriticalQuestion(
                question="是否存在例外情况使该推理无效？",
                scheme=scheme,
                attack_type="exception",
                cognitive_load=0.7
            )
        ]
        
        return CounterArgument(
            target_claim=warrant,
            counter_claim=counter_claim,
            attack_type="undercut",
            evidence=evidence,
            strength=0.8,
            scheme=scheme,
            critical_questions=critical_questions,
            cognitive_biases_exploited=biases
        )
    
    def _generate_conclusion_attack(self, claim: str, biases: List[CognitiveBias]) -> CounterArgument:
        """
        生成针对结论的直接反驳
        """
        scheme = ArgumentationScheme.ARGUMENT_FROM_CONSEQUENCES
        
        counter_claim = f"结论'{claim}'可能是错误的，因为："
        
        evidence = [
            "存在替代性解释可以更好地解释现有证据",
            "该结论的实际后果可能与预期不符",
            "可能存在未考虑的重要因素"
        ]
        
        # 基于偏误生成特定反驳
        for bias in biases:
            if bias == CognitiveBias.OVERCONFIDENCE_BIAS:
                evidence.append("该结论可能过于自信，忽略了不确定性")
            elif bias == CognitiveBias.HINDSIGHT_BIAS:
                evidence.append("该结论可能受到后见之明偏误的影响")
        
        critical_questions = [
            CriticalQuestion(
                question="该结论是否考虑了所有相关因素？",
                scheme=scheme,
                attack_type="premise",
                cognitive_load=0.6
            ),
            CriticalQuestion(
                question="是否存在更合理的替代结论？",
                scheme=scheme,
                attack_type="premise",
                cognitive_load=0.8
            )
        ]
        
        return CounterArgument(
            target_claim=claim,
            counter_claim=counter_claim,
            attack_type="rebut",
            evidence=evidence,
            strength=0.6,
            scheme=scheme,
            critical_questions=critical_questions,
            cognitive_biases_exploited=biases
        )
    
    def _select_strongest_counter_argument(self, counter_arguments: List[CounterArgument]) -> Optional[CounterArgument]:
        """
        选择最强的反驳论证
        """
        if not counter_arguments:
            return None
        
        # 基于多个维度评分
        def score_counter_argument(counter_arg: CounterArgument) -> float:
            base_score = counter_arg.strength
            
            # 证据数量加分
            evidence_bonus = min(len(counter_arg.evidence) * 0.1, 0.3)
            
            # 批判性问题质量加分
            question_bonus = sum(1 - q.cognitive_load for q in counter_arg.critical_questions) * 0.1
            
            # 偏误利用加分
            bias_bonus = len(counter_arg.cognitive_biases_exploited) * 0.05
            
            return base_score + evidence_bonus + question_bonus + bias_bonus
        
        scored_arguments = [(score_counter_argument(ca), ca) for ca in counter_arguments]
        scored_arguments.sort(key=lambda x: x[0], reverse=True)
        
        return scored_arguments[0][1]
    
    def _format_antithesis_output(self, counter_argument: Optional[CounterArgument], biases: List[CognitiveBias]) -> Dict[str, Any]:
        """
        格式化反题输出
        """
        if not counter_argument:
            return {
                'success': False,
                'message': '无法生成有效的反题论证',
                'detected_biases': [bias.value for bias in biases]
            }
        
        return {
            'success': True,
            'counter_claim': counter_argument.counter_claim,
            'attack_type': counter_argument.attack_type,
            'evidence': counter_argument.evidence,
            'strength': counter_argument.strength,
            'argumentation_scheme': counter_argument.scheme.value,
            'critical_questions': [
                {
                    'question': cq.question,
                    'attack_type': cq.attack_type,
                    'cognitive_load': cq.cognitive_load
                }
                for cq in counter_argument.critical_questions
            ],
            'detected_biases': [bias.value for bias in biases],
            'exploited_biases': [bias.value for bias in counter_argument.cognitive_biases_exploited],
            'reasoning_mode': self.reasoning_mode.value,
            'meta_analysis': {
                'argument_complexity': len(counter_argument.evidence),
                'cognitive_demand': sum(cq.cognitive_load for cq in counter_argument.critical_questions) / len(counter_argument.critical_questions) if counter_argument.critical_questions else 0,
                'bias_awareness': len(counter_argument.cognitive_biases_exploited)
            }
        }
    
    def _initialize_argumentation_schemes(self) -> Dict[ArgumentationScheme, Dict]:
        """
        初始化论证模式库
        """
        return {
            ArgumentationScheme.ARGUMENT_FROM_EXPERT_OPINION: {
                'critical_questions': [
                    "该专家在相关领域是否真正具有专业知识？",
                    "该专家是否可能存在利益冲突？",
                    "专家之间是否存在意见分歧？"
                ],
                'strength_factors': ['expertise_level', 'consensus', 'bias_potential']
            },
            ArgumentationScheme.ARGUMENT_FROM_CAUSE_TO_EFFECT: {
                'critical_questions': [
                    "该因果关系是否得到充分证实？",
                    "是否存在其他可能的原因？",
                    "该因果机制是否合理？"
                ],
                'strength_factors': ['causal_evidence', 'alternative_causes', 'mechanism_plausibility']
            },
            ArgumentationScheme.PRACTICAL_REASONING: {
                'critical_questions': [
                    "该目标是否值得追求？",
                    "该行动是否能有效实现目标？",
                    "是否存在更好的替代方案？"
                ],
                'strength_factors': ['goal_value', 'action_effectiveness', 'alternative_options']
            }
        }
    
    def _initialize_critical_questions(self) -> Dict[ArgumentationScheme, List[CriticalQuestion]]:
        """
        初始化批判性问题数据库
        """
        return {
            ArgumentationScheme.ARGUMENT_FROM_EXPERT_OPINION: [
                CriticalQuestion(
                    "该专家在相关领域的专业程度如何？",
                    ArgumentationScheme.ARGUMENT_FROM_EXPERT_OPINION,
                    "premise",
                    0.6,
                    CognitiveBias.AVAILABILITY_HEURISTIC
                ),
                CriticalQuestion(
                    "该专家是否可能存在偏见或利益冲突？",
                    ArgumentationScheme.ARGUMENT_FROM_EXPERT_OPINION,
                    "premise",
                    0.7,
                    CognitiveBias.CONFIRMATION_BIAS
                )
            ]
        }

class CognitiveBiasDetector:
    """
    认知偏误检测器，基于最新心理学研究
    """
    
    def __init__(self):
        self.bias_patterns = self._initialize_bias_patterns()
    
    def detect_biases(self, argument: ArgumentStructure) -> List[CognitiveBias]:
        """
        检测论证中可能存在的认知偏误
        """
        detected_biases = []
        
        # 检测确认偏误
        if self._detect_confirmation_bias(argument):
            detected_biases.append(CognitiveBias.CONFIRMATION_BIAS)
        
        # 检测可得性启发式
        if self._detect_availability_heuristic(argument):
            detected_biases.append(CognitiveBias.AVAILABILITY_HEURISTIC)
        
        # 检测锚定偏误
        if self._detect_anchoring_bias(argument):
            detected_biases.append(CognitiveBias.ANCHORING_BIAS)
        
        # 检测过度自信
        if self._detect_overconfidence_bias(argument):
            detected_biases.append(CognitiveBias.OVERCONFIDENCE_BIAS)
        
        return detected_biases
    
    def _detect_confirmation_bias(self, argument: ArgumentStructure) -> bool:
        """
        检测确认偏误的语言模式
        """
        confirmation_indicators = [
            '证实', '支持', '证明', '显示', '表明',
            'confirm', 'support', 'prove', 'show', 'demonstrate'
        ]
        
        text = (argument.claim + ' ' + ' '.join(argument.data)).lower()
        return any(indicator in text for indicator in confirmation_indicators)
    
    def _detect_availability_heuristic(self, argument: ArgumentStructure) -> bool:
        """
        检测可得性启发式的使用
        """
        availability_indicators = [
            '最近', '经常', '记得', '听说', '看到',
            'recent', 'often', 'remember', 'heard', 'seen'
        ]
        
        text = (argument.claim + ' ' + ' '.join(argument.data)).lower()
        return any(indicator in text for indicator in availability_indicators)
    
    def _detect_anchoring_bias(self, argument: ArgumentStructure) -> bool:
        """
        检测锚定偏误
        """
        anchoring_indicators = [
            '首先', '最初', '开始', '第一', '起初',
            'first', 'initial', 'start', 'begin', 'originally'
        ]
        
        text = (argument.claim + ' ' + ' '.join(argument.data)).lower()
        return any(indicator in text for indicator in anchoring_indicators)
    
    def _detect_overconfidence_bias(self, argument: ArgumentStructure) -> bool:
        """
        检测过度自信偏误
        """
        # 基于论证强度和确定性语言
        overconfidence_indicators = [
            '绝对', '肯定', '必然', '毫无疑问', '显然',
            'absolutely', 'definitely', 'certainly', 'obviously', 'clearly'
        ]
        
        text = (argument.claim + ' ' + ' '.join(argument.data)).lower()
        has_strong_language = any(indicator in text for indicator in overconfidence_indicators)
        
        # 如果使用强烈确定性语言但论证强度不高，可能存在过度自信
        return has_strong_language and argument.strength < 0.7
    
    def _initialize_bias_patterns(self) -> Dict[CognitiveBias, Dict]:
        """
        初始化偏误检测模式
        """
        return {
            CognitiveBias.CONFIRMATION_BIAS: {
                'keywords': ['证实', '支持', '证明', 'confirm', 'support', 'prove'],
                'patterns': ['只考虑支持性证据', '忽略反驳证据'],
                'detection_threshold': 0.6
            },
            CognitiveBias.AVAILABILITY_HEURISTIC: {
                'keywords': ['最近', '经常', '记得', 'recent', 'often', 'remember'],
                'patterns': ['依赖容易回忆的信息', '忽略统计数据'],
                'detection_threshold': 0.5
            }
        }

class MetacognitiveMonitor:
    """
    元认知监控器，基于Tetlock & Gardner (2015)的超级预测研究
    """
    
    def __init__(self):
        self.evaluation_criteria = self._initialize_evaluation_criteria()
    
    def evaluate_and_optimize(self, counter_arguments: List[CounterArgument], original_argument: ArgumentStructure) -> List[CounterArgument]:
        """
        元认知评估和优化反驳论证
        """
        optimized_arguments = []
        
        for counter_arg in counter_arguments:
            # 评估论证质量
            quality_score = self._evaluate_argument_quality(counter_arg)
            
            # 评估认知负荷
            cognitive_load = self._calculate_cognitive_load(counter_arg)
            
            # 评估说服力
            persuasiveness = self._evaluate_persuasiveness(counter_arg, original_argument)
            
            # 基于评估结果优化论证
            if quality_score > 0.6 and cognitive_load < 0.8:
                optimized_counter_arg = self._optimize_counter_argument(counter_arg, quality_score, cognitive_load, persuasiveness)
                optimized_arguments.append(optimized_counter_arg)
        
        return optimized_arguments
    
    def _evaluate_argument_quality(self, counter_arg: CounterArgument) -> float:
        """
        评估反驳论证的质量
        """
        # 证据质量
        evidence_quality = min(len(counter_arg.evidence) * 0.2, 1.0)
        
        # 逻辑一致性
        logical_consistency = 0.8  # 简化实现
        
        # 批判性问题的深度
        question_depth = sum(1 - cq.cognitive_load for cq in counter_arg.critical_questions) / len(counter_arg.critical_questions) if counter_arg.critical_questions else 0
        
        return (evidence_quality + logical_consistency + question_depth) / 3
    
    def _calculate_cognitive_load(self, counter_arg: CounterArgument) -> float:
        """
        计算认知负荷
        """
        # 基于批判性问题的复杂度
        if counter_arg.critical_questions:
            avg_load = sum(cq.cognitive_load for cq in counter_arg.critical_questions) / len(counter_arg.critical_questions)
        else:
            avg_load = 0.5
        
        # 证据复杂度
        evidence_complexity = min(len(counter_arg.evidence) * 0.1, 0.5)
        
        return min(avg_load + evidence_complexity, 1.0)
    
    def _evaluate_persuasiveness(self, counter_arg: CounterArgument, original_arg: ArgumentStructure) -> float:
        """
        评估说服力
        """
        # 攻击类型的有效性
        attack_effectiveness = {
            'undermine': 0.7,
            'undercut': 0.8,
            'rebut': 0.6
        }.get(counter_arg.attack_type, 0.5)
        
        # 强度对比
        strength_advantage = max(0, counter_arg.strength - original_arg.strength)
        
        # 偏误利用的有效性
        bias_effectiveness = len(counter_arg.cognitive_biases_exploited) * 0.1
        
        return min(attack_effectiveness + strength_advantage + bias_effectiveness, 1.0)
    
    def _optimize_counter_argument(self, counter_arg: CounterArgument, quality: float, cognitive_load: float, persuasiveness: float) -> CounterArgument:
        """
        优化反驳论证
        """
        # 如果认知负荷过高，简化批判性问题
        if cognitive_load > 0.7:
            simplified_questions = [cq for cq in counter_arg.critical_questions if cq.cognitive_load < 0.7]
            counter_arg.critical_questions = simplified_questions[:3]  # 最多保留3个问题
        
        # 如果说服力不足，增强证据
        if persuasiveness < 0.6:
            additional_evidence = self._generate_additional_evidence(counter_arg)
            counter_arg.evidence.extend(additional_evidence)
        
        # 调整强度评分
        counter_arg.strength = min(counter_arg.strength * (1 + quality * 0.2), 1.0)
        
        return counter_arg
    
    def _generate_additional_evidence(self, counter_arg: CounterArgument) -> List[str]:
        """
        生成额外的支持证据
        """
        additional_evidence = []
        
        if counter_arg.attack_type == 'undermine':
            additional_evidence.append("相关研究表明该前提的可靠性存在争议")
        elif counter_arg.attack_type == 'undercut':
            additional_evidence.append("逻辑分析显示该推理存在潜在缺陷")
        elif counter_arg.attack_type == 'rebut':
            additional_evidence.append("替代性解释提供了更合理的结论")
        
        return additional_evidence
    
    def _initialize_evaluation_criteria(self) -> Dict:
        """
        初始化评估标准
        """
        return {
            'argument_quality': {
                'evidence_sufficiency': 0.3,
                'logical_consistency': 0.3,
                'critical_depth': 0.4
            },
            'cognitive_load': {
                'complexity_threshold': 0.8,
                'question_limit': 5,
                'evidence_limit': 7
            },
            'persuasiveness': {
                'attack_effectiveness': 0.4,
                'strength_advantage': 0.3,
                'bias_utilization': 0.3
            }
        }

# 使用示例和测试
if __name__ == "__main__":
    # 创建高级反题引擎实例
    engine = AdvancedAntithesisEngine()
    
    # 测试论证
    test_thesis = {
        'claim': '人工智能应该在医疗诊断中完全替代人类医生',
        'premises': [
            'AI诊断准确率比人类医生高',
            '专家研究表明AI可以减少医疗错误',
            'AI不会疲劳，可以24小时工作'
        ],
        'confidence': 0.8
    }
    
    # 生成反题
    result = engine.generate_antithesis(test_thesis)
    
    # 输出结果
    print("=== 高级反题生成结果 ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))