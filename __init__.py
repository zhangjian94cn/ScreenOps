"""
ScreenOps - 为 AI 视觉指令优化的屏幕自动化引擎
"""
from .facade import ops, App
from .core.mouse import Mouse
from .core.keyboard import Keyboard
from .core.screen import Screen

__version__ = "0.1.0"
