# 反爬策略模块

## 功能描述

反爬策略模块提供了一系列智能技术，帮助您的爬取行为更接近于正常用户操作，有效减少被微信平台检测和限制的风险。该模块是保证下载稳定性和成功率的关键组件。

### 智能延迟控制

本模块提供：
- 随机化的请求延迟，避免机械化的固定间隔
- 批量请求时的智能休息策略
- 自动根据请求成功率调整延迟时间
- 遇到限制时的渐进式等待策略

### 模拟正常浏览行为

本模块模拟真实用户行为：
- 随机化的请求头信息
- 合理的请求顺序和模式
- 自适应的访问频率控制
- 验证检测和处理机制

## 使用指南

反爬策略模块大部分功能自动运行在后台，用户只需设置少量参数即可享受其保护。

### 设置请求延迟

通过命令行参数控制延迟时间：

```bash
# 设置请求延迟范围（3-8秒之间随机）
wechat-scrapper download --nickname "公众号名称" --delay-min 3 --delay-max 8 --config config.json
```

对于大型公众号或大量文章，建议增加延迟：

```bash
# 设置更保守的延迟策略
wechat-scrapper download --nickname "公众号名称" --delay-min 8 --delay-max 15 --config config.json
```

### 设置批次控制

批量下载时，可以控制批次大小和批次间的延迟：

```bash
# 每3篇文章为一批，批次间休息20秒
wechat-scrapper download --nickname "公众号名称" --batch-size 3 --batch-delay 20 --config config.json
```

### 通过配置文件设置

在配置文件中永久保存您的反爬策略设置：

```json
{
  "cookie": "您的cookie值",
  "token": "您的token值",
  "delay_min": 5,
  "delay_max": 12,
  "batch_size": 3,
  "batch_delay": 25,
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ..."
}
```

## 反爬验证处理

当触发微信平台的反爬验证机制时，工具会：

1. 自动检测验证需求
2. 提供清晰的验证指导信息
3. 尝试自动打开浏览器展示验证页面
4. 等待您完成验证后继续操作

验证提示示例：
