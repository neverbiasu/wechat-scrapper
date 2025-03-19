# 核心模块

## 模块概述

核心模块实现了微信公众号爬虫工具的主要功能控制和协调，由`WechatScrapper`类提供统一接口，负责调度其他模块完成具体任务。

## 接口定义

### 主类：WechatScrapper

```python
class WechatScrapper:
    def __init__(self, appmsg_token, cookie, proxies={"http": None, "https": None}, output_dir=None):
        """初始化爬虫实例
        
        Args:
            appmsg_token (str): 微信公众平台的token
            cookie (str): 微信公众平台的cookie
            proxies (dict): 代理设置，默认无代理
            output_dir (str): 输出目录，默认为当前工作目录
        """
        pass
        
    def download(self, url=None, nickname=None, mode=4, format="html"):
        """下载单篇文章或批量下载公众号文章
        
        Args:
            url (str, optional): 文章URL
            nickname (str, optional): 公众号昵称
            mode (int): 下载模式
            format (str): 输出格式
            
        Returns:
            str: 操作结果信息
        """
        pass
        
    def get_article_info(self, url):
        """获取文章元信息
        
        Args:
            url (str): 文章URL
            
        Returns:
            dict: 文章信息字典
        """
        pass
        
    def get_public_account_info(self, nickname):
        """获取公众号信息
        
        Args:
            nickname (str): 公众号昵称
            
        Returns:
            dict: 公众号信息字典
        """
        pass
```

## 依赖关系

核心模块依赖于以下组件：

1. **ArticlesInfo**: 文章信息获取组件（来自wechatarticles库）
2. **Url2Html**: HTML下载组件（来自wechatarticles库）
3. **PublicAccountsWeb**: 公众号信息获取组件（来自wechatarticles库）
4. **Url2Pdf**: PDF转换工具（内部实现）
5. **Html2Markdown**: Markdown转换工具（内部实现）

## 使用示例

```python
from wechat_scrapper import WechatScrapper

# 初始化实例
scrapper = WechatScrapper(
    appmsg_token="your_token_here",
    cookie="your_cookie_here",
    output_dir="./downloads"
)

# 下载单篇文章
scrapper.download(url="https://mp.weixin.qq.com/s/example_url")

# 获取公众号信息
account_info = scrapper.get_public_account_info("TechDaily")
print(account_info)

# 批量下载为PDF
scrapper.download(nickname="TechDaily", format="pdf")
```
