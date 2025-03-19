# 配置管理模块

## 功能描述

配置管理模块让您可以方便地保存和重用工具设置，避免每次使用时重复输入参数。该模块特别适合需要频繁使用本工具的用户，可大大提高工作效率。

### 配置信息管理

本模块允许您：
- 将认证信息（cookie和token）保存到配置文件
- 存储常用参数如默认输出目录、下载模式等
- 管理多个不同的配置文件，适应不同使用场景

### 参数设置功能

通过配置文件，您可以设置：
- 认证信息（必需）：cookie和token
- 下载参数：延迟时间、批次大小、下载模式等
- 输出选项：默认保存位置、默认格式等
- 自定义用户代理（User-Agent）

## 使用指南

### 创建配置文件

配置文件使用JSON格式。创建一个名为`config.json`的文件，内容如下：

```json
{
  "cookie": "您的cookie值",
  "token": "您的token值",
  "output_dir": "./downloads",
  "delay_min": 5,
  "delay_max": 10,
  "batch_size": 3,
  "batch_delay": 20,
  "user_agent": "Mozilla/5.0 ..."
}
```

只有cookie和token是必须的，其他参数可以省略。

### 使用配置文件

命令行方式：

```bash
# 使用配置文件下载文章
wechat-scrapper download --url "https://mp.weixin.qq.com/s/example-url" --config config.json

# 使用配置文件批量下载，但覆盖部分参数
wechat-scrapper download --nickname "公众号名称" --config config.json --format pdf --delay-min 8
```

图形界面方式：
1. 启动GUI时指定配置文件：`wechat-scrapper gui --config config.json`
2. 认证信息将自动填充到界面中

### 管理多个配置文件

您可以为不同的用途创建多个配置文件：

```bash
# 使用不同的配置文件
wechat-scrapper download --nickname "公众号1" --config work.json
wechat-scrapper download --nickname "公众号2" --config personal.json
```

## 安全注意事项

1. **保护您的配置文件**：
   - 配置文件包含敏感认证信息
   - 不要将其放在公共目录或上传到版本控制系统
   - 考虑设置适当的文件权限（如在Linux上使用`chmod 600`）

2. **定期更新认证信息**：
   - cookie和token会定期失效
   - 保持配置文件中的认证信息更新
   - 如遇验证问题，优先检查认证信息是否过期

## 最佳实践

1. **配置文件组织**：
   - 使用有意义的文件名区分不同配置
   - 在配置文件中添加注释（JSON注释格式：在值中使用字符串形式）

2. **参数优化**：
   - 根据您的网络情况调整延迟参数
   - 对大型公众号，增加批次延迟减少被封风险
   - 保存常用的输出目录，形成一致的文件组织结构

3. **结合其他模块使用**：
   - 配置文件可简化所有其他模块的使用
   - 特别适合命令行脚本和自动化任务
