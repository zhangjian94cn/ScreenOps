import pyautogui
from PIL import Image
from typing import Tuple, Optional
from loguru import logger

class Screen:
    """封装屏幕基本操作"""
    
    @staticmethod
    def size() -> Tuple[int, int]:
        """获取屏幕分辨率"""
        return pyautogui.size()
    
    @staticmethod
    def screenshot(region: Optional[Tuple[int, int, int, int]] = None) -> Image.Image:
        """截取屏幕内容"""
        try:
            return pyautogui.screenshot(region=region)
        except Exception as e:
            logger.error(f"屏幕截图失败: {e}")
            raise
            
    @staticmethod
    def save_screenshot(path: str, region: Optional[Tuple[int, int, int, int]] = None):
        """保存屏幕截图到文件"""
        try:
            pyautogui.screenshot(path, region=region)
            logger.info(f"截图已保存至: {path}")
        except Exception as e:
            logger.error(f"截图保存失败: {e}")
            
    @staticmethod
    def locate_on_screen(image_path: str, confidence: float = 0.9) -> Optional[Tuple[int, int, int, int]]:
        """在屏幕上查找图像, 返回 (left, top, width, height)"""
        try:
            # 需要安装 opencv-python
            return pyautogui.locateOnScreen(image_path, confidence=confidence)
        except Exception as e:
            logger.error(f"图像识别失败: {e}")
            return None

    @staticmethod
    def locate_center_on_screen(image_path: str, confidence: float = 0.9) -> Optional[Tuple[int, int]]:
        """在屏幕上查找图像并返回中心位置 (x, y)"""
        try:
            return pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        except Exception as e:
            logger.error(f"图像识别中心点失败: {e}")
            return None
