import os
from typing import Dict, Any, Optional
from loguru import logger

class AutomationContext:
    """管理自动化流程中的上下文变量和凭据"""
    
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        # 预设的基础映射, 用于智能判断输入框
        self.hint_map = {
            '用户名': 'username',
            '账号': 'username',
            'username': 'username',
            'login': 'username',
            '密码': 'password',
            'password': 'password',
            '邮箱': 'email',
            'email': 'email',
            '验证码': 'captcha',
            'code': 'captcha'
        }
        
    def set(self, key: str, value: Any):
        """设置变量"""
        self.variables[key] = value
        logger.debug(f"Context set: {key} = {value}")
        
    def get(self, key: str, default: Any = None) -> Any:
        """获取变量"""
        # 支持特殊前缀 env:
        if isinstance(key, str) and key.startswith("env:"):
            env_key = key[4:]
            return os.getenv(env_key, default)
            
        return self.variables.get(key, default)
    
    def resolve_text(self, text: str) -> str:
        """解析带有占位符的文本, 例如 'Hello {{username}}'"""
        if not isinstance(text, str): return text
        
        import re
        def replace_match(match):
            key = match.group(1).strip()
            # 兼容 key=val 格式 或直接 key
            return str(self.get(key, match.group(0)))
            
        return re.sub(r"\{\{(.*?)\}\}", replace_match, text)

    def get_input_for_hint(self, hint: str) -> Optional[str]:
        """根据输入框提示文字判断该输入什么内容"""
        hint_lower = hint.lower()
        for key, var_name in self.hint_map.items():
            if key in hint_lower:
                val = self.get(var_name)
                if val: return val
        return None
