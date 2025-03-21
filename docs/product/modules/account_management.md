# 公众号管理模块

## 功能描述

公众号管理模块让您能够轻松获取和管理微信公众号的信息和文章。通过该模块，您可以查看公众号的基本资料、浏览文章列表，并进行相关操作。

### 公众号信息查询

本模块允许您：
- 通过昵称搜索和识别公众号
- 获取公众号的基本资料（名称、简介、认证信息等）
- 确认公众号是否存在及其可访问性

### 文章管理功能

本模块提供：
- 获取公众号的完整文章列表
- 按发布时间查看文章分布
- 获取单篇文章的详细信息（标题、作者、日期等）
- 文章预览和选择性下载

## 使用指南

### 查询公众号信息

要获取公众号的基本信息，可以使用命令行：

```bash
wechat-scrapper account --nickname "公众号名称" --config config.json
```

输出示例：
