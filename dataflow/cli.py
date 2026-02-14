"""
命令行接口模块

提供 dataflow 命令行工具。
"""

import click
import json
from pathlib import Path
from .converter import Converter
from .utils import get_file_info, validate_data


@click.group()
@click.version_option(version='0.1.0')
def main():
    """DataFlow - 数据格式转换工具"""
    pass


@main.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--mapping', '-m', help='字段映射（JSON格式）')
def convert(input_file: str, output_file: str, mapping: str):
    """转换单个文件
    
    示例:
        dataflow convert input.csv output.json
        dataflow convert data.json result.xlsx -m '{"old":"new"}'
    """
    converter = Converter()
    
    # 解析字段映射
    mapping_dict = None
    if mapping:
        try:
            mapping_dict = json.loads(mapping)
        except json.JSONDecodeError:
            click.echo("错误: 映射格式无效，请使用 JSON 格式", err=True)
            return
    
    # 执行转换
    click.echo(f"正在转换 {input_file} → {output_file}")
    success = converter.convert(input_file, output_file, mapping_dict)
    
    if success:
        click.echo("✓ 转换成功")
    else:
        click.echo("✗ 转换失败", err=True)


@main.command()
@click.argument('input_folder', type=click.Path(exists=True))
@click.argument('output_folder', type=click.Path())
@click.option('--from', 'from_format', required=True, help='源格式')
@click.option('--to', 'to_format', required=True, help='目标格式')
@click.option('--mapping', '-m', help='字段映射（JSON格式）')
def batch(input_folder: str, output_folder: str, from_format: str, to_format: str, mapping: str):
    """批量转换文件
    
    示例:
        dataflow batch ./input ./output --from csv --to json
    """
    converter = Converter()
    
    # 检查格式支持
    if not converter.is_format_supported(from_format):
        click.echo(f"错误: 不支持源格式 '{from_format}'", err=True)
        return
    
    if not converter.is_format_supported(to_format):
        click.echo(f"错误: 不支持目标格式 '{to_format}'", err=True)
        return
    
    # 解析字段映射
    mapping_dict = None
    if mapping:
        try:
            mapping_dict = json.loads(mapping)
        except json.JSONDecodeError:
            click.echo("错误: 映射格式无效，请使用 JSON 格式", err=True)
            return
    
    # 执行批量转换
    click.echo(f"批量转换 {from_format} → {to_format}")
    results = converter.batch(input_folder, output_folder, from_format, to_format, mapping_dict)
    
    # 显示结果
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    click.echo(f"\n完成: {success_count}/{total_count} 个文件转换成功")
    
    for file, success in results.items():
        status = "✓" if success else "✗"
        click.echo(f"  {status} {file}")


@main.command()
@click.argument('file_path', type=click.Path(exists=True))
def info(file_path: str):
    """显示文件信息
    
    示例:
        dataflow info data.csv
    """
    info = get_file_info(file_path)
    
    if "error" in info:
        click.echo(f"错误: {info['error']}", err=True)
        return
    
    click.echo(f"文件名: {info['name']}")
    click.echo(f"格式: {info['format']}")
    click.echo(f"大小: {info['size_mb']} MB")
    click.echo(f"修改时间: {info['modified']}")


@main.command()
def formats():
    """显示支持的格式列表"""
    converter = Converter()
    supported = converter.get_supported_formats()
    
    click.echo("支持的格式:")
    for fmt in supported:
        click.echo(f"  • {fmt}")


if __name__ == '__main__':
    main()
