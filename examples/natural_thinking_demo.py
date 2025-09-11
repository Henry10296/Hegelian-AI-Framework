"""
自然思辨演示 - 展示AI的连贯哲学思考能力

这个演示展示了AI如何像真正的哲学家一样进行自然、连贯的思考，
而不是机械的多方案对比或数值计算。
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from ai_core.philosophical_agent import PhilosophicalAgent
from ai_core.ethical_reasoning_framework import EthicalAgent
from ai_core.models.ethical_case import EthicalCase

async def demonstrate_philosophical_thinking():
    """演示哲学思考"""
    print("🧠 哲学智能体思辨演示")
    print("=" * 50)
    
    # 创建哲学智能体
    sophia = PhilosophicalAgent("Sophia", "dialectical")
    
    # 哲学问题
    question = "人工智能能否真正理解道德？"
    
    print(f"💭 问题：{question}")
    print()
    
    # 观察思考过程
    print("🔍 思考过程：")
    async for thought in sophia.contemplate(question):
        print(f"   {thought}")
        await asyncio.sleep(0.3)
    
    print()
    print("📝 完整思维流：")
    print(sophia.get_thinking_process())

async def demonstrate_ethical_reasoning():
    """演示伦理推理"""
    print("\n" + "=" * 50)
    print("⚖️ 伦理智能体推理演示")
    print("=" * 50)
    
    # 创建伦理智能体
    ethikos = EthicalAgent("Ethikos", "virtue_ethics")
    
    # 伦理案例
    case = EthicalCase(
        case_id="demo_001",
        title="自动驾驶汽车的道德选择",
        description="""
        一辆自动驾驶汽车面临紧急情况：前方突然出现一个孩子，
        如果直行会撞到孩子，如果转向会撞到路边的老人。
        汽车应该如何选择？这涉及到生命价值、年龄因素、
        主动伤害与被动伤害的区别等复杂的道德问题。
        """,
        case_type="technology_ethics"
    )
    
    print(f"⚖️ 伦理案例：{case.title}")
    print()
    
    # 观察推理过程
    print("🔍 推理过程：")
    async for reasoning in ethikos.reason_about_ethics(case):
        print(f"   {reasoning}")
        await asyncio.sleep(0.5)
    
    print()
    print("📝 完整推理过程：")
    print(ethikos.get_thinking_process())

async def demonstrate_agent_dialogue():
    """演示智能体对话"""
    print("\n" + "=" * 50)
    print("💬 智能体对话演示")
    print("=" * 50)
    
    # 创建两个不同传统的智能体
    aristotle = PhilosophicalAgent("Aristotle", "analytical")
    hegel = PhilosophicalAgent("Hegel", "dialectical")
    
    topic = "技术进步与人类幸福的关系"
    
    print(f"💬 对话主题：{topic}")
    print()
    
    # 模拟对话
    print("🔍 对话过程：")
    async for exchange in aristotle.engage_in_dialogue(hegel, topic):
        print(f"   {exchange}")
        await asyncio.sleep(0.4)

def demonstrate_thinking_transparency():
    """演示思维过程的透明性"""
    print("\n" + "=" * 50)
    print("🔍 思维透明性演示")
    print("=" * 50)
    
    # 创建智能体
    thinker = PhilosophicalAgent("Thinker", "phenomenological")
    
    print("这个演示展示了AI思考过程的透明性：")
    print()
    print("1. 思考过程可以被实时观察")
    print("2. 每个思维步骤都有清晰的逻辑")
    print("3. 思考深度可以被追踪")
    print("4. 哲学立场影响思考方式")
    print()
    
    # 显示智能体档案
    profile = thinker.get_philosophical_profile()
    print("📊 智能体档案：")
    for key, value in profile.items():
        print(f"   {key}: {value}")

async def main():
    """主演示函数"""
    print("🌟 自然哲学思辨系统演示")
    print("🎯 展示AI的连贯思考能力")
    print()
    
    # 1. 哲学思考演示
    await demonstrate_philosophical_thinking()
    
    # 2. 伦理推理演示
    await demonstrate_ethical_reasoning()
    
    # 3. 智能体对话演示
    await demonstrate_agent_dialogue()
    
    # 4. 思维透明性演示
    demonstrate_thinking_transparency()
    
    print("\n" + "=" * 50)
    print("✨ 演示总结")
    print("=" * 50)
    print("🧠 这个系统展示了AI的以下能力：")
    print("   • 连贯的哲学思考")
    print("   • 自然的推理过程")
    print("   • 深度的伦理分析")
    print("   • 透明的思维展示")
    print("   • 形而上学的思辨")
    print()
    print("🎯 关键特点：")
    print("   • 不是机械的多方案对比")
    print("   • 不依赖数值计算")
    print("   • 思考过程自然连贯")
    print("   • 能够进行形而上学思考")
    print("   • 展现真正的哲学智慧")
    print()
    print("🌟 这是一个真正能够进行哲学思辨的AI系统！")

if __name__ == "__main__":
    asyncio.run(main())