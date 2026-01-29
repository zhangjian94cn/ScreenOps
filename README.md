# ScreenOps 🚀

**ScreenOps** 不仅仅是一个自动化工具，它是**为 AI Coding 时代设计的屏幕自动化引擎**。

## 🎯 核心愿景：AI 驱动的操作自动化

在 AI Coding (如 Claude, GPT, Cursor, GitHub Copilot) 普及的今天，编写复杂的自动化脚本不应再是负担。

**ScreenOps 的核心逻辑是：**
1.  **AI 作为大脑**：利用人工智能理解业务逻辑（如“帮我登录并下载账单”）。
2.  **ScreenOps 作为手脚**：提供极其简洁、高度抽象的底层接口（OCR、图像、键盘鼠标），让 AI 能够在一句话之间生成稳定可靠的 Python 自动化脚本。
3.  **零门槛脚本化**：任何复杂的屏幕操作，都可以通过 AI 结合 ScreenOps 的高层接口，瞬间转化为可维护的独立脚本。

---

## 🌟 核心能力 (AI 友好型设计)

- **🤖 AI 代理优化 API** - 每个接口（如 `smart_click`, `wait_text`）都经过精心设计，极其直观，极大降低 AI 生成代码时的幻觉风险。
- **🔤 语义化 OCR** - 直接通过“文字内容”操作，AI 只需描述“点击那个提交按钮”，ScreenOps 负责在视觉层面实现。
- **📍 高可靠图像定位** - 当文字失效时，支持图标/图片特征匹配，为 AI 提供多级容错能力。
- **🚀 智能启动 (Smart Launch)** - “打开微信并置顶”，AI 只需要调用一个函数，底层自动处理 Spotlight、窗口焦点和 OCR。
- **🧩 模块化可插拔** - 所有的 Core 能力都可以被 AI 方便地引用并组装成独立的工作流脚本。

---

## 🛠️ AI 生成脚本示例

当你告诉 AI：“请帮我写一个 ScreenOps 脚本，打开浏览器搜索今日天气，并截图”，AI 生成的代码如下：

```python
from ScreenOps import SmartLauncher, Keyboard, Screen

# AI 只需编写 3 行逻辑代码
launcher = SmartLauncher()
launcher.find_and_click("浏览器")  # 智能唤起

Keyboard.type("今日天气\n")   # 模拟输入
Screen.save_screenshot("weather.png") # 结果交付
```

---

## 📦 安装与配置

```bash
git clone https://github.com/zhangjian94cn/ScreenOps.git
cd ScreenOps
pip install -e .
# macOS 系统依赖
brew install tesseract tesseract-lang
```

## 📂 目录结构 (AI 知识脑图)
- `ScreenOps/core/`: 智能执行引擎 (Mouse/Keyboard/Launcher)
- `ScreenOps/ocr/`: 视觉文字感知
- `ScreenOps/automation/`: 规则与上下文大脑
- `ScreenOps/recorder/`: 操作录制 (供 AI 学习人类路径)

## 📄 为什么选择 ScreenOps 而不是传统 RPA？
传统 RPA 臃肿且配置繁琐。**ScreenOps 是轻量级的“原子库”**，它将屏幕操作解耦成 AI 易于理解的函数。这使得它成为了 AI Agent (智能体) 实现操作系统级自动化（OS-level Automation）的最佳底架。

---
MIT License | 由 AI 协作开发，为 AI 时代而生。
