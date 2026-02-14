"""
工具函数模块

提供数据验证和格式检测功能。
"""

import os
from pathlib import Path
from typing import Optional
import pandas as pd


def detect_format(file_path: str) -> Optional[str]:
    """
    根据文件扩展名检测格式
    
    Args:
        file_path: 文件路径
    
    Returns:
        格式名称或 None
    """
    ext = Path(file_path).suffix.lower().lstrip('.')
    
    format_map = {
        'csv': 'csv',
        'json': 'json',
        'xml': 'xml',
        'xlsx': 'xlsx',
        'xls': 'xlsx',
        'yaml': 'yaml',
        'yml': 'yaml',
        'tsv': 'tsv'
    }
    
    return format_map.get(ext)


def validate_data(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    验证数据完整性
    
    Args:
        df: pandas DataFrame
    
    Returns:
        (是否有效, 错误列表)
    """
    errors = []
    
    # 检查是否为空
    if df is None:
        errors.append("DataFrame 为 None")
        return False, errors
    
    if df.empty:
        errors.append("DataFrame 为空")
        return False, errors
    
    # 检查是否有空值
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        for col, count in null_counts.items():
            if count > 0:
                errors.append(f"列 '{col}' 有 {count} 个空值")
    
    # 检查是否有重复行
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        errors.append(f"有 {duplicates} 个重复行")
    
    # 即使有空值或重复，数据仍然有效
    return True, errors


def get_file_info(file_path: str) -> dict:
    """
    获取文件信息
    
    Args:
        file_path: 文件路径
    
    Returns:
        文件信息字典
    """
    path = Path(file_path)
    
    if not path.exists():
        return {"error": "文件不存在"}
    
    stat = path.stat()
    
    return {
        "name": path.name,
        "format": detect_format(file_path),
        "size": stat.st_size,
        "size_mb": round(stat.st_size / (1024 * 1024), 2),
        "modified": stat.st_mtime
    }
