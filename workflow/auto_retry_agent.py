"""
Agent Error Auto-Retry Workflow

功能：每隔 10 秒检查屏幕，如果发现 "Agent terminated due to error" 弹窗，
自动点击 "Retry" 按钮。如果屏幕上没有该弹窗则不操作。

使用方法：
    PYTHONPATH=. python3 ScreenOps/workflow/auto_retry_agent.py
    
停止：按 Ctrl+C
"""
import time
from loguru import logger

# 确保可以找到 ScreenOps 模块
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ScreenOps.ocr.clicker import OCRClicker
from ScreenOps.image.matcher import ImageMatcher
from ScreenOps.core.mouse import Mouse

# 配置
CHECK_INTERVAL = 10  # 检查间隔（秒）
ERROR_TEXT = "Agent terminated due to error"
RETRY_TEXT = "Retry"
ERROR_IMAGE = "ScreenOps/resources/icons/agent_error_dialog.png"

def auto_retry():
    """主监控循环"""
    ocr = OCRClicker()
    img_matcher = ImageMatcher()
    
    logger.info("🚀 Agent Error Auto-Retry 已启动")
    logger.info(f"   检查间隔: {CHECK_INTERVAL}s")
    logger.info(f"   监控目标: '{ERROR_TEXT}'")
    logger.info("   按 Ctrl+C 停止")
    
    while True:
        try:
            # 方法1: 尝试图像匹配（更可靠）
            match = img_matcher.match(ERROR_IMAGE, threshold=0.7)
            if match:
                logger.warning("🔴 检测到错误弹窗 (图像匹配)")
                # 点击 Retry 按钮 (尝试 OCR)
                if ocr.click_text(RETRY_TEXT):
                    logger.success("✅ 已点击 Retry 按钮")
                else:
                    # 如果 OCR 找不到，尝试在弹窗右侧点击（Retry 按钮通常在右侧）
                    x = match[0] + match[2] - 50  # 弹窗右侧偏左一点
                    y = match[1] + match[3] - 30  # 弹窗底部
                    Mouse.click(x, y)
                    logger.success(f"✅ 已点击坐标 ({x}, {y})")
                time.sleep(2)  # 点击后等待一下
                continue
            
            # 方法2: 尝试 OCR 文字匹配
            if ocr.recognizer.find_text(ERROR_TEXT):
                logger.warning("🔴 检测到错误弹窗 (OCR 文字)")
                if ocr.click_text(RETRY_TEXT):
                    logger.success("✅ 已点击 Retry 按钮")
                time.sleep(2)
                continue
            
            # 没有检测到错误
            logger.debug(f"✓ 屏幕正常，{CHECK_INTERVAL}s 后再次检查...")
            
        except Exception as e:
            logger.error(f"检测过程出错: {e}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        auto_retry()
    except KeyboardInterrupt:
        logger.info("👋 已停止监控")
