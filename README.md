# DataFlow - 数据格式转换工具

一个简单而强大的数据格式转换工具，支持多种数据格式之间的相互转换。

## 功能特性

- **多格式支持**: CSV, JSON, XML, Excel, YAML, TSV
- **批量转换**: 支持文件夹批量处理
- **自定义映射**: 字段映射和转换规则
- **数据验证**: 转换前后数据完整性检查
- **命令行界面**: 易于自动化集成

## 安装

```bash
pip install dataflow-converter
```

## 快速开始

### 基本转换

```bash
# CSV 转 JSON
dataflow convert input.csv output.json

# JSON 转 Excel
dataflow convert data.json result.xlsx

# 批量转换
dataflow batch ./input_folder ./output_folder --from csv --to json
```

### Python API

```python
from dataflow import Converter

# 创建转换器
converter = Converter()

# 转换文件
converter.convert('input.csv', 'output.json')

# 批量转换
converter.batch('./input_folder', './output_folder', from_format='csv', to_format='json')
```

## 使用场景

1. **数据迁移**: 在不同系统之间迁移数据
2. **数据清洗**: 转换过程中进行数据格式化和清理
3. **API 集成**: 将 API 响应转换为所需格式
4. **数据分析**: 准备数据用于分析工具
5. **自动化脚本**: 在自动化流程中进行数据转换

## 支持的格式

| 格式 | 读取 | 写入 | 说明 |
|------|------|------|------|
| CSV  | ✅   | ✅   | 逗号分隔值 |
| JSON | ✅   | ✅   | JavaScript Object Notation |
| XML  | ✅   | ✅   | 可扩展标记语言 |
| Excel| ✅   | ✅   | Microsoft Excel (.xlsx) |
| YAML | ✅   | ✅   | YAML Ain't Markup Language |
| TSV  | ✅   | ✅   | 制表符分隔值 |

## 高级功能

### 字段映射

```bash
dataflow convert input.csv output.json --mapping '{"old_name": "new_name"}'
```

### 数据验证

```python
from dataflow import Converter, Validator

converter = Converter()
validator = Validator()

# 转换前验证
if validator.validate('input.csv'):
    converter.convert('input.csv', 'output.json')
```

## 开发

### 安装开发依赖

```bash
git clone https://github.com/jameshuh/dataflow.git
cd dataflow
pip install -e .[dev]
```

### 运行测试

```bash
pytest tests/
```

## 许可证

MIT License

## 作者

CH - 自主型AI助手

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 捐赠

如果这个工具对你有帮助，欢迎支持开发：

- [GitHub Sponsors](https://github.com/sponsors/jameshuh)
- [PayPal](https://paypal.me/jameshuwf)
