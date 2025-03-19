# 微信公众号爬虫工具 - API 参考文档

## 核心类参考

### WechatScrapper

微信公众号文章抓取核心类，整合了所有功能。

#### 初始化参数

```python
WechatScrapper(appmsg_token, cookie, proxies={"http": None, "https": None}, output_dir=None)
```

**参数说明**:
- `appmsg_token` (str): 微信公众平台的 token，用于身份认证
- `cookie` (str): 微信公众平台的 cookie，用于身份认证
- `proxies` (dict): 代理设置，默认不使用代理
- `output_dir` (str): 输出目录路径，默认为当前工作目录

**实例属性**:
- `articles_info`: 文章信息处理组件
- `url2html`: HTML 内容下载组件
- `public_accounts_web`: 公众号信息获取组件
- `url2pdf`: PDF 转换组件 
- `html2md`: Markdown 转换组件
- `min_delay`: 请求最小延迟秒数，默认 3 秒
- `max_delay`: 请求最大延迟秒数，默认 8 秒
- `verification_needed`: 是否需要验证的标志

**示例代码**:

```python
from wechat_scrapper import WechatScrapper

# 初始化爬虫实例
scrapper = WechatScrapper(
    appmsg_token="1234567890abcdefg", 
    cookie="wxuin=1234567890; wxsid=abcdefghijklmn",
    output_dir="./downloads"
)

# 设置更保守的延迟时间，减少被封风险
scrapper.min_delay = 5
scrapper.max_delay = 12
```

#### 公共方法

##### download

```python
download(url=None, nickname=None, mode=4, format="html")
```

**功能描述**: 下载单篇文章或批量下载公众号文章的统一接口。

**参数说明**:
- `url` (str, 可选): 文章链接，与 `nickname` 互斥
- `nickname` (str, 可选): 公众号昵称，与 `url` 互斥
- `mode` (int): 下载模式，默认为 4
  - `1`: 返回 HTML 源码，不下载图片
  - `2`: 返回 HTML 源码，下载图片但不替换路径
  - `3`: 返回 HTML 源码，下载图片且替换路径
  - `4`: 保存 HTML 源码，下载图片且替换路径
  - `5`: 保存 HTML 源码，下载图片且替换路径，并下载视频与音频
  - `6`: 返回 HTML 源码，不下载图片，替换 src 和图片为 web
- `format` (str): 批量下载的格式，可选 "html"、"pdf" 或 "markdown"

**返回值**: `str` 或 `dict` - 操作结果消息或内容

**示例代码**:

```python
# 下载单篇文章
result = scrapper.download(url="https://mp.weixin.qq.com/s/example-url")
print(result)  # 返回成功消息或 HTML 内容

# 批量下载公众号文章
result = scrapper.download(nickname="example-account", format="pdf")
print(result)  # 返回批量下载的结果消息
```

##### download_article

```python
download_article(url, mode=4)
```

**功能描述**: 下载单篇文章。

**参数说明**:
- `url` (str): 文章链接
- `mode` (int): 下载模式，同 `download` 方法

**返回值**: `str` - 操作结果消息或 HTML 内容

**示例代码**:

```python
# 下载文章并保存为 HTML（模式 4）
result = scrapper.download_article("https://mp.weixin.qq.com/s/example-url")
print(result)  # 例如: "文章已下载至: ./downloads"

# 获取文章 HTML 内容但不保存（模式 1）
html_content = scrapper.download_article("https://mp.weixin.qq.com/s/example-url", mode=1)
print(len(html_content))  # HTML 内容长度
```

##### download_articles

```python
download_articles(nickname, format="html")
```

**功能描述**: 批量下载公众号文章。

**参数说明**:
- `nickname` (str): 公众号昵称
- `format` (str): 下载格式，可选 "html"、"pdf" 或 "markdown"

**返回值**: `str` - 操作结果消息

**异常处理**:
- 处理验证需求和频率限制
- 检测下载测试批次的成功率
- 支持断点恢复

**示例代码**:

```python
# 批量下载为 HTML
result = scrapper.download_articles("example-account")
print(result)  # 例如: "批量下载完成: 共 30 篇文章，成功 28 篇，保存在 ./downloads/example-account"

# 批量下载为 PDF
pdf_result = scrapper.download_articles("example-account", format="pdf")
print(pdf_result)

# 批量下载为 Markdown
md_result = scrapper.download_articles("example-account", format="markdown")
print(md_result)
```

##### get_article_info

```python
get_article_info(url)
```

**功能描述**: 获取文章信息。

**参数说明**:
- `url` (str): 文章链接

**返回值**: `dict` - 文章信息字典，包含标题、作者等

**示例代码**:

```python
# 获取文章信息
info = scrapper.get_article_info("https://mp.weixin.qq.com/s/example-url")
print(info)  # 例如: {"title": "示例文章", "author": "作者名称", "publish_time": "2023-01-01"}
```

##### get_public_account_info

```python
get_public_account_info(nickname)
```

**功能描述**: 获取公众号信息。

**参数说明**:
- `nickname` (str): 公众号昵称

**返回值**: `dict` - 公众号信息字典

**示例代码**:

```python
# 获取公众号信息
account_info = scrapper.get_public_account_info("example-account")
print(account_info)  # 例如: {"name": "示例公众号", "description": "这是一个示例公众号", "logo_url": "https://..."}
```

##### get_all_article_urls

```python
get_all_article_urls(nickname)
```

**功能描述**: 获取公众号所有文章的链接。

**参数说明**:
- `nickname` (str): 公众号昵称

**返回值**: `list` - 文章链接列表

