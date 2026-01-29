import pytesseract
from PIL import Image
import pyautogui
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict
from loguru import logger

@dataclass
class TextMatch:
    """OCR 识别到的文字匹配项"""
    text: str
    x: int
    y: int
    width: int
    height: int
    confidence: float
    
    @property
    def center(self) -> Tuple[int, int]:
        """获取文字中心坐标"""
        return (self.x + self.width // 2, self.y + self.height // 2)

    def __str__(self):
        return f"['{self.text}' @ ({self.x},{self.y}) conf={self.confidence:.1f}]"

class OCRRecognizer:
    """OCR 文字识别器"""
    
    def __init__(self, lang: str = 'chi_sim+eng'):
        self.lang = lang
        # 尝试检查 tesseract 是否安装
        try:
            pytesseract.get_tesseract_version()
        except Exception:
            logger.warning("未检测到 Tesseract OCR。请确保已安装 tesseract 并添加至系统 PATH (brew install tesseract)")

    def recognize(self, image: Optional[Image.Image] = None) -> List[TextMatch]:
        """识别屏幕或指定图片中的文字"""
        if image is None:
            try:
                image = pyautogui.screenshot()
            except Exception as e:
                logger.error(f"截图失败: {e}")
                return []
        
        try:
            # 使用 pytesseract 获取详细的文字和位置信息
            # image_to_data 返回包含坐标、置信度等信息的字典
            data = pytesseract.image_to_data(
                image, 
                lang=self.lang,
                output_type=pytesseract.Output.DICT
            )
            
            results = []
            for i, text in enumerate(data['text']):
                # 过滤置信度过低或空白的文本
                if text.strip() and int(data['conf'][i]) > 0:
                    results.append(TextMatch(
                        text=text.strip(),
                        x=data['left'][i],
                        y=data['top'][i],
                        width=data['width'][i],
                        height=data['height'][i],
                        confidence=float(data['conf'][i])
                    ))
            return results
        except Exception as e:
            logger.error(f"OCR 识别失败: {e}")
            return []
    
    def find_text(self, target: str, regex: bool = False, min_confidence: float = 30.0) -> Optional[TextMatch]:
        """在屏幕上查找指定文字"""
        matches = self.recognize()
        
        # 首先尝试完全匹配或包含匹配
        for match in matches:
            if match.confidence < min_confidence:
                continue
                
            if regex:
                import re
                if re.search(target, match.text, re.IGNORE_CASE):
                    return match
            else:
                if target.lower() in match.text.lower():
                    return match
        
        return None
