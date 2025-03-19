# 工具功能模块

## 功能描述

工具功能模块提供了一系列实用功能，帮助您更高效地管理和处理微信公众号内容。这些工具功能既可以与其他模块协同工作，也可以作为独立功能使用。

### 文件和路径管理

本模块提供：
- 自动创建输出目录结构
- 文件名合法化处理，移除非法字符
- 文件路径优化，支持长路径
- 防止文件名冲突的自动重命名

### 资源本地化

本模块助您实现资源本地保存：
- 图片资源下载和存储
- 音频和视频文件的处理
- 样式表和脚本的本地化
- 资源链接的替换

### 功能辅助工具

还包括一系列辅助功能：
- 日期和时间戳转换
- 请求头生成和管理
- 内容类型检测和处理
- 错误处理和日志记录

## 使用指南

工具功能模块的大多数功能在其他模块中自动使用，但部分功能可以直接调用。

### 文件名处理

如果您需要处理可能包含非法字符的文件名：

```python
from wechat_scrapper.utils import sanitize_filename

original_name = "微信文章:《如何学习?》(推荐)"
safe_name = sanitize_filename(original_name)
print(safe_name)  # 输出: 微信文章《如何学习》(推荐)
```

### 时间戳转换

转换微信文章的时间戳为可读格式：

```python
from wechat_scrapper.utils import format_timestamp

timestamp = 1647320400  # 微信文章时间戳
date_string = format_timestamp(timestamp)
print(date_string)  # 输出: 2022-03-15
```

### 目录管理

创建或确保目录存在：

```python
from wechat_scrapper.utils import ensure_dir

output_path = "./downloads/公众号名称/2023年文章"
ensure_dir(output_path)
print(f"目录已创建: {output_path}")
```

## 实用技巧

### 自定义输出文件名

在下载时，您可以控制输出文件的命名格式：

```bash
# 使用自定义文件名格式
wechat-scrapper download --url "https://mp.weixin.qq.com/s/example" --output-format "[{date}]{title}" --config config.json
```

### 资源文件管理

控制资源文件的保存方式：

```bash
# 指定资源保存选项
wechat-scrapper download --url "https://mp.weixin.qq.com/s/example" --resources-dir "resources" --save-images true --save-videos true --config config.json
```

### 批量文件处理

处理已下载的文件集合：

```python
import os
from wechat_scrapper.utils import sanitize_filename, ensure_dir

# 批量重命名文件
def batch_rename(directory, prefix="文章-"):
    ensure_dir(directory)
    files = os.listdir(directory)
    for file in files:
        if file.endswith('.html'):
            new_name = sanitize_filename(prefix + file)
            os.rename(os.path.join(directory, file), 
                     os.path.join(directory, new_name))
            print(f"重命名: {file} -> {new_name}")

# 使用示例
batch_rename("./downloads/公众号名称", "技术文章-")
```

## 最佳实践

1. **文件命名策略**：
   - 使用一致的命名规则，如"[日期]-[标题]"
   - 避免使用过长的文件名
   - 考虑添加分类前缀，如"技术-"、"行业-"

2. **资源管理**：
   - 对于重要文章，总是选择保存所有资源
   - 为每个公众号创建单独的资源目录
   - 定期整理和备份资源文件

3. **错误处理**：
   - 保持错误日志以便排查问题
   - 出现资源下载失败时，记录URL以便后续手动下载
   - 使用断点续传功能恢复中断的下载

4. **空间优化**：
   - 定期检查下载内容，删除不再需要的文件
   - 考虑压缩旧文章的资源文件
   - 对相同资源使用硬链接减少重复

5. **备份策略**：
   - 定期将重要内容备份到云存储
   - 使用版本控制系统（如Git）管理文本内容
   - 创建内容索引，方便快速查找特定文章
