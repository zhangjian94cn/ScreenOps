# ScreenOps 工作流目录

此目录用于存放用户自定义的自动化脚本。

## 使用方法

1. 将你的 Python 脚本放入此目录
2. 脚本应遵循 ScreenOps 的 API 规范
3. 使用 `from ScreenOps import ops` 导入流式接口

## 示例脚本

- `wechat_auto_reply.py` - 微信自动回复示例

## 添加新工作流

你可以直接向 AI 描述你的需求，例如：

> "请帮我写一个 ScreenOps 脚本，每天早上自动打开钉钉打卡"

AI 将生成符合本项目规范的 Python 脚本，你可以将其保存到此目录。
