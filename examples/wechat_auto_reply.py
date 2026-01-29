"""
这是一个展示如何使用 ScreenOps 简化接口的示例。
场景：在微信中搜索特定的联系人并自动回复。

你可以直接把这个逻辑描述给 AI，让它帮你生成类似的代码。
"""
from ScreenOps import ops
import sys

def auto_reply(contact_name, message):
    try:
        # 1. 打开微信 (如果没在屏幕上则启动它)
        # 2. 等待搜索框出现
        # 3. 搜索联系人并回车
        # 4. 输入回复内容并发送
        (ops.open("微信")
            .wait_for("搜索", timeout=5)
            .type(contact_name, enter=True)
            .wait(1) 
            .type(message, enter=True))
            
        print(f"✅ 成功给 {contact_name} 发送了消息")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "文件传输助手"
    msg = "这是由 ScreenOps 自动发送的消息 🚀"
    auto_reply(name, msg)
