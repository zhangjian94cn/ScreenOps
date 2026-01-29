import sys
import argparse
from loguru import logger
import time

# 导入所有模块组件
from ScreenOps.core.mouse import Mouse
from ScreenOps.core.keyboard import Keyboard
from ScreenOps.core.screen import Screen
from ScreenOps.ocr.clicker import OCRClicker
from ScreenOps.image.clicker import ImageClicker
from ScreenOps.recorder.recorder import Recorder
from ScreenOps.recorder.player import Player
from ScreenOps.automation.watcher import ScreenWatcher
from ScreenOps.auto_clicker.clicker import AutoClicker
from ScreenOps.auto_clicker.hotkey import HotkeyListener
from ScreenOps.core.launcher import SmartLauncher

def main():
    parser = argparse.ArgumentParser(description="ScreenOps - 智能屏幕自动化工具")
    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # 1. 基础操作
    subparsers.add_parser('position', help='获取当前鼠标位置')
    
    click_p = subparsers.add_parser('click', help='定点点击')
    click_p.add_argument('--x', type=int, required=True)
    click_p.add_argument('--y', type=int, required=True)
    
    loop_p = subparsers.add_parser('loop', help='循环点击当前位置')
    loop_p.add_argument('--interval', type=float, default=1.0, help='间隔(秒)')
    loop_p.add_argument('--count', type=int, default=0, help='次数(0为无限)')

    # 2. OCR 点击
    ocr_p = subparsers.add_parser('ocr-click', help='OCR 文字点击')
    ocr_p.add_argument('text', help='要匹配点击的文字')
    ocr_p.add_argument('--wait', action='store_true', help='等待文字出现')
    ocr_p.add_argument('--timeout', type=int, default=10, help='等待超时(秒)')

    # 3. 图像识别
    img_p = subparsers.add_parser('img-click', help='图像匹配点击')
    img_p.add_argument('path', help='模板图片路径')
    img_p.add_argument('--wait', action='store_true', help='等待图片出现')

    # 4. 录制与回放
    record_p = subparsers.add_parser('record', help='录制鼠标键盘操作')
    record_p.add_argument('--output', '-o', default='scripts/recorded.json5', help='输出文件')
    
    play_p = subparsers.add_parser('play', help='回访运行脚本')
    play_p.add_argument('path', help='脚本文件路径')
    play_p.add_argument('--times', '-t', type=int, default=1, help='播放次数')

    # 5. 智能自动化监控
    watch_p = subparsers.add_parser('watch', help='启动工作流监控器')
    watch_p.add_argument('--rules', required=True, help='YAML 规则文件路径')
    watch_p.add_argument('--interval', type=float, default=2.0, help='检测间隔')

    # 6. 智能点击
    smart_p = subparsers.add_parser('smart-click', help='智能寻找并点击(描述文字或搜索)')
    smart_p.add_argument('desc', help='描述文字(如: 微信)')
    
    args = parser.parse_args()

    if args.command == 'position':
        pos = Mouse.position()
        print(f"当前鼠标位置: {pos}")

    elif args.command == 'click':
        Mouse.click(args.x, args.y)
        logger.success(f"已点击 ({args.x}, {args.y})")

    elif args.command == 'loop':
        clicker = AutoClicker(interval=args.interval)
        # 启动热键
        listener = HotkeyListener(on_toggle=clicker.toggle, on_stop=clicker.stop)
        listener.start()
        clicker.start(count=args.count)
        try:
            while clicker.running: time.sleep(0.1)
        except KeyboardInterrupt:
            clicker.stop()

    elif args.command == 'ocr-click':
        clicker = OCRClicker()
        if args.wait:
            clicker.wait_and_click(args.text, timeout=args.timeout)
        else:
            clicker.click_text(args.text)

    elif args.command == 'img-click':
        clicker = ImageClicker()
        if args.wait:
            clicker.wait_and_click(args.path)
        else:
            clicker.click_image(args.path)

    elif args.command == 'record':
        recorder = Recorder()
        logger.info("准备录制... 按下 Ctrl+C 停止")
        try:
            recorder.start()
            while True: time.sleep(1)
        except KeyboardInterrupt:
            events = recorder.stop()
            recorder.save(args.output)

    elif args.command == 'play':
        player = Player()
        player.play(args.path, times=args.times)
        try:
            while player.running: time.sleep(0.1)
        except KeyboardInterrupt:
            player.stop()

    elif args.command == 'watch':
        watcher = ScreenWatcher(args.rules, interval=args.interval)
        watcher.start()
        try:
            while watcher.running: time.sleep(1)
        except KeyboardInterrupt:
            watcher.stop()

    elif args.command == 'smart-click':
        launcher = SmartLauncher()
        launcher.find_and_click(args.desc)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
