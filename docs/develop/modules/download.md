# 下载功能模块

## 模块概述

下载功能模块实现了微信公众号文章的单篇下载和批量下载核心功能，支持验证处理和反爬策略，可设置下载模式和输出格式。

## 功能描述

### 单篇文章下载

实现单篇微信公众号文章的下载，支持多种下载模式，可以控制是否下载图片、音视频等资源。

```python
def download_article(self, url, mode=4):
    """下载单篇文章
    
    Args:
        url (str): 文章URL
        mode (int): 下载模式，有以下选项：
            1: 返回HTML源码，不下载图片
            2: 返回HTML源码，下载图片但不替换路径
            3: 返回HTML源码，下载图片且替换路径
            4: 保存HTML源码，下载图片且替换路径
            5: 保存HTML源码，下载图片且替换路径，并下载视频与音频
            6: 返回HTML源码，不下载图片，替换 src 和图片为 web
            
    Returns:
        str: HTML内容或操作结果消息
    """
```

#### 实现方式

1. 检查是否需要验证
2. 添加随机延迟避免触发反爬机制
3. 从URL中提取文件名作为保存文件名
4. 根据下载模式调用Url2Html的run方法
5. 检查返回结果，处理验证情况
6. 若保存文件，返回成功消息；否则返回HTML内容

### 批量文章下载

实现批量下载公众号文章功能，支持多种输出格式，包含测试批次下载、断点续传策略。

```python
def download_articles(self, nickname, format="html"):
    """批量下载公众号文章
    
    Args:
        nickname (str): 公众号昵称
        format (str): 下载格式，可选"html"、"pdf"或"markdown"
        
    Returns:
        str: 操作结果消息
    """
```

#### 实现方式

1. 获取公众号所有文章链接
2. 创建公众号专用目录
3. 先下载少量测试批次，检查成功率
4. 根据测试批次结果决定是否继续下载
5. 按批次下载剩余文章，每批次间添加额外延迟
6. 根据不同格式调用不同的转换工具
7. 处理下载过程中的验证和错误情况

## 示例代码

### 单篇文章下载示例

```python
# 下载并保存为HTML
result = scrapper.download_article("https://mp.weixin.qq.com/s/example-url")
print(result)  # 输出: "文章已下载至: ./downloads/filename.html"

# 获取文章HTML内容不保存
html_content = scrapper.download_article("https://mp.weixin.qq.com/s/example-url", mode=1)
```

### 批量下载示例

```python
# 批量下载为HTML
result = scrapper.download_articles("TechDaily")
print(result)  # 输出: "批量下载完成: 共30篇文章，成功28篇，保存在 ./downloads/TechDaily"

# 批量下载为PDF
pdf_result = scrapper.download_articles("TechDaily", format="pdf")

# 批量下载为Markdown
md_result = scrapper.download_articles("TechDaily", format="markdown")
```

## 异常处理

模块包含以下异常处理策略:

1. **验证处理**: 检测"当前环境异常"提示，自动打开浏览器引导用户完成验证
2. **重试机制**: 获取文章链接失败时自动重试，最多3次
3. **测试批次**: 先下载少量文章测试成功率，避免整体失败
4. **断点续传**: 支持下载中断后继续下载
5. **频率限制处理**: 检测到频率限制时增加等待时间
