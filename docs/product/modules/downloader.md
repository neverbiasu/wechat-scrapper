# 下载模块

## 功能描述

下载模块是微信公众号爬虫工具的核心功能模块，提供了单篇文章下载和批量文章下载的功能，支持多种下载模式和格式选择。

### 单篇文章下载

通过提供文章URL，可以下载单篇微信公众号文章：
- 支持多种下载模式，控制是否下载图片、视频等资源
- 自动处理文章资源本地化
- 支持HTML、PDF和Markdown格式输出

### 批量文章下载

通过提供公众号昵称，可以批量下载该公众号的所有文章：
- 自动获取公众号所有文章列表
- 智能控制下载速度，减少被封风险
- 支持断点续传，下载中断后可继续
- 支持测试批次下载，验证成功率

## 使用指南

### 下载单篇文章

命令行方式：

```bash
# 基本用法（HTML格式）
wechat-scrapper download --url "https://mp.weixin.qq.com/s/example-url" --config config.json

# 指定下载模式（5表示下载图片、视频和音频）
wechat-scrapper download --url "https://mp.weixin.qq.com/s/example-url" --mode 5 --config config.json
```

图形界面方式：
1. 启动GUI：`wechat-scrapper gui`
2. 设置认证信息
3. 在"URL或昵称"输入框中粘贴文章链接
4. 在"模式"输入框中设置下载模式（默认为4）
5. 点击"下载文章"按钮

### 批量下载文章

命令行方式：

```bash
# HTML格式下载
wechat-scrapper download --nickname "公众号昵称" --config config.json

# PDF格式下载
wechat-scrapper download --nickname "公众号昵称" --format pdf --config config.json

# Markdown格式下载
wechat-scrapper download --nickname "公众号昵称" --format markdown --config config.json
```

图形界面方式：
1. 启动GUI：`wechat-scrapper gui`
2. 设置认证信息
3. 在"URL或昵称"输入框中输入公众号昵称
4. 在"格式"下拉菜单中选择下载格式
5. 点击"批量下载"按钮

## 下载模式说明

| 模式 | 描述                                               |
| ---- | -------------------------------------------------- |
| 1    | 返回HTML源码，不下载图片                           |
| 2    | 返回HTML源码，下载图片但不替换路径                 |
| 3    | 返回HTML源码，下载图片且替换路径                   |
| 4    | 保存HTML源码，下载图片且替换路径（默认）           |
| 5    | 保存HTML源码，下载图片且替换路径，并下载视频与音频 |
| 6    | 返回HTML源码，不下载图片，替换src和图片为web       |

## 最佳实践

1. **渐进式批量下载**：首次使用时，先下载少量文章测试认证是否有效
2. **合理设置延迟**：对于大量文章，增加延迟减少被封风险
   ```bash
   wechat-scrapper download --nickname "公众号昵称" --delay-min 8 --delay-max 15 --batch-delay 30
   ```
3. **分批处理**：文章数量较多时，分批进行下载
4. **选择合适的格式**：
   - HTML格式：保留完整排版和样式
   - PDF格式：适合分享和存档
   - Markdown格式：适合内容编辑和二次加工
```

```markdown
<!-- filepath: c:\Users\kcloud\workspace\wechat-scrapper\docs\product\modules\converter.md -->
# 格式转换模块

## 功能描述

格式转换模块负责将微信公众号文章转换为不同格式，满足用户在不同场景下的需求。当前支持三种主要格式：HTML、PDF和Markdown。

### HTML格式

HTML格式保留了文章的原始排版和样式，是最接近原文的存储方式：
- 完整保留原文的排版和样式
- 本地化图片资源，避免链接失效
- 支持完整查看文章内容

### PDF格式

PDF格式提供了标准的文档格式，便于阅读、打印和分享：
- 固定的文档格式，在不同设备上显示一致
- 适合打印和长期存档
- 便于分享给不使用本工具的人阅读

### Markdown格式

Markdown格式提供了轻量级的文本格式，便于编辑和内容再利用：
- 纯文本格式，易于编辑和修改
- 保留基本的格式如标题、列表、链接等
- 便于内容提取和二次创作

## 使用指南

### 命令行转换

在下载时指定格式：

```bash
# 下载为HTML格式（默认）
wechat-scrapper download --nickname "公众号昵称" --format html --config config.json

# 下载为PDF格式
wechat-scrapper download --nickname "公众号昵称" --format pdf --config config.json

# 下载为Markdown格式
wechat-scrapper download --nickname "公众号昵称" --format markdown --config config.json
```

### 图形界面转换

1. 启动GUI：`wechat-scrapper gui`
2. 设置认证信息
3. 在"URL或昵称"输入框中输入公众号昵称
4. 从"格式"下拉菜单中选择所需格式
5. 点击"批量下载"按钮

### 已下载内容的格式转换

目前工具不直接支持已下载内容的格式转换。如需将已下载的HTML转换为PDF，可以：
- 使用浏览器打开HTML文件，通过"打印"功能另存为PDF
- 使用第三方HTML到PDF转换工具

## 格式特性对比

| 特性           | HTML  | PDF   | Markdown |
| -------------- | ----- | ----- | -------- |
| 保留原始排版   | ★★★★★ | ★★★★☆ | ★★☆☆☆    |
| 图片资源保存   | ★★★★★ | ★★★★☆ | ★★★☆☆    |
| 文件大小       | 较大  | 中等  | 较小     |
| 编辑难度       | 中等  | 困难  | 简单     |
| 分享便捷性     | 中等  | 高    | 低       |
| 长期存档适用性 | 高    | 高    | 中等     |

