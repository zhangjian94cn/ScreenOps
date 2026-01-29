import time
import pyautogui
from dataclasses import dataclass
from typing import Union, Tuple, List, Optional
from loguru import logger
import re

SW, SH = pyautogui.size()

@dataclass
class ScriptEvent:
    """脚本事件模型, 兼容 KeymouseGo"""
    delay: int  # 延迟(毫秒)
    event_type: str  # EM(鼠标), EK(键盘), EX(扩展)
    action_type: str 
    action: Union[Tuple, List, str]
    message: Optional[str] = None

    def execute(self):
        """执行该事件"""
        if self.delay > 0:
            time.sleep(self.delay / 1000.0)
            
        if self.event_type == 'EM':
            self._execute_mouse()
        elif self.event_type == 'EK':
            self._execute_keyboard()
        elif self.event_type == 'EX':
            self._execute_extra()
            
    def _parse_position(self, pos) -> Tuple[int, int]:
        """解析坐标, 支持绝对坐标、相对坐标和 [-1, -1]"""
        if not isinstance(pos, (list, tuple)) or len(pos) != 2:
            return -1, -1
            
        x, y = pos
        
        # 处理 [-1, -1]
        if x == -1 and y == -1:
            return -1, -1
            
        # 处理百分比字符串 (兼容 KeymouseGo)
        if isinstance(x, str) and x.endswith('%'):
            x = float(x.rstrip('%')) / 100.0
        if isinstance(y, str) and y.endswith('%'):
            y = float(y.rstrip('%')) / 100.0
            
        # 处理浮点数(百分比)
        if isinstance(x, float):
            x = int(x * SW)
        if isinstance(y, float):
            y = int(y * SH)
            
        return x, y

    def _execute_mouse(self):
        x, y = self._parse_position(self.action)
        
        # 移动鼠标 (如果坐标不是 [-1, -1])
        if x != -1 and y != -1:
            pyautogui.moveTo(x, y)
            
        # 执行动作
        at = self.action_type.lower()
        if 'left down' in at:
            pyautogui.mouseDown(button='left')
        elif 'left up' in at:
            pyautogui.mouseUp(button='left')
        elif 'right down' in at:
            pyautogui.mouseDown(button='right')
        elif 'right up' in at:
            pyautogui.mouseUp(button='right')
        elif 'middle down' in at:
            pyautogui.mouseDown(button='middle')
        elif 'middle up' in at:
            pyautogui.mouseUp(button='middle')
        elif 'wheel up' in at:
            pyautogui.scroll(1)
        elif 'wheel down' in at:
            pyautogui.scroll(-1)
        elif 'move' in at:
            pass # 已经 moveTo 了

    def _execute_keyboard(self):
        # EK action: [keycode, keyname, extended] 
        # KeymouseGo 格式: [70, 'f', 0]
        _, key_name, _ = self.action
        
        at = self.action_type.lower()
        if 'key down' in at:
            pyautogui.keyDown(key_name)
        elif 'key up' in at:
            pyautogui.keyUp(key_name)

    def _execute_extra(self):
        # EX action: string 
        if self.action_type.lower() == 'input':
            pyautogui.write(self.action)
