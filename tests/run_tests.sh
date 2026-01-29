#!/bin/bash

echo "🚀 开始运行屏幕自动化工具测试..."
echo ""

# 1. 运行诊断脚本
python3 ScreenOps/tests/health_check.py

echo ""
echo "🧪 运行逻辑单元测试 (pytest)..."
echo ""

# 2. 运行 pytest (需要安装 pytest)
if command -v pytest &> /dev/null
then
    pytest ScreenOps/tests/test_logic.py
else
    echo "⚠️ 未安装 pytest, 尝试通过 python -m pytest 运行..."
    python3 -m pytest ScreenOps/tests/test_logic.py
fi

echo ""
echo "✨ 测试流程结束。"
