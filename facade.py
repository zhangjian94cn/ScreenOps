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

    def open(self, name: str, wait_time: float = 1.0):
        """
        智能打开/切换应用。
        支持别名映射，如果无法通过视觉找到，则通过 Spotlight 唤起。
        """
        logger.info(f"AI 指令: 唤起 '{name}'")
        self.launcher.find_and_click(name)
        time.sleep(wait_time)
        return self

    def click(self, target: str, timeout: float = 5.0, retry_interval: float = 0.5):
        """
        智能点击。在超时时间内不断尝试寻找目标（文字或图片库图标）。
        """
        logger.info(f"AI 指令: 寻找并点击 '{target}'")
        start_time = time.time()
        while time.time() - start_time < timeout:
            # 尝试 OCR
            if self.ocr.click_text(target):
                return self
            # 尝试图标匹配
            if self.launcher._try_icon_match([target]):
                return self
            time.sleep(retry_interval)
        
        logger.warning(f"由于超时，未能在屏幕上定位到: '{target}'")
        return self

    def wait_for(self, target: str, timeout: float = 20.0):
        """等待特定文字或图标出现在屏幕上"""
        logger.info(f"AI 指令: 等待 '{target}' 出现...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.ocr.recognizer.find_text(target):
                return self
            if self.launcher._try_icon_match([target]): # 这里内部会点击，我们需要个只匹配不点击的
                 # 暂时复用，未来可重构为纯查找
                 return self
            time.sleep(1)
        logger.error(f"等待超时: '{target}' 未出现")
        return self

    def click_at(self, x: int, y: int):
        """直接点击绝对坐标 (通常由录制生成，建议交给 AI 优化为智能点击)"""
        Mouse.click(x, y)
        return self

    def double_click_at(self, x: int, y: int):
        """双击绝对坐标"""
        Mouse.double_click(x, y)
        return self

    def type(self, text: str, enter: bool = False):
        """在当前焦点处键入内容"""
        logger.info(f"AI 指令: 输入 '{text}'")
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
