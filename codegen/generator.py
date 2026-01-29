import json5
from loguru import logger
import os

class CodeGenerator:
    """将 KeymouseGo 格式的 JSON5 录制脚本转换为 ScreenOps 流式 Python 代码"""
    
    def __init__(self, json5_path: str):
        self.json5_path = json5_path
        
    def generate(self, output_path: str):
        try:
            with open(self.json5_path, 'r', encoding='utf-8') as f:
                events = json5.load(f)
        except Exception as e:
            logger.error(f"读取录制文件失败: {e}")
            return

        code_lines = [
            "from ScreenOps import ops",
            "",
            "def run_automation():",
            "    # 由 ScreenOps 自动生成的流水线脚本",
            "    # 你可以放心地交给 AI 进行后续的逻辑优化和纠错",
            "    (ops",
        ]

        for event in events:
            etype = event.get('event_type')
            atype = event.get('action_type')
            action = event.get('action')
            delay = event.get('delay', 0)

            # 添加等待
            if delay > 0.1:
                code_lines.append(f"     .wait({delay/1000:.2f})")

            if etype == 'EM': # Mouse
                if atype == 'click':
                    # 这里保持原始坐标，但 AI 可以后续将其改为 smart_click 或 ocr 模式
                    code_lines.append(f"     .click_at({action[0]}, {action[1]})")
                elif atype == 'double_click':
                    code_lines.append(f"     .double_click_at({action[0]}, {action[1]})")
            
            elif etype == 'EK': # Keyboard
                if atype == 'type':
                    content = action.replace("'", "\\'")
                    code_lines.append(f"     .type('{content}')")
                elif atype == 'hotkey':
                    keys_str = ", ".join([f"'{k}'" for k in action])
                    code_lines.append(f"     .hotkey({keys_str})")

        code_lines.append("    )")
        code_lines.append("")
        code_lines.append("if __name__ == '__main__':")
        code_lines.append("    # 💡 AI 提示 (AI Tip): ")
        code_lines.append("    # 你可以将此脚本交给 AI 工具（如 Claude/Cursor），并输入：")
        code_lines.append("    # '请帮我优化这段脚本，将其中的 .click_at(x, y) 坐标点击，")
        code_lines.append("    #  根据我录制时的视觉目标，改为更稳健的 .click(\"目标文字\") 智能点击。'")
        code_lines.append("    run_automation()")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(code_lines))
            
        logger.success(f"已生成 Python 脚本: {output_path}")
        logger.info("现在你可以将此脚本交给 AI，输入指令: '请帮我优化这段 ScreenOps 脚本，将死坐标点击改为 OCR 文字点击'")
