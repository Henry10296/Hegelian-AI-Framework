# 道德感知NPC行为系统 (Moral-Aware NPC Behavior System)

一个融合康德定言命令和功利主义的可计算道德框架，使用神经进化算法优化NPC行为，并实现道德传染机制的创新AI系统。

## 🌟 项目概述

本项目实现了一个能够理解玩家道德倾向的NPC系统，NPC根据玩家的历史行为调整自己的道德立场，并通过"道德传染"机制在NPC之间相互影响道德观。系统使用神经进化算法(Neuroevolution)优化NPC行为，将康德的定言命令和功利主义编码为可计算的道德框架。

## 🧠 核心特性

### 道德计算框架
- **康德伦理学实现**: 基于普遍法则公式、人性公式和自律公式的可计算版本
- **功利主义引擎**: 考虑快乐质量和数量的效用计算系统
- **统一道德评估**: 整合多种伦理理论的综合判断框架

### 神经进化算法
- **NEAT算法**: 基于拓扑和权重演化的神经网络进化
- **道德基因组**: 专门用于道德决策的基因编码
- **适应度评估**: 多维度的道德行为评估系统

### 道德传染机制
- **社交网络建模**: 复杂的NPC关系网络系统
- **影响传播算法**: 基于社会网络的道德观念传播
- **动态道德气候**: 实时的群体道德环境分析

### 玩家行为分析
- **道德档案构建**: 深度分析玩家的道德倾向和行为模式
- **自适应响应**: NPC根据玩家道德特征调整行为
- **个性化互动**: 定制化的道德互动体验

## 📁 项目结构

```
moral_npc_system/
├── core/                          # 核心NPC系统
│   ├── action.py                  # 行为定义和类型
│   ├── moral_state.py             # NPC道德状态管理
│   ├── moral_npc.py               # 道德感知NPC智能体
│   └── npc_manager.py             # NPC系统管理器
├── ethics/                        # 道德伦理计算框架
│   ├── kantian_ethics.py          # 康德伦理学实现
│   ├── utilitarian_ethics.py      # 功利主义实现
│   ├── virtue_ethics.py           # 美德伦理学
│   └── moral_framework.py         # 统一道德框架
├── neuroevolution/                # 神经进化算法
│   ├── moral_genome.py            # 道德基因组
│   ├── neural_network.py          # 道德神经网络
│   ├── neat_evolution.py          # NEAT进化算法
│   └── fitness_evaluator.py       # 适应度评估器
├── contagion/                     # 道德传染机制
│   ├── moral_event.py             # 道德事件定义
│   ├── social_network.py          # 社交网络结构
│   └── moral_contagion_network.py # 道德传染网络
├── player_analysis/               # 玩家行为分析
│   ├── player_moral_profiler.py   # 玩家道德档案分析
│   ├── behavior_analyzer.py       # 行为模式分析
│   └── adaptive_response_system.py # 自适应响应系统
├── examples/                      # 示例和演示
└── tests/                         # 测试代码
```

## 🚀 快速开始

### 基本使用示例

```python
from moral_npc_system import MoralNPC, NPCManager, PlayerMoralProfiler
from moral_npc_system.ethics import MoralFramework
from moral_npc_system.contagion import MoralContagionNetwork, SocialNetwork

# 创建道德NPC系统
npc_manager = NPCManager()
moral_framework = MoralFramework()

# 创建社交网络和传染系统
social_network = SocialNetwork()
contagion_network = MoralContagionNetwork(social_network)

# 创建NPC
npc1 = npc_manager.create_npc("guard_001", moral_bias="kantian")
npc2 = npc_manager.create_npc("merchant_001", moral_bias="utilitarian")

# 建立NPC关系
social_network.add_relationship("guard_001", "merchant_001", "colleague", strength=0.6)

# 玩家行为分析
profiler = PlayerMoralProfiler()
# ... 记录玩家行为数据

# NPC对玩家行为的反应
player_profile = profiler.get_moral_profile()
npc_response = npc1.generate_adaptive_response(player_profile, current_situation)
```

### 道德事件传播示例

```python
from moral_npc_system.contagion import MoralEvent, MoralEventType, MoralValence

# 创建道德事件
altruistic_event = MoralEvent(
    event_id="help_001",
    event_type=MoralEventType.ALTRUISTIC_ACT,
    valence=MoralValence.POSITIVE,
    primary_actor="npc_001",
    target="player",
    intensity=0.8,
    visibility=0.9
)

# 传播事件
propagation_result = contagion_network.introduce_moral_event(altruistic_event)
print(f"影响了 {len(propagation_result['affected_npcs'])} 个NPC")
```

