# 文章信息模块

## 模块概述

文章信息模块负责获取和处理微信公众号文章的元数据和内容。该模块提供了获取文章列表、文章详情、历史文章等功能，是下载功能的基础支持模块。

## 接口定义

### WechatArticles 类

```python
class WechatArticles:
    def __init__(self, auth_handler, anti_crawler_handler=None):
        """初始化文章信息处理器
        
        Args:
            auth_handler (WechatAuth): 认证处理器
            anti_crawler_handler (AntiCrawlerHandler, optional): 反爬虫处理器
        """
        pass
        
    def get_article_info(self, url):
        """获取单篇文章的详细信息
        
        Args:
            url (str): 文章链接
            
        Returns:
            dict: 文章信息字典，包含标题、作者、发布时间等
        """
        pass
        
    def get_account_articles(self, nickname=None, biz=None, offset=0, count=10):
        """获取公众号的文章列表
        
        Args:
            nickname (str, optional): 公众号昵称
            biz (str, optional): 公众号biz标识符(与nickname二选一)
            offset (int): 起始偏移量
            count (int): 获取数量
            
        Returns:
            list: 文章信息列表
        """
        pass
        
    def get_all_articles(self, nickname=None, biz=None):
        """获取公众号的所有文章
        
        Args:
            nickname (str, optional): 公众号昵称
            biz (str, optional): 公众号biz标识符(与nickname二选一)
            
        Returns:
            list: 所有文章信息列表
        """
        pass
        
    def extract_article_content(self, url):
        """提取文章正文内容
        
        Args:
            url (str): 文章链接
            
        Returns:
            dict: 包含标题、正文、图片等内容的字典
        """
        pass
```

## 依赖关系

本模块依赖于以下组件:

1. **auth模块**: 提供认证信息和验证功能
2. **anti_crawler模块**: 提供反爬策略支持
3. **account模块**: 获取公众号biz等信息

## 实现方式

### 文章信息获取

1. 调用微信文章API获取文章元数据
2. 解析响应内容，提取标题、作者、日期等信息
3. 对长文章支持分页获取

### 文章列表获取

1. 根据公众号昵称或biz获取其发布的文章列表
2. 支持分页获取，默认每页10篇
3. 可获取全部历史文章
4. 对获取过程进行错误重试和延迟控制

### 文章内容提取

1. 下载文章HTML内容
2. 使用BeautifulSoup解析提取正文
3. 识别和处理文章中的图片、链接和样式
4. 处理特殊内容如代码块、表格等

## 使用示例

### 获取文章信息

```python
from wechat_scrapper.auth import WechatAuth
from wechat_scrapper.anti_crawler import AntiCrawlerHandler
from wechat_scrapper.articles import WechatArticles

# 初始化组件
auth = WechatAuth(appmsg_token="...", cookie="...")
anti_crawler = AntiCrawlerHandler()
articles_handler = WechatArticles(auth, anti_crawler)

# 获取文章信息
article_info = articles_handler.get_article_info("https://mp.weixin.qq.com/s/example_url")
print(f"标题: {article_info['title']}")
print(f"作者: {article_info['author']}")
print(f"发布时间: {article_info['publish_time']}")
```

### 获取公众号文章列表

```python
# 获取最近10篇文章
recent_articles = articles_handler.get_account_articles(nickname="TechDaily", count=10)
for article in recent_articles:
    print(f"{article['title']} - {article['publish_time']}")

# 获取所有文章
all_articles = articles_handler.get_all_articles(nickname="TechDaily")
print(f"总共有 {len(all_articles)} 篇文章")
```

### 提取文章内容

```python
# 提取文章内容
content = articles_handler.extract_article_content("https://mp.weixin.qq.com/s/example_url")
print(f"标题: {content['title']}")
print(f"字数: {len(content['text'])}")
print(f"图片数: {len(content['images'])}")
```

## 异常处理

模块实现了以下异常处理机制:

1. **ArticleNotFoundError**: 文章不存在时抛出
2. **ContentExtractionError**: 内容提取失败时抛出
3. **RateLimitError**: 遇到频率限制时抛出
4. **RetryableError**: 可重试的临时错误
