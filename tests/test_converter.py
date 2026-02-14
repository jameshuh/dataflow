"""
测试模块

测试核心转换功能。
"""

import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path
from dataflow.converter import Converter
from dataflow.utils import detect_format, validate_data


class TestConverter:
    """测试 Converter 类"""
    
    @pytest.fixture
    def converter(self):
        """创建转换器实例"""
        return Converter()
    
    @pytest.fixture
    def sample_df(self):
        """创建测试数据"""
        return pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'city': ['New York', 'London', 'Tokyo']
        })
    
    @pytest.fixture
    def temp_dir(self):
        """创建临时目录"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    def test_supported_formats(self, converter):
        """测试支持的格式列表"""
        formats = converter.get_supported_formats()
        
        assert 'csv' in formats
        assert 'json' in formats
        assert 'xml' in formats
        assert 'xlsx' in formats
        assert 'yaml' in formats
    
    def test_csv_to_json(self, converter, sample_df, temp_dir):
        """测试 CSV 转 JSON"""
        # 创建输入文件
        input_file = os.path.join(temp_dir, 'test.csv')
        sample_df.to_csv(input_file, index=False)
        
        # 转换
        output_file = os.path.join(temp_dir, 'test.json')
        success = converter.convert(input_file, output_file)
        
        # 验证
        assert success
        assert os.path.exists(output_file)
        
        # 读取并验证内容
        result = pd.read_json(output_file)
        assert len(result) == 3
        assert 'name' in result.columns
    
    def test_json_to_csv(self, converter, sample_df, temp_dir):
        """测试 JSON 转 CSV"""
        # 创建输入文件
        input_file = os.path.join(temp_dir, 'test.json')
        sample_df.to_json(input_file, orient='records')
        
        # 转换
        output_file = os.path.join(temp_dir, 'test.csv')
        success = converter.convert(input_file, output_file)
        
        # 验证
        assert success
        assert os.path.exists(output_file)
    
    def test_field_mapping(self, converter, sample_df, temp_dir):
        """测试字段映射"""
        # 创建输入文件
        input_file = os.path.join(temp_dir, 'test.csv')
        sample_df.to_csv(input_file, index=False)
        
        # 转换并映射字段
        output_file = os.path.join(temp_dir, 'test.json')
        mapping = {'name': 'full_name', 'age': 'years_old'}
        success = converter.convert(input_file, output_file, mapping)
        
        # 验证
        assert success
        result = pd.read_json(output_file)
        assert 'full_name' in result.columns
        assert 'years_old' in result.columns
    
    def test_batch_conversion(self, converter, sample_df, temp_dir):
        """测试批量转换"""
        # 创建多个输入文件
        input_folder = os.path.join(temp_dir, 'input')
        output_folder = os.path.join(temp_dir, 'output')
        os.makedirs(input_folder)
        
        for i in range(3):
            file_path = os.path.join(input_folder, f'file{i}.csv')
            sample_df.to_csv(file_path, index=False)
        
        # 批量转换
        results = converter.batch(input_folder, output_folder, 'csv', 'json')
        
        # 验证
        assert len(results) == 3
        assert all(results.values())
        
        # 检查输出文件
        output_files = list(Path(output_folder).glob('*.json'))
        assert len(output_files) == 3


class TestUtils:
    """测试工具函数"""
    
    def test_detect_format(self):
        """测试格式检测"""
        assert detect_format('data.csv') == 'csv'
        assert detect_format('data.json') == 'json'
        assert detect_format('data.xml') == 'xml'
        assert detect_format('data.xlsx') == 'xlsx'
        assert detect_format('data.yaml') == 'yaml'
        assert detect_format('data.yml') == 'yaml'
        assert detect_format('data.tsv') == 'tsv'
    
    def test_validate_data(self):
        """测试数据验证"""
        # 有效数据
        df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'age': [25, 30]
        })
        is_valid, errors = validate_data(df)
        assert is_valid
        
        # 空数据
        empty_df = pd.DataFrame()
        is_valid, errors = validate_data(empty_df)
        assert not is_valid
