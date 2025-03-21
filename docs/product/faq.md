# 微信公众号爬虫工具 - 常见问题解答

## 1. 安装与配置问题

### Q: 安装时报错 "ImportError: No module named 'xxx'"
**A:** 这通常是因为缺少依赖库。请尝试逐个安装依赖：
```bash
pip install requests beautifulsoup4 lxml wechatarticles html2text pyhtml2pdf
```

### Q: 如何在Linux/MacOS上安装?
**A:** 安装过程与Windows相同，但可能需要额外的依赖：
```bash
# 对于Debian/Ubuntu系统
sudo apt-get install python3-dev python3-pip
# 对于MacOS (使用Homebrew)
brew install python3
```
然后按照正常步骤安装工具。

### Q: 我可以在没有管理员权限的情况下安装吗?
**A:** 可以使用`--user`选项在用户空间安装：
```bash
pip install --user -r requirements.txt
pip install --user -e .
```

## 2. 认证问题

### Q: 如何找到cookie和token?
**A:**
1. 使用Chrome浏览器登录微信公众平台(https://mp.weixin.qq.com/)
2. 按F12打开开发者工具
3. 切换到Network标签
4. 刷新页面
5. 找到主页请求，在Headers中找到Cookie
6. 对于token，访问任一文章并查看请求参数中的appmsg_token值

### Q: cookie/token多久过期一次?
**A:** 一般情况下，微信平台的cookie可能会在几小时到几天内过期。如果遇到"需要验证"提示，通常说明认证信息已过期，需要重新获取。

### Q: 如何安全保存认证信息?
**A:** 
- 创建一个config.json文件存储认证信息
- 不要将此文件提交到版本控制系统
- 定期更新文件中的认证信息
- 设置适当的文件权限限制访问

## 3. 下载问题

### Q: 下载时提示"当前环境异常，请完成验证"
**A:** 这是微信反爬机制触发的验证码检查。请按照以下步骤操作：
1. 工具会尝试自动打开浏览器显示验证页面
2. 使用微信扫描验证码完成验证
3. 验证通过后，重新获取cookie
4. 使用新cookie重新运行命令

### Q: 批量下载经常中断，如何提高稳定性?
**A:** 可以尝试以下方法：
1. 增加请求间的延迟时间：`--delay-min 8 --delay-max 15`
2. 减小每批下载的文章数量：`--batch-size 3`
3. 增加批次之间的休息时间：`--batch-delay 30`
4. 分多次下载，每次只下载部分文章

### Q: 为什么有些图片没有被下载?
**A:** 可能的原因：
1. 图片已过期或被删除
2. 图片URL格式不标准，工具无法识别
3. 图片服务器限制了访问

尝试使用`--mode 5`参数，这会使用更全面的资源下载策略。

### Q: 如何提高批量下载的效率?
**A:** 目前版本不支持并行下载，因为过快的并行请求可能触发微信的反爬机制。未来版本会考虑添加受控的多线程支持。

## 4. 格式问题

### Q: PDF格式的文章显示不完整
**A:** 可能原因：
1. 文章包含特殊格式内容（如复杂表格或自定义样式）
2. PDF转换引擎限制

解决方法：可以先下载为HTML格式，然后使用专业PDF转换工具（如Chrome浏览器的打印功能）转换。

### Q: Markdown格式缺少原文的某些格式
**A:** Markdown格式转换会丢失一些复杂的HTML格式，这是正常现象。如果需要保留完整格式，建议使用HTML或PDF格式。

### Q: 在HTML格式中，某些样式看起来与网页不同
**A:** 这是因为我们只下载了必要的样式，并移除了一些微信专有的样式和脚本，以减小文件大小并提高兼容性。

## 5. 功能与兼容性问题

### Q: 工具支持下载视频内容吗?
**A:** 基本支持。当使用`--mode 5`参数时，工具会尝试下载文章中的视频和音频内容。但是由于微信视频的复杂保护机制，下载成功率可能不高。

### Q: 可以同时下载多个公众号的文章吗?
**A:** 当前版本需要分别执行命令下载不同公众号的文章。未来版本可能会增加批量处理多个公众号的功能。

### Q: 支持哪些Python版本?
**A:** 工具支持Python 3.6及以上版本。推荐使用Python 3.8或更高版本以获得最佳性能和兼容性。

## 6. 错误与调试

### Q: 如何获取更详细的错误信息?
**A:** 目前可以查看控制台输出的错误信息。未来版本会增加日志系统和`--debug`参数以提供更详细的调试信息。

### Q: "Connection refused"错误如何解决?
**A:** 这通常表示网络连接问题：
1. 检查您的网络连接
2. 确认微信公众平台可以正常访问
3. 如果使用代理，检查代理设置
4. 如果频繁出现，可能是IP被临时限制，请稍后再试

### Q: 如何报告bug?
**A:** 请在GitHub项目页面创建issue，并包含以下信息：
1. 错误信息和异常堆栈
2. 操作系统和Python版本
3. 运行的命令和参数
4. 问题描述和重现步骤
