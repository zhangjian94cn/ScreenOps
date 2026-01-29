import pytest
from ScreenOps.automation.context import AutomationContext
from ScreenOps.core.events import ScriptEvent
import os

def test_context_variables():
    """测试上下文变量读写"""
    ctx = AutomationContext()
    ctx.set("username", "antigravity")
    assert ctx.get("username") == "antigravity"
    assert ctx.get("nonexistent", "default") == "default"

def test_context_resolve_text():
    """测试占位符解析"""
    ctx = AutomationContext()
    ctx.set("user", "Admin")
    ctx.set("v", "1.0")
    
    resolved = ctx.resolve_text("Hello {{user}}, version is {{v}}")
    assert resolved == "Hello Admin, version is 1.0"

def test_context_env_var():
    """测试环境变量在上下文中的解析"""
    os.environ["TEST_VAR"] = "test_value"
    ctx = AutomationContext()
    assert ctx.get("env:TEST_VAR") == "test_value"
    
    resolved = ctx.resolve_text("Env is {{env:TEST_VAR}}")
    assert resolved == "Env is test_value"

def test_event_position_parsing():
    """测试坐标解析逻辑"""
    # 模拟屏幕大小 1920x1080
    from ScreenOps.core import events
    events.SW, events.SH = 1920, 1080
    
    event = ScriptEvent(delay=0, event_type='EM', action_type='click', action=[0, 0])
    
    # 百分比字符串
    assert event._parse_position(["50%", "50%"]) == (960, 540)
    # 浮点数百分比
    assert event._parse_position([0.1, 0.2]) == (192, 216)
    # 绝对坐标
    assert event._parse_position([100, 200]) == (100, 200)
    # 保持原位
    assert event._parse_position([-1, -1]) == (-1, -1)

def test_context_hint_matching():
    """测试输入框提示匹配"""
    ctx = AutomationContext()
    ctx.set("username", "user123")
    
    assert ctx.get_input_for_hint("Please enter your username") == "user123"
    assert ctx.get_input_for_hint("请输入您的用户名") == "user123"
    assert ctx.get_input_for_hint("密码") is None