## 最佳实践

1. **HTML格式**：当您需要完整保留原文样式和排版时使用
2. **PDF格式**：当您需要分享或打印文章时使用
3. **Markdown格式**：当您需要对文章内容进行编辑或内容提取时使用
4. **多格式保存**：对于重要文章，可以同时保存多种格式以适应不同场景
```

```markdown
<!-- filepath: c:\Users\kcloud\workspace\wechat-scrapper\docs\product\modules\interface.md -->
# 用户界面模块

## 功能描述

用户界面模块提供了两种交互方式：命令行界面(CLI)和图形用户界面(GUI)，满足不同用户的使用习惯和需求。

### 命令行界面

命令行界面提供了全面而灵活的功能控制：
- 支持所有工具功能的完整参数设置
- 适合脚本集成和自动化操作
- 提供详细的操作输出和错误信息

### 图形用户界面

图形用户界面提供了直观易用的操作体验：
- 无需记忆命令参数
- 直观的表单填写和按钮操作
- 实时显示操作结果和日志
- 适合不熟悉命令行的用户

## 使用指南

### 命令行界面使用

基本格式：
```bash
wechat-scrapper <操作> [选项]
```

支持的操作：
- `download`: 下载文章或批量下载公众号文章
- `info`: 获取文章信息
- `account`: 获取公众号信息
- `gui`: 启动图形用户界面

常用示例：

```bash
# 下载单篇文章
wechat-scrapper download --url "https://mp.weixin.qq.com/s/example-url" --cookie "..." --token "..."

# 批量下载公众号文章为PDF
wechat-scrapper download --nickname "公众号名称" --format pdf --config config.json

# 获取文章信息
wechat-scrapper info --url "https://mp.weixin.qq.com/s/example-url" --config config.json

# 获取公众号信息
wechat-scrapper account --nickname "公众号名称" --config config.json

# 启动图形界面
wechat-scrapper gui
```

### 图形界面使用

启动图形界面：
```bash
wechat-scrapper gui
# 或使用预设凭据启动
wechat-scrapper gui --config config.json
```

图形界面组成：
1. **认证信息区**：设置Token和Cookie
2. **输出设置区**：设置文件保存目录
3. **操作区**：输入URL或昵称，选择操作模式和格式
4. **结果显示区**：显示操作结果和日志

操作流程：
1. 填写Token和Cookie，点击"设置认证信息"
2. 设置输出目录（可选）
3. 在"URL或昵称"输入框中输入目标内容
4. 根据需要调整其他选项
5. 点击对应功能按钮执行操作
6. 在结果区查看操作日志和结果

## 命令行参数参考

### 全局选项

| 参数          | 说明                            | 默认值   |
| ------------- | ------------------------------- | -------- |
| --cookie      | 微信公众平台的cookie            | -        |
| --token       | 微信公众平台的token             | -        |
| --config      | 包含cookie和token的配置文件路径 | -        |
| --output-dir  | 输出目录                        | 当前目录 |
| --delay-min   | 请求之间的最小延迟时间(秒)      | 3.0      |
| --delay-max   | 请求之间的最大延迟时间(秒)      | 8.0      |
| --batch-size  | 每批下载的文章数量              | 3        |
| --batch-delay | 批次之间的延迟时间(秒)          | 15.0     |

### 下载操作选项

| 参数       | 说明                        | 默认值 |
| ---------- | --------------------------- | ------ |
| --url      | 要下载的文章URL             | -      |
| --nickname | 要下载的公众号昵称          | -      |
| --mode     | 下载模式(1-6)               | 4      |
| --format   | 下载格式(html/pdf/markdown) | html   |

## 最佳实践

1. **命令行高效使用**：
   - 创建配置文件存储认证信息
   - 使用上下键调用历史命令
   - 使用`--output-dir`指定输出目录

2. **图形界面高效使用**：
   - 首次设置认证后，可以保持界面开启进行多次操作
   - 使用"浏览"按钮选择输出目录，避免手动输入路径
   - 操作完成后查看结果区了解详细信息
```

## 2. 创建模块拆分文档

```markdown
<!-- filepath: c:\Users\kcloud\workspace\wechat-scrapper\docs\develop\module_splitting.md -->
# 微信公众号爬虫工具 - 模块拆分文档

## 模块拆分概述

本文档详细说明了微信公众号爬虫工具的模块拆分方案，包括拆分原则、各模块职责、依赖关系和实施计划。

### 拆分原则

1. **单一职责**：每个模块只负责一种明确的功能
2. **高内聚低耦合**：模块内部紧密关联，模块间尽量减少依赖
3. **依赖注入**：通过参数传递依赖，避免硬编码依赖关系
4. **接口稳定**：对外接口设计稳定，内部实现可随时优化

### 模块结构

```
wechat_scrapper/
├── auth/                # 认证模块
├── anti_crawler/        # 反爬虫策略模块
├── account/             # 公众号信息模块
├── articles/            # 文章信息模块
├── downloader/          # 下载功能模块
├── converter/           # 格式转换模块
├── utils/               # 工具函数模块
├── ui/                  # 用户界面模块
│   ├── cli.py           # 命令行界面
│   └── gui.py           # 图形用户界面
├── config/              # 配置管理模块
└── app.py               # 应用入口模块
