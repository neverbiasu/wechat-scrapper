# 格式转换模块

## 模块概述

格式转换模块提供了对微信公众号文章进行格式转换的功能，将HTML内容转换为PDF或Markdown格式，以满足不同场景下的使用需求。

## 接口定义

### HTML到PDF转换

```python
class Url2Pdf:
    def __init__(self, *args, **kwargs):
        """初始化PDF转换器"""
        pass
        
    def url_to_pdf(self, url, title):
        """将URL转换为PDF文件
        
        Args:
            url (str): 要转换的URL
            title (str): 输出PDF文件名（不含扩展名）
            
        Returns:
            str: 操作结果消息
        """
        pass
```

### HTML到Markdown转换

```python
class Html2Markdown:
    def __init__(self):
        """初始化Markdown转换器"""
        pass
        
    def convert(self, html_content, title):
        """将HTML内容转换为Markdown
        
        Args:
            html_content (str): HTML内容字符串
            title (str): 输出Markdown文件名（不含扩展名）
            
        Returns:
            str: 操作结果消息
        """
        pass
```

## 实现方式

### PDF转换实现

1. 使用`pyhtml2pdf`库作为转换引擎
2. 步骤:
   - 获取URL对应的HTML内容
   - 创建临时HTML文件
   - 使用转换器将HTML转为PDF
   - 保存PDF文件
   - 清理临时文件

### Markdown转换实现

1. 使用`html2text`库作为转换引擎
2. 步骤:
   - 解析HTML内容
   - 提取正文部分
   - 转换为Markdown格式
   - 保存为.md文件

## 使用示例

### PDF转换示例

```python
from wechat_scrapper.utils import Url2Pdf

converter = Url2Pdf()
result = converter.url_to_pdf(
    "https://mp.weixin.qq.com/s/example-url", 
    "./downloads/example"
)
print(result)  # 输出: "PDF 已保存为 ./downloads/example.pdf"
```

### Markdown转换示例

```python
from wechat_scrapper.utils import Html2Markdown

# 获取HTML内容
html_content = scrapper.download_article("https://mp.weixin.qq.com/s/example-url", mode=1)

# 转换为Markdown
converter = Html2Markdown()
result = converter.convert(html_content, "./downloads/example")
print(result)  # 输出: "Markdown 已保存为 ./downloads/example.md"
```

## 异常处理

两个转换器都实现了以下异常处理:

1. **验证检测**: 检查是否需要完成验证，如需要则提示用户
2. **类型检查**: 验证输入内容的类型是否正确
3. **路径确保**: 自动创建必要的目录结构
4. **通用错误捕获**: 捕获并格式化转换过程中的任何错误
