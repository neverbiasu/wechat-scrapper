# 工具模块

## 模块概述

工具模块提供了一系列辅助功能，包括验证处理、反爬策略、文件名处理等，为其他模块提供支持。

## 接口定义

### 反爬延迟控制

```python
def _add_random_delay(self):
    """添加随机延迟，避免触发反爬虫机制"""
    pass
```

### 验证处理

```python
def _handle_verification(self, content, url=None):
    """处理微信的环境异常验证页面
    
    Args:
        content (str): 响应内容
        url (str, optional): 需要验证的URL
        
    Returns:
        bool: 是否需要验证
    """
    pass
```

### 文件名处理

```python
def _sanitize_filename(self, filename):
    """清理文件名，移除不合法字符
    
    Args:
        filename (str): 原始文件名
        
    Returns:
        str: 处理后的文件名
    """
    pass
```

## 实现方式

### 反爬延迟实现

1. 使用`random.uniform()`生成指定范围内的随机延迟时间
2. 使用`time.sleep()`执行延迟
3. 支持通过`min_delay`和`max_delay`属性调整延迟范围

### 验证处理实现

1. 检测内容中的关键词("当前环境异常"、"完成验证")
2. 设置验证状态标志
3. 尝试自动打开浏览器帮助用户完成验证
4. 提供清晰的验证指导信息

### 文件名处理实现

1. 使用正则表达式匹配不合法的文件名字符
2. 替换所有匹配到的字符
3. 适配Windows/Linux/MacOS文件系统规则

## 使用示例

### 延迟控制示例

```python
# 在WechatScrapper类中设置延迟范围
scrapper = WechatScrapper(...)
scrapper.min_delay = 5  # 最小延迟5秒
scrapper.max_delay = 10 # 最大延迟10秒

# 在下载过程中自动添加随机延迟
def download_with_delay():
    self._add_random_delay()
    # 执行下载操作
```

### 验证处理示例

```python
# 检查响应内容是否需要验证
html_content = requests.get(url).text
if self._handle_verification(html_content, url):
    return "需要手动验证，请按照指示操作"
    
# 在下载过程中检测验证需求
if self.verification_needed:
    print("环境需要验证，请先完成验证后再尝试下载")
    return "需要手动验证，请按照指示操作"
```

### 文件名处理示例

```python
# 清理文件名
original_filename = "微信文章: 「测试」内容/分享*?.md"
safe_filename = self._sanitize_filename(original_filename)
print(safe_filename)  # 输出: "微信文章 「测试」内容分享.md"
```

## 异常处理策略

1. **渐进式重试**: 出错时逐渐增加等待时间
2. **批次控制**: 批量操作时分批进行，减少风险
3. **验证自动检测**: 主动识别验证需求，避免无效请求
4. **路径安全检查**: 确保不会因文件名问题导致错误
