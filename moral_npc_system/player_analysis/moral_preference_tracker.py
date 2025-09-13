"""
道德偏好追踪器 - 追踪玩家的道德偏好变化
"""

from typing import Dict, List, Any
from collections import defaultdict


class MoralPreferenceTracker:
    """道德偏好追踪器"""
    
    def __init__(self):
        self.preference_history = defaultdict(list)
    
    def track_preference_changes(self, preferences: Dict[str, float]) -> Dict[str, Any]:
        """追踪偏好变化"""
        return {'preference_stability': 0.8, 'dominant_preference': 'kantian'}