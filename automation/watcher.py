import time
from loguru import logger
from .rules import RuleEngine
from .context import AutomationContext
import threading

class ScreenWatcher:
    """持续监控屏幕并根据规则自动执行动作"""
    
    def __init__(self, rule_file: str, interval: float = 2.0):
        self.context = AutomationContext()
        self.engine = RuleEngine(self.context)
        self.engine.load_rules(rule_file)
        self.interval = interval
        self.running = False
        self._thread = None
        
    def start(self):
        """启动监控线程"""
        if self.running: return
        self.running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        logger.info(f"屏幕监控已启动 (间隔 {self.interval}s)")
        
    def stop(self):
        """停止监控"""
        self.running = False
        logger.info("屏幕监控已停止")
        
    def _run(self):
        while self.running:
            try:
                # 执行一次评估
                self.engine.evaluate()
            except Exception as e:
                logger.error(f"自动化执行错误: {e}")
                
            time.sleep(self.interval)
            
    def run_once(self):
        """同步执行单次检测"""
        return self.engine.evaluate()
