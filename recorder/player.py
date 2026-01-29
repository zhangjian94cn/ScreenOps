import json5
import time
from ..core.events import ScriptEvent
from loguru import logger
import threading

class Player:
    """脚本回放器"""
    
    def __init__(self):
        self.running = False
        self.paused = False
        self._thread = None
        
    def play(self, script_path: str, times: int = 1):
        """回放脚本, times=0 表示无限循环"""
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                data = json5.load(f)
            
            script_events = []
            for item in data.get('scripts', []):
                if item.get('type') == 'event':
                    script_events.append(ScriptEvent(
                        delay=item['delay'],
                        event_type=item['event_type'],
                        action_type=item['action_type'],
                        action=item['action']
                    ))
            
            if not script_events:
                logger.warning("脚本中没有可执行事件")
                return
                
            self.running = True
            self.paused = False
            
            self._thread = threading.Thread(
                target=self._loop, 
                args=(script_events, times), 
                daemon=True
            )
            self._thread.start()
            
        except Exception as e:
            logger.error(f"播放脚本失败: {e}")

    def stop(self):
        """停止播放"""
        self.running = False
        logger.info("脚本播放已停止")

    def toggle_pause(self):
        """切换暂停/恢复"""
        self.paused = not self.paused
        logger.info(f"播放已{'暂停' if self.paused else '恢复'}")

    def _loop(self, events: list, times: int):
        iteration = 0
        while self.running and (times == 0 or iteration < times):
            iteration += 1
            logger.info(f"正在执行第 {iteration} 轮播放...")
            
            for event in events:
                if not self.running:
                    break
                
                # 处理暂停
                while self.paused and self.running:
                    time.sleep(0.1)
                
                try:
                    event.execute()
                except Exception as e:
                    logger.error(f"执行事件失败: {e}")
                    
            if times != 0 and iteration >= times:
                break
                
        self.running = False
        logger.success("脚本回放完成")
