# 用户界面模块

## 模块概述

用户界面模块为微信公众号爬虫工具提供了两种交互方式：命令行界面(CLI)和图形用户界面(GUI)，使不同类型的用户都能方便地使用工具功能。

## 接口定义

### 命令行界面(CLI)

```python
def main():
    """命令行入口函数，处理命令行参数并执行相应操作"""
    pass
```

### 图形用户界面(GUI)

```python
class WechatGUI:
    def __init__(self, token="", cookie="", output_dir=None):
        """初始化GUI界面
        
        Args:
            token (str): 初始token值
            cookie (str): 初始cookie值
            output_dir (str): 初始输出目录
        """
        pass
        
    def run(self):
        """启动GUI主循环"""
        pass
```

## 实现方式

### 命令行界面实现

1. 使用`argparse`库解析命令行参数
2. 支持的主要操作:
   - `download`: 下载文章或批量下载
   - `info`: 获取文章信息
   - `account`: 获取公众号信息
   - `gui`: 启动图形界面
3. 全局选项和操作特定选项
4. 配置文件支持

### 图形界面实现

1. 使用`tkinter`库创建图形界面
2. 主要组件:
   - 认证信息设置区
   - 输出目录设置区
   - 操作区（URL/昵称输入、模式选择等）
   - 结果显示区
3. 事件处理和异常捕获

## 使用示例

### 命令行使用示例

```bash
# 下载单篇文章
wechat-scrapper download --url "https://mp.weixin.qq.com/s/example" --cookie "..." --token "..."

# 批量下载为PDF
wechat-scrapper download --nickname "TechDaily" --format pdf --config config.json

# 获取文章信息
wechat-scrapper info --url "https://mp.weixin.qq.com/s/example" --config config.json

# 启动GUI
wechat-scrapper gui
```

### 图形界面使用示例

```python
from wechat_scrapper.gui import WechatGUI

# 初始化并启动GUI
gui = WechatGUI(token="预设token", cookie="预设cookie", output_dir="./downloads")
gui.run()
```

## GUI组件交互图

