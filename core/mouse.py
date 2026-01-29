import pyautogui
from typing import Tuple, Optional
from loguru import logger

class Mouse:
    """封装鼠标基本操作"""
    
    @staticmethod
    def position() -> Tuple[int, int]:
        """获取当前鼠标位置"""
        return pyautogui.position()
    
    @staticmethod
    def move_to(x: int, y: int, duration: float = 0.1):
        """移动鼠标到指定位置"""
        try:
            pyautogui.moveTo(x, y, duration=duration)
        except Exception as e:
            logger.error(f"鼠标移动失败: {e}")
            
    @staticmethod
    def click(x: Optional[int] = None, y: Optional[int] = None, button: str = 'left'):
        """在指定位置点击鼠标"""
        try:
            pyautogui.click(x=x, y=y, button=button)
        except Exception as e:
            logger.error(f"鼠标点击失败: {e}")
            
    @staticmethod
    def double_click(x: Optional[int] = None, y: Optional[int] = None, button: str = 'left'):
        """双击鼠标"""
        try:
            pyautogui.doubleClick(x=x, y=y, button=button)
        except Exception as e:
            logger.error(f"鼠标双击失败: {e}")
            
    @staticmethod
    def drag_to(x: int, y: int, duration: float = 0.5, button: str = 'left'):
        """拖拽鼠标到指定位置"""
        try:
            pyautogui.dragTo(x, y, duration=duration, button=button)
        except Exception as e:
            logger.error(f"鼠标拖拽失败: {e}")
            
    @staticmethod
    def scroll(clicks: int):
        """滚动鼠标, 正数向上, 负数向下"""
        try:
            pyautogui.scroll(clicks)
        except Exception as e:
            logger.error(f"鼠标滚动失败: {e}")

    @staticmethod
    def down(button: str = 'left'):
        """按下鼠标按键"""
        pyautogui.mouseDown(button=button)

    @staticmethod
    def up(button: str = 'left'):
        """抬起鼠标按键"""
        pyautogui.mouseUp(button=button)
