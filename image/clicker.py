import pyautogui
from .matcher import ImageMatcher
from loguru import logger
from typing import Optional, Tuple
import time

class ImageClicker:
    """通过图片识别进行点击"""
    
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold
        self.matcher = ImageMatcher()
        
    def click_image(self, template_path: str, offset: Tuple[int, int] = (0, 0), double: bool = False) -> bool:
        """识别图片并点击(可设置偏移)"""
        logger.info(f"正在找图并点击: {template_path}")
        res = self.matcher.match(template_path, threshold=self.threshold)
        
        if res:
            left, top, width, height = res
            # 点击中心位置 + 偏移
            x = left + width // 2 + offset[0]
            y = top + height // 2 + offset[1]
            
            logger.success(f"找到图片 '{template_path}' 于 ({x}, {y}), 正在执行点击")
            if double:
                pyautogui.doubleClick(x, y)
            else:
                pyautogui.click(x, y)
            return True
        else:
            logger.warning(f"未能找到图片: {template_path}")
            return False
            
    def wait_and_click(self, template_path: str, timeout: float = 10, interval: float = 0.5) -> bool:
        """等待图片出现并点击"""
        logger.info(f"等待图片出现: {template_path} (超时 {timeout}s)")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.click_image(template_path):
                return True
            time.sleep(interval)
            
        logger.error(f"等待图片 '{template_path}' 超时")
        return False
