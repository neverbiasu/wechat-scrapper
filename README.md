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

```bash
wechat-scrapper download --url <url> --mode <mode>
wechat-scrapper download --nickname <nickname> --format <format>
wechat-scrapper info --url <url>
wechat-scrapper account --nickname <nickname>
```

### 图形用户界面

```bash
wechat-scrapper gui
```

## 配置

在使用前，需要配置 `appmsg_token` 和 `cookie`，可以在 `wechat_scrapper/scrapper.py` 文件中设置。

## 贡献

欢迎提交 issue 和 pull request 来贡献代码。

## 未来功能

以下是一些可以实现的功能：

- 支持多线程下载，提高下载速度
- 增加对微信公众号文章评论的抓取功能
- 增加对微信公众号文章阅读数和点赞数的抓取功能
- 支持更多的命令行参数和选项
- 增加对微信公众号文章的搜索功能
