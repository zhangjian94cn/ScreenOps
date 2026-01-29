import cv2
import numpy as np
from PIL import Image
import pyautogui
from typing import Optional, Tuple, List
from loguru import logger

class ImageMatcher:
    """基于 OpenCV 的图像匹配器"""
    
    @staticmethod
    def pil_to_cv2(image: Image.Image) -> np.ndarray:
        """将 PIL Image 转换为 OpenCV 格式"""
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    @staticmethod
    def match(template_path: str, screen_image: Optional[Image.Image] = None, threshold: float = 0.8) -> Optional[Tuple[int, int, int, int]]:
        """
        在屏幕截图(或指定图片)中匹配模板图片
        返回: (left, top, width, height) 如果找到, 否则返回 None
        """
        try:
            if screen_image is None:
                screen_image = pyautogui.screenshot()
            
            img_cv = ImageMatcher.pil_to_cv2(screen_image)
            template = cv2.imread(template_path)
            
            if template is None:
                logger.error(f"无法读取模板图片: {template_path}")
                return None
            
            th, tw = template.shape[:2]
            
            # 使用模板匹配
            res = cv2.matchTemplate(img_cv, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            
            if max_val >= threshold:
                return (max_loc[0], max_loc[1], tw, th)
            
            return None
        except Exception as e:
            logger.error(f"图片识别失败: {e}")
            return None

    @staticmethod
    def match_all(template_path: str, screen_image: Optional[Image.Image] = None, threshold: float = 0.8) -> List[Tuple[int, int, int, int]]:
        """在屏幕上查找所有匹配的位置"""
        try:
            if screen_image is None:
                screen_image = pyautogui.screenshot()
                
            img_cv = ImageMatcher.pil_to_cv2(screen_image)
            template = cv2.imread(template_path)
            
            if template is None:
                return []
                
            th, tw = template.shape[:2]
            res = cv2.matchTemplate(img_cv, template, cv2.TM_CCOEFF_NORMED)
            
            y_coords, x_coords = np.where(res >= threshold)
            
            matches = []
            # 简单的重叠过滤 (只取局部的最大值)
            # 这里简化处理, 在实际复杂应用中可能需要更科学的 NMS (Non-Maximum Suppression)
            for x, y in zip(x_coords, y_coords):
                matches.append((int(x), int(y), tw, th))
                
            return matches
        except Exception as e:
            logger.error(f"批量图片识别失败: {e}")
            return []
