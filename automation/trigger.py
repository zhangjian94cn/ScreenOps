from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Tuple, Any
import re
from loguru import logger

class TriggerType(Enum):
    TEXT_APPEAR = "text_appear"      # 文字出现
    TEXT_DISAPPEAR = "text_disappear" # 文字消失
    IMAGE_APPEAR = "image_appear"    # 图标出现
    PIXEL_MATCH = "pixel_match"      # 像素点匹配

@dataclass
class Trigger:
    """自动化触发器条件"""
    type: TriggerType
    pattern: str  # 文字内容或图片路径
    region: Optional[Tuple[int, int, int, int]] = None  # 限制区域
    regex: bool = False
    
    def check(self, current_state: dict) -> bool:
        """
        检查触发器是否满足条件
        current_state: 包含 'texts' (List[TextMatch]) 和 'image_matches' 等信息的字典
        """
        if self.type == TriggerType.TEXT_APPEAR:
            texts = current_state.get('texts', [])
            for tm in texts:
                if self.regex:
                    if re.search(self.pattern, tm.text, re.IGNORE_CASE):
                        # 如果有区域限制, 检查是否在区域内
                        if self._is_in_region(tm.x, tm.y):
                            current_state['last_match'] = tm
                            return True
                else:
                    if self.pattern.lower() in tm.text.lower():
                        if self._is_in_region(tm.x, tm.y):
                            current_state['last_match'] = tm
                            return True
                            
        elif self.type == TriggerType.IMAGE_APPEAR:
            # 由 RuleEngine 调用 ImageMatcher 后传入状态
            match = current_state.get('image_match')
            if match:
                current_state['last_match'] = match
                return True
                
        return False

    def _is_in_region(self, x: int, y: int) -> bool:
        if not self.region: return True
        rx, ry, rw, rh = self.region
        return rx <= x <= rx + rw and ry <= y <= ry + rh
