import time
import pyautogui
from .recognizer import OCRRecognizer, TextMatch
from loguru import logger
from typing import Optional

class OCRClicker:
    """通过文字内容进行自动点击"""
    
    def __init__(self, lang: str = 'chi_sim+eng'):
        self.recognizer = OCRRecognizer(lang)
    
    def click_text(self, text: str, regex: bool = False, double: bool = False) -> bool:
        """识别并点击指定文字"""
        logger.info(f"正在查找并点击文字: '{text}'")
        match = self.recognizer.find_text(text, regex)
        
        if match:
            x, y = match.center
            logger.success(f"找到文字 '{match.text}' 于 ({x}, {y}), 正在执行点击")
            if double:
                pyautogui.doubleClick(x, y)
            else:
                pyautogui.click(x, y)
            return True
        else:
            logger.warning(f"未能找到文字: '{text}'")
            return False
            
    def wait_and_click(self, text: str, timeout: float = 10, interval: float = 0.5, regex: bool = False) -> bool:
        """等待文字出现并点击"""
        logger.info(f"等待文字出现: '{text}' (超时 {timeout}s)")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.click_text(text, regex):
                return True
            time.sleep(interval)
            
        logger.error(f"等待文字 '{text}' 超时")
        return False
        
    def find(self, text: str, regex: bool = False) -> Optional[TextMatch]:
        """仅查找文字位置, 不点击"""
        return self.recognizer.find_text(text, regex)
