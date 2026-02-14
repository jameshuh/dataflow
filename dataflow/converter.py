"""
核心转换功能模块

支持多种数据格式之间的相互转换。
"""

import pandas as pd
import json
import yaml
import os
from pathlib import Path
from typing import Optional, Dict, Any, List


class Converter:
    """数据格式转换器"""
    
    SUPPORTED_FORMATS = ['csv', 'json', 'xml', 'xlsx', 'yaml', 'tsv']
    
    def __init__(self):
        """初始化转换器"""
        self.validation_enabled = True
    
    def convert(
        self, 
        input_file: str, 
        output_file: str,
        mapping: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        转换单个文件
        
        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
            mapping: 字段映射字典（可选）
        
        Returns:
            转换是否成功
        """
        try:
            # 读取数据
            df = self._read_file(input_file)
            
            if df is None or df.empty:
                raise ValueError(f"无法读取文件或文件为空: {input_file}")
            
            # 应用字段映射
            if mapping:
                df = df.rename(columns=mapping)
            
            # 写入文件
            success = self._write_file(df, output_file)
            
            return success
            
        except Exception as e:
            print(f"转换失败: {e}")
            return False
    
    def batch(
        self,
        input_folder: str,
        output_folder: str,
        from_format: str,
        to_format: str,
        mapping: Optional[Dict[str, str]] = None
    ) -> Dict[str, bool]:
        """
        批量转换文件夹中的文件
        
        Args:
            input_folder: 输入文件夹路径
            output_folder: 输出文件夹路径
            from_format: 源格式
            to_format: 目标格式
            mapping: 字段映射字典（可选）
        
        Returns:
            文件名到转换结果的映射
        """
        results = {}
        
        # 确保输出文件夹存在
        os.makedirs(output_folder, exist_ok=True)
        
        # 遍历输入文件夹
        input_path = Path(input_folder)
        for file_path in input_path.glob(f"*.{from_format}"):
            output_file = os.path.join(
                output_folder, 
                f"{file_path.stem}.{to_format}"
            )
            
            success = self.convert(str(file_path), output_file, mapping)
            results[file_path.name] = success
        
        return results
    
    def _read_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        读取文件到 DataFrame
        
        Args:
            file_path: 文件路径
        
        Returns:
            pandas DataFrame 或 None
        """
        ext = Path(file_path).suffix.lower().lstrip('.')
        
        try:
            if ext == 'csv':
                return pd.read_csv(file_path)
            elif ext == 'json':
                return pd.read_json(file_path)
            elif ext == 'xml':
                return pd.read_xml(file_path)
            elif ext in ['xlsx', 'xls']:
                return pd.read_excel(file_path)
            elif ext in ['yaml', 'yml']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                return pd.DataFrame(data)
            elif ext == 'tsv':
                return pd.read_csv(file_path, sep='\t')
            else:
                raise ValueError(f"不支持的文件格式: {ext}")
        except Exception as e:
            print(f"读取文件失败: {e}")
            return None
    
    def _write_file(self, df: pd.DataFrame, file_path: str) -> bool:
        """
        将 DataFrame 写入文件
        
        Args:
            df: pandas DataFrame
            file_path: 输出文件路径
        
        Returns:
            写入是否成功
        """
        ext = Path(file_path).suffix.lower().lstrip('.')
        
        try:
            if ext == 'csv':
                df.to_csv(file_path, index=False, encoding='utf-8')
            elif ext == 'json':
                df.to_json(file_path, orient='records', force_ascii=False, indent=2)
            elif ext == 'xml':
                df.to_xml(file_path, index=False)
            elif ext == 'xlsx':
                df.to_excel(file_path, index=False, engine='openpyxl')
            elif ext in ['yaml', 'yml']:
                data = df.to_dict(orient='records')
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
            elif ext == 'tsv':
                df.to_csv(file_path, index=False, sep='\t', encoding='utf-8')
            else:
                raise ValueError(f"不支持的输出格式: {ext}")
            
            return True
            
        except Exception as e:
            print(f"写入文件失败: {e}")
            return False
    
    def get_supported_formats(self) -> List[str]:
        """获取支持的格式列表"""
        return self.SUPPORTED_FORMATS.copy()
    
    def is_format_supported(self, format_name: str) -> bool:
        """检查格式是否支持"""
        return format_name.lower() in self.SUPPORTED_FORMATS
