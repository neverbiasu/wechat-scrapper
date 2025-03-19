# 微信公众号爬虫工具 - 贡献指南

## 开发环境设置

### 基础环境准备

1. 克隆代码库

```bash
git clone https://github.com/yourusername/wechat-scrapper.git
cd wechat-scrapper
```

2. 创建虚拟环境（推荐）

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate.bat  # Windows
```

3. 安装依赖

```bash
pip install -r requirements.txt
pip install -e .  # 以可编辑模式安装
```

### 开发工具配置

1. 安装开发工具

```bash
pip install black pytest pre-commit
pre-commit install
```

2. IDE 建议配置
   - VSCode: 建议安装 Python、Pylance、Black Formatter 扩展
   - PyCharm: 启用 PEP8 检查，配置 Black 作为格式化工具
   - 任何编辑器: 配置 EditorConfig 支持

## 代码规范

### 格式化规范

本项目使用 [Black](https://black.readthedocs.io/) 作为代码格式化工具。为了保持一致的代码风格，请在提交代码前运行 Black：

```bash
black .
```

我们已配置 pre-commit 钩子，在每次提交时自动运行 Black。

### 代码风格指南

1. **命名规范**
   - 类名: 使用 PascalCase (例如 `WechatScrapper`)
   - 函数/方法: 使用 snake_case (例如 `download_article`)
   - 常量: 使用全大写 SNAKE_CASE (例如 `MAX_RETRY_COUNT`)
   - 私有方法/属性: 使用下划线前缀 (例如 `_add_random_delay`)

2. **注释规范**
   - 使用文档字符串 (docstrings) 描述类、方法和函数
   - 遵循 Google 风格的文档字符串格式
   - 对复杂逻辑添加行内注释
   - 中文注释使用 UTF-8 编码

3. **导入顺序**
   - 标准库导入
   - 相关第三方库导入
   - 本地应用/库特定导入

## 测试指南

### 编写测试

1. 所有新功能都应添加相应的单元测试
2. 使用 pytest 作为测试框架
3. 测试文件命名为 `test_*.py`
4. 针对不同功能模块编写独立测试类

### 运行测试

运行所有测试:

```bash
pytest
```

运行特定测试文件:

```bash
pytest tests/test_scrapper.py
```

运行特定测试方法:

```bash
pytest tests/test_scrapper.py::TestWechatScrapper::test_download_article
```

生成覆盖率报告:

```bash
pytest --cov=wechat_scrapper
```

## 提交规范

### 提交消息格式

提交消息应遵循以下格式：