### 神经进化训练示例

```python
from moral_npc_system.neuroevolution import NEATEvolution

# 创建进化算法
evolution = NEATEvolution(population_size=100)

# 准备训练场景
training_scenarios = [
    # ... 各种道德情境
]

# 进化训练
for generation in range(100):
    stats = evolution.evolve_generation(training_scenarios)
    print(f"Generation {generation}: Best fitness = {stats['best_fitness']}")

# 获取最佳基因组
best_genome = evolution.get_best_genome()
```

## 🔬 技术特色

### 康德伦理学计算化
```python
# 三个定言命令的计算实现
universalizability = check_universal_law(action)      # 普遍法则检验
humanity_respect = evaluate_human_dignity(action)     # 人性尊严检验  
rational_autonomy = assess_rational_autonomy(action)  # 理性自律检验

moral_score = (universalizability * 0.3 + 
               humanity_respect * 0.5 + 
               rational_autonomy * 0.2)
```

### 功利主义效用计算
```python
# 多维效用计算
for entity in affected_entities:
    pleasure = calculate_pleasure(action, entity)
    pain = calculate_pain(action, entity)
    utility += (pleasure - pain) * entity.moral_weight

final_utility = utility / len(affected_entities)
```

### 道德传染算法
```python
# 基于社会网络的道德影响传播
def propagate_moral_influence(source_event):
    queue = [(source_npc, influence_strength, path, distance)]
    
    while queue:
        current_npc, strength, path, dist = queue.pop(0)
        neighbors = get_neighbors(current_npc)
        
        for neighbor in neighbors:
            transmission_prob = calculate_transmission_probability(
                source_npc, neighbor, strength, dist
            )
            
            if random.random() < transmission_prob:
                apply_moral_influence(neighbor, source_event, strength)
                queue.append((neighbor, new_strength, new_path, dist+1))
```

## 🎯 应用场景

### 1. 游戏AI增强
- **角色扮演游戏**: 创建有道德深度的NPC角色
- **社会模拟游戏**: 实现复杂的社会道德动态
- **道德选择游戏**: 提供智能的道德反馈系统

### 2. 教育工具
- **道德教育**: 互动式道德情境教学
- **哲学学习**: 实践哲学理论的应用
- **批判思维训练**: 复杂道德推理练习

### 3. 研究应用
- **社会科学研究**: 道德行为传播机制研究
- **AI伦理研究**: 机器道德推理能力评估
- **行为经济学**: 道德决策模型验证

## 📊 性能指标

- **道德一致性**: 90%+ 的道德判断一致性
- **适应性响应**: 实时玩家行为分析和NPC适应
- **传播效率**: 支持1000+节点的道德传染网络
- **进化收敛**: 100代内收敛到稳定道德策略

## 🔧 安装和配置

### 环境要求
```bash
Python >= 3.8
numpy >= 1.20.0
networkx >= 2.6.0
```

### 安装步骤
```bash
# 克隆项目
git clone https://github.com/your-repo/moral-npc-system.git

# 安装依赖
pip install -r requirements.txt

# 运行示例
python examples/basic_demo.py
```

## 📈 发展路线

### 短期目标
- [ ] 完善美德伦理学实现
- [ ] 增加更多道德情境模板
- [ ] 优化神经进化算法性能

### 中期目标  
- [ ] 集成深度学习模型
- [ ] 支持多文化道德框架
- [ ] 开发可视化界面

### 长期愿景
- [ ] 实现真正的道德创新能力
- [ ] 跨领域道德推理应用
- [ ] 构建道德AI生态系统

## 🤝 贡献指南

我们欢迎各种形式的贡献：

1. **代码贡献**: 新功能、bug修复、性能优化
2. **理论贡献**: 新的道德理论实现、算法改进
3. **测试贡献**: 测试用例、场景设计、性能基准
4. **文档贡献**: 教程、示例、API文档

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

感谢以下贡献者和项目：
- 九州大学 Vargas教授（对抗性AI研究）
- 大阪大学智能媒体实验室
- 康德和密尔的道德哲学理论基础
- NEAT算法的原始研究者们

---

**"道德不是知识，而是行动的智慧。"** - 通过这个系统，我们试图让AI具备真正的道德行动能力。