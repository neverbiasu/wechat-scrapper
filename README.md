# Wechat Scrapper

Wechat Scrapper 是一个用于抓取微信公众号文章的工具，支持命令行和图形用户界面两种使用方式。

## 功能

- 下载微信公众号文章为 HTML 文件
- 获取微信公众号文章的信息
- 获取微信公众号的账号信息
- 批量下载微信公众号文章为 HTML、PDF 和 Markdown 文件

## 安装

```bash
git clone https://github.com/yourusername/wechat-scrapper.git
cd wechat-scrapper
pip install -r requirements.txt
```

## 使用

### 命令行

你需要提供 cookie 和 token 来使用此工具：

```bash
# 下载单篇文章
wechat-scrapper download --url <url> --mode <mode> --cookie <cookie> --token <token>

# 批量下载公众号文章
wechat-scrapper download --nickname <nickname> --format <format> --cookie <cookie> --token <token>

# 获取文章信息
wechat-scrapper info --url <url> --cookie <cookie> --token <token>

# 获取公众号信息
wechat-scrapper account --nickname <nickname> --cookie <cookie> --token <token>
```

### 使用配置文件

你也可以创建一个配置文件来存储 cookie 和 token：

```json
{
  "cookie": "your_cookie_here",
  "token": "your_token_here"
}
```

然后通过 `--config` 参数指定配置文件路径：

```bash
wechat-scrapper download --url <url> --mode <mode> --config config.json
```

### 图形用户界面

```bash
wechat-scrapper gui --cookie <cookie> --token <token>
# 或者使用配置文件
wechat-scrapper gui --config config.json
```

## 贡献

欢迎提交 issue 和 pull request 来贡献代码。

## 未来功能

以下是一些可以实现的功能：

- 支持多线程下载，提高下载速度
- 增加对微信公众号文章评论的抓取功能
- 增加对微信公众号文章阅读数和点赞数的抓取功能
- 支持更多的命令行参数和选项
- 增加对微信公众号文章的搜索功能
