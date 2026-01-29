import time
import pyautogui
from loguru import logger
import threading
from typing import Optional

class AutoClicker:
    """自动点击器逻辑"""
    
    def __init__(self, interval: float = 0.5):
        self.interval = interval
        self.running = False
        self.paused = False
        self._thread = None
        
    def toggle(self):
        """切换 运行/暂停"""
        if not self.running:
            self.start()
        else:
            self.paused = not self.paused
            status = "暂停" if self.paused else "恢复"
            logger.info(f"点击器已{status}")
            
    def start(self, count: int = 0):
        """开始点击, count=0 表示无限循环"""
        if self.running:
            self.paused = False
            return
            
        self.running = True
        self.paused = False
        logger.info("点击器开始运行")
        
        self._thread = threading.Thread(target=self._loop, args=(count,), daemon=True)
        self._thread.start()
        
    def stop(self):
        """停止点击器"""
        self.running = False
        self.paused = False
        logger.info("点击器已停止")
        
    def _loop(self, count: int):
        i = 0
        while self.running:
            if not self.paused:
                try:
                    pyautogui.click()
                    i += 1
                    if count > 0 and i >= count:
                        logger.info(f"已达到点击次数限制: {count}")
                        break
                except Exception as e:
                    logger.error(f"点击失败: {e}")
                    break
            time.sleep(self.interval)
        self.running = False
