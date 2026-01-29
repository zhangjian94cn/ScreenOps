"""Automation module - 智能自动化"""
from .context import AutomationContext
from .trigger import Trigger, TriggerType
from .rules import Rule, RuleEngine
from .watcher import ScreenWatcher

__all__ = ['AutomationContext', 'Trigger', 'TriggerType', 'Rule', 'RuleEngine', 'ScreenWatcher']
