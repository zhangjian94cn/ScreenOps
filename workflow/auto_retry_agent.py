"""
Agent Error Auto-Retry Workflow

功能：每隔 10 秒检查屏幕，如果发现 "Agent terminated due to error" 弹窗，
自动点击 "Retry" 按钮。如果屏幕上没有该弹窗则不操作。

使用方法：
    cd /Volumes/home2/Code/script
    PYTHONPATH=. python3 ScreenOps/workflow/auto_retry_agent.py
    
停止：按 Ctrl+C
"""
import time
from loguru import logger

# 确保可以找到 ScreenOps 模块
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ScreenOps.ocr.recognizer import OCRRecognizer
from ScreenOps.core.mouse import Mouse

# 配置
CHECK_INTERVAL = 10  # 检查间隔（秒）
ERROR_TEXT = "Agent terminated due to error"
RETRY_TEXT = "Retry"

def auto_retry():
    """主监控循环"""
    ocr = OCRRecognizer()
    
    logger.info("🚀 Agent Error Auto-Retry 已启动")
    logger.info(f"   检查间隔: {CHECK_INTERVAL}s")
    logger.info(f"   监控目标: '{ERROR_TEXT}'")
    logger.info("   按 Ctrl+C 停止")
    
    while True:
        try:
            # 使用 OCR 进行精确的文字匹配
            results = ocr.recognize()
            
            # 检查是否有错误文字
            error_found = False
            retry_box = None
            
            for item in results:
                text = item.text.strip()
                # 严格匹配错误文字（不是子串匹配）
                if "Agent terminated" in text or "due to error" in text:
                    error_found = True
                    logger.warning(f"🔴 检测到错误文字: '{text}'")
                
                # 严格匹配 Retry 按钮（必须是独立的 Retry，不是文件名的一部分）
                if text == "Retry" or text == "Retry ":
                    retry_box = item
                    logger.info(f"📍 找到 Retry 按钮位置: ({item.center[0]}, {item.center[1]})")
            
            if error_found and retry_box:
                # 点击 Retry 按钮
                x, y = retry_box.center
                logger.success(f"✅ 正在点击 Retry 按钮 ({x}, {y})")
                Mouse.click(x, y)
                time.sleep(3)  # 点击后等待
                continue
            elif error_found:
                logger.warning("⚠️ 检测到错误但未找到 Retry 按钮，等待下次检查")
            else:
                logger.debug(f"✓ 屏幕正常，{CHECK_INTERVAL}s 后再次检查...")
            
        except Exception as e:
            logger.error(f"检测过程出错: {e}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        auto_retry()
    except KeyboardInterrupt:
        logger.info("👋 已停止监控")
