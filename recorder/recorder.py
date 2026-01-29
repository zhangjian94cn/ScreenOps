from pynput import mouse, keyboard
import time
import json5
from ..core.events import ScriptEvent
from loguru import logger
from typing import List, Optional

class Recorder:
    """操作录制器, 兼容 KeymouseGo 脚本格式"""
    
    def __init__(self):
        self.events = []
        self.last_time = 0
        self.mouse_listener = None
        self.key_listener = None
        self.running = False
        
    def _current_time_ms(self) -> int:
        return int(time.time() * 1000)
    
    def _get_delay(self) -> int:
        now = self._current_time_ms()
        if self.last_time == 0:
            delay = 0
        else:
            delay = now - self.last_time
        self.last_time = now
        return delay

    def _on_click(self, x, y, button, pressed):
        if not self.running: return
        
        button_name = button.name
        action_type = f"mouse {button_name} {'down' if pressed else 'up'}"
        
        # 记录百分比坐标以实现屏幕适配
        import pyautogui
        sw, sh = pyautogui.size()
        tx = f"{x / sw:.5%}"
        ty = f"{y / sh:.5%}"
        
        self.events.append({
            'type': 'event',
            'event_type': 'EM',
            'delay': self._get_delay(),
            'action_type': action_type,
            'action': [tx, ty]
        })

    def _on_press(self, key):
        if not self.running: return
        
        try:
            # 尝试获取字符或键名
            key_name = key.char if hasattr(key, 'char') else key.name
            key_vk = key.vk if hasattr(key, 'vk') else 0
        except AttributeError:
            key_name = str(key)
            key_vk = 0
            
        if key_name is None: return

        self.events.append({
            'type': 'event',
            'event_type': 'EK',
            'delay': self._get_delay(),
            'action_type': 'key down',
            'action': [key_vk, key_name, 0]
        })

    def _on_release(self, key):
        if not self.running: return
        
        # 停止录制的快捷键通常在外部主循环处理, 
        # 这里只负责记录
        try:
            key_name = key.char if hasattr(key, 'char') else key.name
            key_vk = key.vk if hasattr(key, 'vk') else 0
        except AttributeError:
            key_name = str(key)
            key_vk = 0
            
        if key_name is None: return

        self.events.append({
            'type': 'event',
            'event_type': 'EK',
            'delay': self._get_delay(),
            'action_type': 'key up',
            'action': [key_vk, key_name, 0]
        })

    def start(self):
        """开始录制"""
        self.events = []
        self.last_time = self._current_time_ms()
        self.running = True
        
        self.mouse_listener = mouse.Listener(on_click=self._on_click)
        self.key_listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        
        self.mouse_listener.start()
        self.key_listener.start()
        logger.info("录制已开始... 按下停止键(或通过CLI停止)结束录制")

    def stop(self) -> List[dict]:
        """停止录制并返回事件列表"""
        self.running = False
        if self.mouse_listener: self.mouse_listener.stop()
        if self.key_listener: self.key_listener.stop()
        logger.info(f"录制结束, 共捕获 {len(self.events)} 个事件")
        return self.events

    def save(self, path: str):
        """保存为 JSON5 格式文件"""
        output = {"scripts": self.events}
        with open(path, 'w', encoding='utf-8') as f:
            # 简单起见直接用 json, json5 库通常用于读取
            import json
            json.dump(output, f, indent=2, ensure_ascii=False)
        logger.success(f"脚本已保存至: {path}")
