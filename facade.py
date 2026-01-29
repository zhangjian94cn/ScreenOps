from .core.mouse import Mouse
from .core.keyboard import Keyboard
from .core.screen import Screen
from .core.launcher import SmartLauncher
from .ocr.clicker import OCRClicker
from .image.clicker import ImageClicker
import time
from loguru import logger

class App:
    """
    ScreenOps 极简 API 门面 (Facade)，专为 AI 生成脚本设计。
    让 AI 能够用最自然的语言描述操作。
    """
    
    def __init__(self):
        self.launcher = SmartLauncher()
        self.ocr = OCRClicker()
        self.img = ImageClicker()

    def open(self, name: str):
        """打开/跳转至某个应用或点击包含该名字的地方"""
        logger.info(f"AI 指令: 打开 {name}")
        self.launcher.find_and_click(name)
        return self

    def click(self, target: str):
        """点击屏幕上的文字或图标名称"""
        logger.info(f"AI 指令: 点击 {target}")
        # 尝试 OCR 并尝试图片目录
        if not self.ocr.click_text(target):
             self.launcher._try_icon_match([target])
        return self

    def type(self, text: str, enter: bool = False):
        """键入内容"""
        logger.info(f"AI 指令: 输入内容")
        Keyboard.type(text + ('\n' if enter else ''))
        return self

    def wait(self, seconds: float):
        """等待"""
        time.sleep(seconds)
        return self

    def screenshot(self, filename: str):
        """截图保存"""
        Screen.save_screenshot(filename)
        return self

    def hotkey(self, *keys: str):
        """按下快捷键"""
        Keyboard.hotkey(*keys)
        return self

# 导出全局单例
ops = App()
