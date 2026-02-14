"""
DataFlow - 数据格式转换工具

一个简单而强大的数据格式转换工具。
"""

__version__ = "0.1.0"
__author__ = "CH"

from .converter import Converter
from .utils import detect_format, validate_data

__all__ = ["Converter", "detect_format", "validate_data"]
