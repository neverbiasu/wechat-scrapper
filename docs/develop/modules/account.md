# 公众号信息模块

## 模块概述

公众号信息模块负责获取和处理微信公众号的基本信息，包括公众号名称、简介、分类、认证信息等。该模块提供了识别公众号、查询公众号详情和获取公众号标识符等功能。

## 接口定义

### WechatAccount 类

```python
class WechatAccount:
    def __init__(self, auth_handler, anti_crawler_handler=None):
        """初始化公众号信息处理器
        
        Args:
            auth_handler (WechatAuth): 认证处理器
            anti_crawler_handler (AntiCrawlerHandler, optional): 反爬虫处理器
        """
        pass
        
    def get_account_info(self, nickname):
        """获取公众号基本信息
        
        Args:
            nickname (str): 公众号昵称
            
        Returns:
            dict: 公众号信息字典，包含名称、简介、头像URL等
        """
        pass
        
    def get_account_biz(self, nickname):
        """获取公众号的biz标识符
        
        Args:
            nickname (str): 公众号昵称
            
        Returns:
            str: 公众号biz标识符
        """
        pass
        
    def search_account(self, keyword):
        """搜索公众号
        
        Args:
            keyword (str): 搜索关键词
            
        Returns:
            list: 匹配的公众号列表
        """
        pass
        
    def check_exists(self, nickname):
        """检查公众号是否存在
        
        Args:
            nickname (str): 公众号昵称
            
        Returns:
            bool: 是否存在
        """
        pass
```

## 依赖关系

本模块依赖于以下组件:

1. **auth模块**: 提供认证信息和验证功能
2. **anti_crawler模块**: 提供反爬策略支持

## 实现方式

### 公众号信息获取

1. 通过微信公众平台搜索接口查询公众号
2. 解析返回的HTML或JSON内容，提取公众号信息
3. 缓存已查询的公众号信息，减少重复请求

### Biz标识符获取

1. 通过公众号主页或文章链接提取biz参数
2. biz参数是公众号的唯一标识符，后续用于获取文章列表
3. 实现多种提取方法，提高成功率

### 错误处理

1. 处理公众号不存在的情况
2. 处理需要验证的情况
3. 处理网络超时等异常

## 使用示例

### 获取公众号信息

```python
from wechat_scrapper.auth import WechatAuth
from wechat_scrapper.anti_crawler import AntiCrawlerHandler
from wechat_scrapper.account import WechatAccount

# 初始化组件
auth = WechatAuth(appmsg_token="...", cookie="...")
anti_crawler = AntiCrawlerHandler()
account_handler = WechatAccount(auth, anti_crawler)

# 获取公众号信息
account_info = account_handler.get_account_info("TechDaily")
print(account_info)
# 输出:
# {
#   "nickname": "TechDaily",
#   "description": "每日科技资讯...",
#   "avatar_url": "https://mmbiz.qpic.cn/...",
#   "authentication": "科技媒体",
#   "biz": "MzI5Mzg5NTcxMw=="
# }
```

### 搜索公众号

```python
# 搜索公众号
results = account_handler.search_account("科技")
for account in results:
    print(f"{account['nickname']} - {account['description']}")
```

### 检查公众号存在性

```python
# 检查公众号是否存在
if account_handler.check_exists("TechDaily"):
    print("公众号存在")
else:
    print("公众号不存在")
```

## 异常处理

模块实现了以下异常处理机制:

1. **NotFoundError**: 公众号不存在时抛出
2. **AuthError**: 认证失败时抛出
3. **RateLimitError**: 遇到频率限制时抛出
4. **NetworkError**: 网络问题时抛出
