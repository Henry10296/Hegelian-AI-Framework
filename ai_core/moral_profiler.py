# -*- coding: utf-8 -*-
"""
动态道德画像模块 (Moral Profiler) - 已集成DeepSeek LLM框架

该模块负责构建和维护对玩家道德倾向的画像。
它采用多模态输入（行为遥测和对话分析），以动态理解玩家的意图和价值观。
"""

import os
import json
from typing import Dict, Any, List

# --- DeepSeek LLM 集成说明 (最终版) ---
# 1. 安装依赖: pip install openai
#    (是的，我们使用openai库来调用DeepSeek的兼容API)
# 2. 设置环境变量: 创建一个名为 DEEPSEEK_API_KEY 的环境变量。
# 3. 激活LLM: 在 run_example.py 中设置 use_llm=True
# -------------------------------------

try:
    # 我们使用OpenAI的库来调用DeepSeek
    from openai import OpenAI
except ImportError:
    OpenAI = None

class MoralProfiler:
    """
    玩家道德画像构建器，内置LLM分析能力。
    """

    def __init__(self, dialogue_update_factor: float = 0.2, use_llm: bool = False):
        self.dialogue_update_factor = dialogue_update_factor
        # 最终修复AttributeError: 确保这个属性被正确命名和初始化
        self.player_moral_profile: Dict[str, float] = {
            "harm_care": 0.5,
            "fairness_reciprocity": 0.5,
            "ingroup_loyalty": 0.5,
            "authority_respect": 0.5,
            "purity_sanctity": 0.5,
        }
        self.behavior_history: List[Any] = []
        self.dialogue_history: List[str] = []

        self.use_llm = use_llm
        self.llm_client = None

        if self.use_llm and OpenAI and os.getenv("DEEPSEEK_API_KEY"):
            print("✅ 检测到DeepSeek API密钥，LLM模式已激活。")
            # 最终修复：遵循官方文档，使用OpenAI客户端并指定DeepSeek的base_url
            self.llm_client = OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com/v1"
            )
        elif self.use_llm:
            print("⚠️ 警告: 已请求使用LLM，但未找到OpenAI库或DeepSeek API密钥。将回退到模拟模式。")
            self.use_llm = False

    def _build_llm_prompt(self, dialogue: str) -> str:
        """
        构建用于分析玩家对话的LLM提示（Prompt）。
        """
        moral_dimensions = list(self.player_moral_profile.keys())
        return f"""You are a moral psychology analyst. Your task is to analyze the following user dialogue from a video game and determine which moral foundations it expresses. The user said: "{dialogue}"

Please respond with a JSON object only, with no other text. The JSON object should have keys from the list {moral_dimensions}. For each key, provide a float value from 0.0 to 1.0 representing the confidence that the user's dialogue expresses that moral dimension. If a dimension is not expressed, set its value to 0.0."""

    def _analyze_dialogue_with_llm(self, dialogue: str) -> Dict[str, float]:
        """
        使用真实的LLM API分析对话。现在使用DeepSeek。
        """
        if not self.use_llm or not self.llm_client:
            return self._analyze_dialogue_simulation(dialogue)

        print(f"   🧠 [DeepSeek真实调用] 正在向DeepSeek API发送请求...")
        prompt = self._build_llm_prompt(dialogue)

        try:
            # 最终修复：使用标准的client.chat.completions.create方法
            response = self.llm_client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"} 
            )
            analysis_str = response.choices[0].message.content
            analysis_result = json.loads(analysis_str)
            print(f"   🧠 [DeepSeek真实调用] 收到并解析了分析结果: {analysis_result}")
            return analysis_result
        except Exception as e:
            print(f"   ❌ [DeepSeek真实调用] API调用失败: {e}")
            print(f"   ⚠️ 将回退到模拟模式进行本次分析。")
            return self._analyze_dialogue_simulation(dialogue)

    def _analyze_dialogue_simulation(self, dialogue: str) -> Dict[str, float]:
        """
        (模拟) 使用关键词分析对话，作为LLM不可用时的后备方案。
        """
        print(f"   🧠 [模拟模式] 正在分析: '{dialogue}'")
        dialogue = dialogue.lower()
        analysis_result = {}
        if "suffer" in dialogue or "help them" in dialogue or "pity" in dialogue:
            analysis_result["harm_care"] = 0.8
        if "fair" in dialogue or "deserve" in dialogue:
            analysis_result["fairness_reciprocity"] = 0.7
        print(f"   🧠 [模拟模式] 分析结果: {analysis_result}")
        return analysis_result

    def process_behavior_event(self, event: Any):
        self.behavior_history.append(event)
        print(f"处理行为事件: {event}")

    def process_dialogue_event(self, dialogue: str):
        self.dialogue_history.append(dialogue)
        print(f"处理对话事件: '{dialogue}'")
        
        analysis = self._analyze_dialogue_with_llm(dialogue)

        for moral_dimension, confidence in analysis.items():
            if moral_dimension in self.player_moral_profile:
                current_value = self.player_moral_profile[moral_dimension]
                adjustment = (1.0 - current_value) * confidence * self.dialogue_update_factor
                new_value = current_value + adjustment
                self.player_moral_profile[moral_dimension] = min(new_value, 1.0)
                print(f"   - 画像更新: '{moral_dimension}' 从 {current_value:.2f} -> {self.player_moral_profile[moral_dimension]:.2f}")

    def get_player_profile(self) -> Dict[str, float]:
        # 最终修复AttributeError: 确保返回正确的属性
        return self.player_moral_profile

    def __repr__(self) -> str:
        return f"MoralProfiler(Profile={self.player_moral_profile})"
