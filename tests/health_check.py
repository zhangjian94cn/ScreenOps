import sys
import os
import pyautogui
from PIL import Image
import pytesseract
import cv2
import numpy as np
from loguru import logger

def check_dependencies():
    print("=== 依赖与环境诊断 ===")
    
    # 1. 检查 Python 版本
    print(f"Python 版本: {sys.version.split()[0]}")
    
    # 2. 检查 Tesseract
    try:
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract OCR: 已安装 (版本 {version})")
    except Exception as e:
        print(f"❌ Tesseract OCR: 未找到。请运行 'brew install tesseract'")

    # 3. 检查 OpenCV
    try:
        print(f"✅ OpenCV: 已安装 (版本 {cv2.__version__})")
    except ImportError:
        print(f"❌ OpenCV: 未安装。请运行 'pip install opencv-python'")

    # 4. 检查屏幕访问权限 (macOS)
    try:
        size = pyautogui.size()
        print(f"✅ 屏幕分辨率: {size[0]}x{size[1]}")
        
        # 尝试截图测试权限
        screenshot = pyautogui.screenshot(region=(0, 0, 10, 10))
        print("✅ 屏幕截图权限: 正常")
    except Exception as e:
        print(f"❌ 屏幕访问权限: 可能受限。请在 系统设置 -> 隐私与安全性 -> 辅助功能/屏幕录制 中检查。")
        print(f"   错误信息: {e}")

    # 5. 检查 PyAutoGUI 故障安全
    print(f"ℹ️ PyAutoGUI 故障安全 (Fail-safe): {'开启' if pyautogui.FAILSAFE else '关闭'} (将鼠标移至屏幕角落可紧急停止)")

def test_ocr_functionality():
    print("\n=== OCR 功能简单测试 ===")
    try:
        # 截取屏幕中央一小块区域进行识别
        sw, sh = pyautogui.size()
        region = (sw//2 - 100, sh//2 - 50, 200, 100)
        img = pyautogui.screenshot(region=region)
        
        # 临时保存用于观察
        # img.save("ocr_debug.png")
        
        data = pytesseract.image_to_string(img, lang='chi_sim+eng')
        print(f"识别到的内容预览 (屏幕中心区域):")
        print("-" * 20)
        print(data.strip() or "[空白内容]")
        print("-" * 20)
        print("✅ OCR 流程调用正常")
    except Exception as e:
        print(f"❌ OCR 测试运行失败: {e}")

if __name__ == "__main__":
    check_dependencies()
    test_ocr_functionality()
