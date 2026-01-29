import yaml
from typing import List, Optional, Any
from .trigger import Trigger, TriggerType
from .context import AutomationContext
from ..ocr.recognizer import OCRRecognizer
from ..image.matcher import ImageMatcher
from ..core.mouse import Mouse
from ..core.keyboard import Keyboard
from loguru import logger

class Rule:
    """联动触发器与动作的规则"""
    def __init__(self, data: dict):
        self.name = data.get('name', 'Unnamed Rule')
        trigger_data = data.get('trigger', {})
        self.trigger = Trigger(
            type=TriggerType(trigger_data['type']),
            pattern=trigger_data['pattern'],
            regex=trigger_data.get('regex', False),
            region=trigger_data.get('region')
        )
        self.action_type = data.get('action')
        self.params = data.get('params', {})

class RuleEngine:
    """自动化规则引擎"""
    def __init__(self, context: AutomationContext):
        self.context = context
        self.rules: List[Rule] = []
        self.ocr = OCRRecognizer()
        self.img_matcher = ImageMatcher()
        
    def load_rules(self, yaml_path: str):
        """导入 YAML 定义的规则"""
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            # 加载上下文
            if 'context' in data:
                for k, v in data['context'].items():
                    self.context.set(k, v)
                    
            # 加载规则
            for r_data in data.get('rules', []):
                self.rules.append(Rule(r_data))
                
            logger.info(f"成功加载文件 {yaml_path}: 共 {len(self.rules)} 条规则")
        except Exception as e:
            logger.error(f"加载规则失败: {e}")

    def evaluate(self) -> bool:
        """
        执行一次扫描并评估规则。
        返回 True 如果执行了任何动作。
        """
        # 1. 扫描屏幕获取当前状态
        state = {
            'texts': self.ocr.recognize(),
            'last_match': None
        }
        
        # 2. 遍历规则
        for rule in self.rules:
            # 如果是图像触发, 单独处理
            if rule.trigger.type == TriggerType.IMAGE_APPEAR:
                match = self.img_matcher.match(rule.trigger.pattern)
                state['image_match'] = match
                
            if rule.trigger.check(state):
                logger.info(f"规则触发: '{rule.name}'")
                self.execute_action(rule, state['last_match'])
                return True
                
        return False

    def execute_action(self, rule: Rule, match: Any):
        """执行匹配到的动作"""
        at = rule.action_type
        params = rule.params
        
        if at == 'click':
            # 点击触发它的物体
            if match and hasattr(match, 'center'):
                x, y = match.center
                Mouse.click(x, y)
            elif isinstance(match, (list, tuple)):
                # 图像识别返回的是 (x, y, w, h)
                x = match[0] + match[2]//2
                y = match[1] + match[3]//2
                Mouse.click(x, y)
                
        elif at == 'type':
            text = self.context.resolve_text(params.get('text', ''))
            Keyboard.type(text)
            
        elif at == 'hotkey':
            keys = params.get('keys', [])
            Keyboard.hotkey(*keys)
            
        elif at == 'wait':
            seconds = params.get('seconds', 1)
            import time
            time.sleep(seconds)
            
        logger.success(f"完成动作: {at}")
