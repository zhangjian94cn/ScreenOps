import time
import os
import difflib
from loguru import logger
from typing import Optional, List, Tuple
from ..ocr.recognizer import OCRRecognizer, TextMatch
from ..image.matcher import ImageMatcher
from ..core.mouse import Mouse
from ..core.keyboard import Keyboard
import pyautogui

class SmartLauncher:
    """智能启动器：整合 OCR、图像识别和系统搜索"""
    
    def __init__(self, icon_dir: str = "ScreenOps/resources/icons"):
        self.ocr = OCRRecognizer()
        self.img_matcher = ImageMatcher()
        self.icon_dir = icon_dir
        # 常见应用的同义词映射
        self.alias_map = {
            "微信": ["微信", "WeChat", "We Chat"],
            "浏览器": ["Chrome", "Safari", "Edge", "Browser", "浏览器"],
            "终端": ["Terminal", "ITerm", "终端", "zsh", "bash"],
            "飞书": ["飞书", "Lark"],
            "钉钉": ["钉钉", "DingTalk"]
        }
        
    def find_and_click(self, description: str) -> bool:
        """
        全能寻找并点击策略：
        1. 尝试在资源目录中查找是否有匹配描述文字的图标图片
        2. 扫描屏幕进行 OCR 模糊匹配
        3. 如果均失败，通过 Spotlight 唤起
        """
        logger.info(f"开启智能定位流程: '{description}'")
        
        # 获取所有可能的名称
        candidates = self.alias_map.get(description, [description])
        if description not in candidates:
            candidates.append(description)

        # 策略 A: 图标匹配 (最优，如果用户提供了样本)
        if self._try_icon_match(candidates):
            return True

        # 策略 B: OCR 屏幕识别
        logger.info(f"正在扫描屏幕寻找文字 {candidates}...")
        all_texts = self.ocr.recognize()
        best_match = self._find_best_text_match(candidates, all_texts)
        if best_match:
            logger.success(f"通过 OCR 发现最匹配文字 '{best_match.text}'，正在点击...")
            Mouse.click(*best_match.center)
            return True
            
        # 策略 C: 系统搜索唤起 (Spotlight)
        logger.info(f"屏幕未发现文字或图标，尝试通过系统搜索唤起 '{description}'...")
        return self._open_via_spotlight(description)

    def _try_icon_match(self, candidates: List[str]) -> bool:
        """从图标库中寻找匹配的图标并尝试在屏幕定位"""
        if not os.path.exists(self.icon_dir):
            return False
            
        # 获取图标目录下所有文件
        icon_files = os.listdir(self.icon_dir)
        for cand in candidates:
            # 查找文件名包含候选词的图片 (忽略大小写)
            for f in icon_files:
                if cand.lower() in f.lower() and f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    icon_path = os.path.join(self.icon_dir, f)
                    logger.info(f"发现候选图标文件: {icon_path}, 正在尝试匹配...")
                    
                    match = self.img_matcher.match(icon_path, threshold=0.8)
                    if match:
                        x = match[0] + match[2]//2
                        y = match[1] + match[3]//2
                        logger.success(f"在屏幕上匹配到图标 '{f}'，正在点击...")
                        Mouse.click(x, y)
                        return True
        return False

    def _find_best_text_match(self, candidates: List[str], text_matches: List[TextMatch], threshold: float = 0.6) -> Optional[TextMatch]:
        """模糊匹配识别到的文字"""
        best_tm = None
        highest_score = 0.0
        for tm in text_matches:
            for cand in candidates:
                score = difflib.SequenceMatcher(None, cand.lower(), tm.text.lower()).ratio()
                if score > highest_score:
                    highest_score = score
                    best_tm = tm
        if highest_score >= threshold:
            logger.debug(f"文字模糊匹配得分: {highest_score:.2f} ('{best_tm.text}')")
            return best_tm
        return None

    def _open_via_spotlight(self, name: str) -> bool:
        """通过 macOS Spotlight 搜索并打开"""
        try:
            Keyboard.hotkey('command', 'space')
            time.sleep(0.5)
            Keyboard.type(name)
            time.sleep(1.0)
            Keyboard.press('enter')
            logger.success(f"已通过 Spotlight 发送打开 '{name}' 的指令")
            return True
        except Exception as e:
            logger.error(f"Spotlight 唤起失败: {e}")
            return False
