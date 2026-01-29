from ScreenOps.core.keyboard import Keyboard
import time
from loguru import logger

def open_wechat():
    logger.info("正在尝试打开微信...")
    
    # 1. 唤起 Spotlight (Cmd + Space)
    logger.info("唤起 Spotlight (command + space)")
    Keyboard.hotkey('command', 'space')
    time.sleep(1)
    
    # 2. 输入 WeChat
    logger.info("输入 'WeChat'")
    Keyboard.type('WeChat', interval=0.1)
    time.sleep(1)
    
    # 3. 按回车确认
    logger.info("按下回车键")
    Keyboard.press('enter')
    
    logger.success("已发送打开微信的指令")

if __name__ == "__main__":
    open_wechat()