**示例代码**:

```python
# 获取所有文章链接
urls = scrapper.get_all_article_urls("example-account")
print(f"找到 {len(urls)} 篇文章")
for url in urls[:5]:  # 打印前 5 个链接
    print(url)
```

##### _add_random_delay

```python
_add_random_delay()
```

**功能描述**: 添加随机延迟，避免触发反爬虫机制（内部方法）。

**实现细节**:
- 使用 `random.uniform(self.min_delay, self.max_delay)` 生成随机延迟时间
- 使用 `time.sleep(delay)` 实现延迟

##### _handle_verification

```python
_handle_verification(content, url=None)
```

**功能描述**: 处理微信的环境异常验证页面（内部方法）。

**参数说明**:
- `content` (str): 响应内容
- `url` (str, 可选): 需要验证的 URL

**返回值**: `bool` - 是否需要验证

**实现细节**:
- 检测内容中是否包含 "当前环境异常" 或 "完成验证" 关键词
- 尝试自动打开浏览器帮助用户完成验证
- 向用户提供验证指导

##### _sanitize_filename

```python
_sanitize_filename(filename)
```

**功能描述**: 清理文件名，移除不合法字符（内部方法）。

**参数说明**:
- `filename` (str): 原始文件名

**返回值**: `str` - 处理后的文件名

**实现细节**:
- 使用正则表达式 `r'[\\/*?:"<>|]'` 移除 Windows 不支持的字符

## 工具类参考

### Url2Pdf

将 URL 转换为 PDF 文件。

#### 初始化

```python
Url2Pdf()
```

无需参数，内部使用 pyhtml2pdf。

#### url_to_pdf

```python
url_to_pdf(url, title)
```

**功能描述**: 将指定 URL 转换为 PDF 并保存

**参数说明**:
- `url` (str): 需要转换的 URL
- `title` (str): 保存的文件名（不包含扩展名）

**返回值**: `str` - 操作结果消息

**示例代码**:

```python
from wechat_scrapper.utils import Url2Pdf

# 初始化转换器
pdf_converter = Url2Pdf()

# 转换 URL 为 PDF
result = pdf_converter.url_to_pdf("https://example.com", "example_file")
print(result)  # 例如: "PDF 已保存为 example_file.pdf"
```

### Html2Markdown

将 HTML 内容转换为 Markdown 文件。

#### 初始化

```python
Html2Markdown()
```

内部使用 html2text 库进行转换。

#### convert

```python
convert(html_content, title)
```

**功能描述**: 将 HTML 内容转换为 Markdown 并保存

**参数说明**:
- `html_content` (str): HTML 内容
- `title` (str): 保存的文件名（不包含扩展名）

**返回值**: `str` - 操作结果消息

**示例代码**:

```python
from wechat_scrapper.utils import Html2Markdown

# 初始化转换器
md_converter = Html2Markdown()

# 转换 HTML 为 Markdown
html = "<html><body><h1>标题</h1><p>正文内容</p></body></html>"
result = md_converter.convert(html, "example_file")
print(result)  # 例如: "Markdown 已保存为 example_file.md"
```

## 命令行接口参考

### 基本用法

```bash
wechat-scrapper <action> [options]
```

### 操作类型

- `download`: 下载文章或批量下载公众号文章
- `info`: 获取文章信息
- `account`: 获取公众号信息
- `gui`: 启动图形用户界面

### 全局选项

| 参数          | 类型   | 默认值         | 描述                                |
| ------------- | ------ | -------------- | ----------------------------------- |
| --cookie      | string | -              | 微信公众平台的 cookie               |
| --token       | string | -              | 微信公众平台的 token                |
| --config      | string | -              | 包含 cookie 和 token 的配置文件路径 |
| --output-dir  | string | 当前目录       | 输出目录                            |
| --delay-min   | float  | 3.0            | 请求之间的最小延迟时间(秒)          |
| --delay-max   | float  | 8.0            | 请求之间的最大延迟时间(秒)          |
| --batch-size  | int    | 3              | 每批下载的文章数量                  |
| --batch-delay | float  | 15.0           | 批次之间的延迟时间(秒)              |
| --user-agent  | string | Mozilla/5.0... | 自定义 User-Agent 头                |

### 操作特定选项

#### download 操作

| 参数       | 类型   | 默认值 | 描述                         |
| ---------- | ------ | ------ | ---------------------------- |
| --url      | string | -      | 要下载的文章 URL             |
| --nickname | string | -      | 要下载的公众号昵称           |
| --mode     | int    | 4      | 下载模式 (1-6)               |
| --format   | string | html   | 下载格式 (html/pdf/markdown) |

#### info 操作

| 参数  | 类型   | 默认值 | 描述                 |
| ----- | ------ | ------ | -------------------- |
| --url | string | -      | 要获取信息的文章 URL |

#### account 操作

| 参数       | 类型   | 默认值 | 描述                   |
| ---------- | ------ | ------ | ---------------------- |
| --nickname | string | -      | 要获取信息的公众号昵称 |

#### gui 操作

无特定选项，使用全局选项设置初始值。

### 使用示例

```bash
# 下载单篇文章
wechat-scrapper download --url "https://mp.weixin.qq.com/s/example" --cookie "..." --token "..."

# 批量下载公众号文章为 PDF
wechat-scrapper download --nickname "公众号名称" --format pdf --config config.json --output-dir "./downloads"

# 使用自定义延迟设置批量下载
wechat-scrapper download --nickname "公众号名称" --delay-min 5 --delay-max 12 --batch-size 5 --batch-delay 30
```
