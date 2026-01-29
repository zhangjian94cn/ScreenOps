import pyautogui
from typing import List, Union
from loguru import logger

class Keyboard:
    """封装键盘基本操作"""
    
    @staticmethod
    def type(text: str, interval: float = 0.05):
        """输入文本"""
        try:
            pyautogui.write(text, interval=interval)
        except Exception as e:
            logger.error(f"文本输入失败: {e}")
            
    @staticmethod
    def press(keys: Union[str, List[str]]):
        """按下并释放按键(或组合键)"""
        try:
            if isinstance(keys, list):
                pyautogui.hotkey(*keys)
            else:
                pyautogui.press(keys)
        except Exception as e:
            logger.error(f"按键失败: {e}")
            
    @staticmethod
    def down(key: str):
        """按下按键不放"""
        pyautogui.keyDown(key)
        
    @staticmethod
    def up(key: str):
        """抬起按键"""
        pyautogui.keyUp(key)

    @staticmethod
    def hotkey(*args):
        """执行组合键"""
        pyautogui.hotkey(*args)
