# 反爬虫策略模块

## 模块概述

反爬虫策略模块提供了一系列方法和策略，用于避免触发微信平台的反爬虫机制。该模块实现了请求延迟、请求头管理、访问频率控制等功能，以模拟正常用户行为，提高爬取成功率。

## 接口定义

### AntiCrawlerHandler 类

```python
class AntiCrawlerHandler:
    def __init__(self, min_delay=3, max_delay=8, batch_size=3, batch_delay=15):
        """初始化反爬虫处理器
        
        Args:
            min_delay (float): 请求之间的最小延迟(秒)
            max_delay (float): 请求之间的最大延迟(秒)
            batch_size (int): 批处理大小，每批处理多少请求后增加额外延迟
            batch_delay (float): 批次之间的额外延迟(秒)
        """
        pass
        
    def add_random_delay(self):
        """添加随机延迟，避免固定间隔请求
        
        Returns:
            float: 实际延迟的秒数
        """
        pass
        
    def batch_delay(self):
        """在批次之间添加额外延迟
        
        Returns:
            float: 实际延迟的秒数
        """
        pass
        
    def get_headers(self, referer=None):
        """获取随机化的请求头
        
        Args:
            referer (str, optional): 引用页URL
            
        Returns:
            dict: HTTP请求头字典
        """
        pass
        
    def handle_rate_limit(self, error_message):
        """处理频率限制错误，增加等待时间
        
        Args:
            error_message (str): 错误信息
            
        Returns:
            float: 建议的等待时间(秒)
        """
        pass
        
    def adjust_strategy(self, success_rate):
        """根据成功率动态调整策略
        
        Args:
            success_rate (float): 请求成功率(0-1)
            
        Returns:
            dict: 调整后的策略参数
        """
        pass
```

## 实现方式

### 延迟控制

1. 使用`random.uniform(min_delay, max_delay)`生成随机延迟时间
2. 批量请求时，每`batch_size`个请求增加额外的批次延迟
3. 遇到错误时动态增加延迟时间
4. 通过友好的日志输出让用户了解等待原因和时间

### 请求头管理

1. 维护一个常见User-Agent列表，随机选择
2. 根据需要设置Referer、Accept等HTTP头
3. 保持一定的请求头一致性，避免频繁变化

### 动态策略调整

1. 记录请求成功率
2. 根据成功率动态调整延迟参数
3. 低成功率时采取更保守的策略
4. 高成功率时可适度减少延迟，提高效率

## 使用示例

### 基本延迟应用

```python
# 创建反爬处理器
anti_crawler = AntiCrawlerHandler(min_delay=3, max_delay=8)

# 在请求之间添加随机延迟
for url in urls:
    anti_crawler.add_random_delay()
    response = requests.get(url, headers=anti_crawler.get_headers())
```

### 批量请求控制

```python
# 设置批量处理参数
anti_crawler = AntiCrawlerHandler(batch_size=5, batch_delay=20)

# 批量下载文章
for i, url in enumerate(urls):
    response = requests.get(url, headers=anti_crawler.get_headers())
    
    # 每5个请求后增加额外延迟
    if (i + 1) % anti_crawler.batch_size == 0:
        delay_time = anti_crawler.batch_delay()
        print(f"批次延迟: {delay_time:.2f}秒")
```

### 错误处理和策略调整

```python
# 错误处理
try:
    response = requests.get(url)
except Exception as e:
    wait_time = anti_crawler.handle_rate_limit(str(e))
    print(f"频率限制，等待 {wait_time:.2f}秒后重试")
    time.sleep(wait_time)
    
# 根据成功率调整策略
success_count = 8
total_count = 10
success_rate = success_count / total_count
new_strategy = anti_crawler.adjust_strategy(success_rate)
print(f"调整策略: {new_strategy}")
```

## 最佳实践

1. **渐进式延迟**: 初始使用较短延迟，发现问题时逐渐增加
2. **监控成功率**: 持续监控请求成功率，低于阈值时主动调整策略
3. **分时段爬取**: 避免在固定时间段大量爬取
4. **设置上限**: 限制单次会话的最大请求次数
