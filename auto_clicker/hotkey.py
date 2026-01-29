from pynput import keyboard
from loguru import logger
import sys
from typing import Callable, Optional

class HotkeyListener:
    """全局热键监听器 (F6/F9/Esc)"""
    
    def __init__(self, 
                 on_toggle: Optional[Callable] = None, 
                 on_stop: Optional[Callable] = None):
        """
        on_toggle: 按下 F6 时触发 (开始/暂停)
        on_stop: 按下 F9 时触发 (彻底停止)
        """
        self.on_toggle = on_toggle
        self.on_stop = on_stop
        self.listener = None
        
    def _on_press(self, key):
        try:
            # F6: 切换
            if key == keyboard.Key.f6:
                logger.info("检测到热键: F6 (切换)")
                if self.on_toggle:
                    self.on_toggle()
            
            # F9: 停止
            elif key == keyboard.Key.f9:
                logger.info("检测到热键: F9 (停止)")
                if self.on_stop:
                    self.on_stop()
            
            # Esc: 紧急停止脚本运行
            elif key == keyboard.Key.esc:
                logger.warning("检测到热键: Esc (紧急停止)")
                sys.exit(1)
                
        except Exception as e:
            logger.error(f"热键处理错误: {e}")

    def start(self):
        """在后台启动监听器"""
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()
        logger.info("热键监听器已启动 (F6: 切换, F9: 停止, Esc: 退出)")
        
    def stop(self):
        """停止监听器"""
        if self.listener:
            self.listener.stop()
