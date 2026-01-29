"""OCR module - 文字识别与点击"""
from .recognizer import OCRRecognizer, TextMatch
from .clicker import OCRClicker

__all__ = ['OCRRecognizer', 'TextMatch', 'OCRClicker']
