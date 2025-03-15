# Wechat Scrapper

Wechat Scrapper 是一个用于抓取微信公众号文章的工具，支持命令行和终端两种使用方式。

## 安装

```bash
git clone https://github.com/yourusername/wechat-scrapper.git
cd wechat-scrapper
pip install -r requirements.txt
```

## 使用

### 命令行

```bash
wechat-scrapper-cli download <url> --mode <mode>
wechat-scrapper-cli info <url>
wechat-scrapper-cli account <nickname>
```

### 终端

```bash
wechat-scrapper-terminal
```

在终端中输入以下命令：

- `download <url> <mode>`: 下载文章
- `info <url>`: 获取文章信息
- `account <nickname>`: 获取公众号信息

## 配置

在使用前，需要配置 `appmsg_token` 和 `cookie`，可以在 `wechat_scrapper/scrapper.py` 文件中设置。

## 贡献

欢迎提交 issue 和 pull request 来贡献代码。
