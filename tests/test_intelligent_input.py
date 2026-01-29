import time
from loguru import logger
from ScreenOps.automation.watcher import ScreenWatcher
from ScreenOps.core.keyboard import Keyboard
from ScreenOps.core.mouse import Mouse
import os

def test_intelligent_terminal_input():
    """
    测试“发现终端需要输入内容，自动判断输入什么”的场景。
    
    模拟流程：
    1. 打开一个 Mock 的规则文件，该规则监听屏幕上的 "Commit" 或 "Password" 文字。
    2. 如果看到 "Enter password"，自动输入预设密码。
    """
    
    # 创建一个测试规则
    rule_content = """
name: 终端自动化测试
context:
  commit_msg: "feat: add intelligent screen automation"
  sudo_pass: "mypassword123"

rules:
  - name: "处理 Git 提交"
    trigger:
      type: "text_appear"
      pattern: "Commit message:"
    action: "type"
    params:
      text: "{{commit_msg}}\n"

  - name: "处理 Sudo 密码"
    trigger:
      type: "text_appear"
      pattern: "Password:"
    action: "type"
    params:
      text: "{{sudo_pass}}\n"
"""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(rule_content)
        rule_file = f.name
    
    logger.info(f"开启智能终端自动化监控 (测试用)...")
    watcher = ScreenWatcher(rule_file, interval=1.0)

    
    print("\n--- 智能输入测试说明 ---")
    print("1. 脚本正在监控屏幕。")
    print("2. 请尝试在任何地方（如记事本、终端）输入或显示文字 'Commit message:' 或 'Password:'。")
    print("3. 系统检测到这些文字后，应会自动帮你键入预设的内容。")
    print("4. 按 Ctrl+C 停止测试。")
    
    try:
        watcher.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        watcher.stop()
        logger.info("测试结束")

if __name__ == "__main__":
    test_intelligent_terminal_input()
