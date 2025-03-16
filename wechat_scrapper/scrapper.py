from wechatarticles import Url2Html, ArticlesInfo, PublicAccountsWeb
from .utils import Url2Pdf, Html2Markdown
import os
import re
import time
import random
import webbrowser


class WechatScrapper:
    def __init__(
        self,
        appmsg_token,
        cookie,
        proxies={"http": None, "https": None},
        output_dir=None,
    ):
        self.articles_info = ArticlesInfo(appmsg_token, cookie, proxies)
        self.url2html = Url2Html()
        self.public_accounts_web = PublicAccountsWeb(cookie, appmsg_token, proxies)
        self.url2pdf = Url2Pdf()
        self.html2md = Html2Markdown()

        # 设置输出目录，默认为当前工作目录
        self.output_dir = output_dir if output_dir else os.getcwd()
        print(f"文件将保存到: {self.output_dir}")
        # 如果目录不存在，创建它
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # 添加爬取速度控制
        self.min_delay = 3  # 最小延迟秒数
        self.max_delay = 8  # 最大延迟秒数

        # 记录验证状态
        self.verification_needed = False
        self.verification_url = None

    def _add_random_delay(self):
        """添加随机延迟，避免触发反爬虫机制"""
        delay = random.uniform(self.min_delay, self.max_delay)
        print(f"等待 {delay:.2f} 秒...")
        time.sleep(delay)

    def _handle_verification(self, content, url=None):
        """处理微信的环境异常验证页面"""
        if "当前环境异常" in content or "完成验证" in content:
            self.verification_needed = True
            self.verification_url = url

            print("\n\n" + "=" * 50)
            print("检测到环境异常验证！请按照以下步骤操作：")
            print("1. 使用微信扫描验证码，或手动访问以下链接验证")
            if url:
                print(f"   链接: {url}")
                try:
                    # 尝试自动打开浏览器
                    webbrowser.open(url)
                    print("已尝试在浏览器中打开链接，请完成验证")
                except:
                    print("无法自动打开浏览器，请手动复制链接到浏览器打开")
            print("2. 完成验证后，更新cookie")
            print("3. 使用新的cookie重试")
            print("=" * 50 + "\n")

            return True
        return False

    def _sanitize_filename(self, filename):
        """清理文件名，移除不合法字符"""
        # 移除不允许的字符
        invalid_chars = r'[\\/*?:"<>|]'
        return re.sub(invalid_chars, '', filename)

    def download(self, url=None, nickname=None, mode=4, format="html"):
        if url:
            return self.download_article(url, mode)
        elif nickname:
            return self.download_articles(nickname, format)
        return "请提供 URL 或公众号昵称"

    def download_article(self, url, mode=4):
        print(f"正在下载文章: {url}")

        # 如果已知需要验证，先提示
        if self.verification_needed:
            print("环境需要验证，请先完成验证后再尝试下载")
            return "需要手动验证，请按照指示操作"

        # 添加随机延迟
        self._add_random_delay()

        # 从URL中提取文件名
        filename = self._sanitize_filename(url.split('/')[-1])
        output_path = os.path.join(self.output_dir, filename)

        # 修改请求头，模拟正常浏览器行为
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

        try:
            # 如果模式是4或5，会直接保存文件，返回的是状态消息
            if mode in [4, 5]:
                # 使用更好的自定义模式
                custom_kwargs = {
                    "account": os.path.basename(self.output_dir),
                    "headers": {
                        "User-Agent": user_agent,
                        "Referer": "https://mp.weixin.qq.com/",
                    },
                }
                result = self.url2html.run(url, mode, **custom_kwargs)

                # 检查是否需要验证
                if isinstance(result, str):
                    if self._handle_verification(result, url):
                        return "需要手动验证，请按照指示操作"
                    if "success" in result:
                        print(f"下载完成! 文件保存在: {self.output_dir}")
                        return f"文章已下载至: {self.output_dir}"

                return result
            # 否则返回HTML内容
            else:
                result = self.url2html.run(url, mode)
                # 检查是否需要验证
                if isinstance(result, str) and self._handle_verification(result, url):
                    return "需要手动验证，请按照指示操作"
                print("已获取HTML内容!")
                return result
        except Exception as e:
            error_msg = str(e)
            print(f"下载文章时出错: {error_msg}")

            # 检查是否包含验证相关错误
            if "验证" in error_msg or "访问频繁" in error_msg or "频繁" in error_msg:
                print("可能需要通过验证，请尝试在浏览器中访问该链接")
                self._handle_verification("当前环境异常", url)

            return f"下载失败: {error_msg}"

    def get_article_info(self, url):
        return self.articles_info.content(url)

    def get_public_account_info(self, nickname):
        return self.public_accounts_web.official_info(nickname)

    def get_all_article_urls(self, nickname):
        print(f"正在获取公众号 '{nickname}' 的所有文章链接...")
        urls = []
        begin = 0
        retry_count = 0
        max_retries = 3

        while True:
            try:
                # 添加延迟，减少被反爬机制检测的可能性
                self._add_random_delay()

                articles = self.public_accounts_web.get_urls(
                    nickname, begin=begin, count=5
                )
                if not articles:
                    break

                # 成功获取文章，重置重试计数
                retry_count = 0
                urls.extend([article['link'] for article in articles])
                begin += 5
                print(f"已获取 {len(urls)} 篇文章链接")

            except Exception as e:
                retry_count += 1
                if retry_count > max_retries:
                    print(f"获取文章链接失败，已重试 {max_retries} 次，退出: {e}")
                    break

                print(f"获取文章链接出错，正在重试 ({retry_count}/{max_retries}): {e}")
                # 遇到错误时增加延迟
                time.sleep(10)

                # 如果错误可能是由于访问频率过高导致，需要更长的等待时间
                if "频繁" in str(e) or "cookie" in str(e).lower():
                    print("检测到访问频率限制，等待时间增加...")
                    time.sleep(30)

        print(f"总共找到 {len(urls)} 篇文章")
        return urls

    def download_articles(self, nickname, format="html"):
        urls = self.get_all_article_urls(nickname)
        if not urls:
            print(f"未找到公众号 '{nickname}' 的任何文章")
            return f"未找到公众号 '{nickname}' 的任何文章"

        print(f"找到 {len(urls)} 篇文章，开始下载...")
        # 为该公众号创建一个专门的目录
        account_dir = os.path.join(self.output_dir, self._sanitize_filename(nickname))
        if not os.path.exists(account_dir):
            os.makedirs(account_dir)
        print(f"文件将保存到: {account_dir}")

        # 临时切换输出目录
        original_dir = self.output_dir
        self.output_dir = account_dir

        # 优化：一开始只下载一小部分文章，检查是否可以成功下载
        test_batch_size = 3
        test_urls = urls[: min(test_batch_size, len(urls))]
        remaining_urls = urls[min(test_batch_size, len(urls)) :]

        print(f"先尝试下载前 {len(test_urls)} 篇文章作为测试...")

        # 先尝试下载测试批次
        success_count = 0

        for index, url in enumerate(test_urls):
            filename = self._sanitize_filename(url.split('/')[-1])
            print(f"[{index+1}/{len(urls)}] 测试下载: {filename}")

            try:
                # 添加延迟，避免频率过高
                self._add_random_delay()

                if format == "html":
                    result = self.download_article(url, mode=4)
                    if "文章已下载" in str(result):
                        success_count += 1
                    if "需要手动验证" in str(result):
                        print("检测到需要验证，请先完成验证再继续下载")
                        # 恢复原始输出目录
                        self.output_dir = original_dir
                        return "下载中断，需要手动完成验证。请在微信中打开链接完成验证后，使用新的cookie重试。"
                elif format == "pdf":
                    output_path = os.path.join(account_dir, filename)
                    result = self.url2pdf.url_to_pdf(url, title=output_path)
                    if "PDF 已保存" in str(result):
                        success_count += 1
                    if "需要手动验证" in str(result):
                        print("检测到需要验证，请先完成验证再继续下载")
                        # 恢复原始输出目录
                        self.output_dir = original_dir
                        return "下载中断，需要手动完成验证。请在微信中打开链接完成验证后，使用新的cookie重试。"
                elif format == "markdown":
                    html_content = self.download_article(url, mode=1)
                    # 检查是否返回了验证提示
                    if isinstance(html_content, str) and "需要手动验证" in html_content:
                        print("检测到需要验证，请先完成验证再继续下载")
                        # 恢复原始输出目录
                        self.output_dir = original_dir
                        return "下载中断，需要手动完成验证。请在微信中打开链接完成验证后，使用新的cookie重试。"
                    output_path = os.path.join(account_dir, filename)
                    result = self.html2md.convert(html_content, title=output_path)
                    if "Markdown 已保存" in str(result):
                        success_count += 1

                print(f"[{index+1}/{len(urls)}] 下载完成: {result}")
            except Exception as e:
                error_msg = f"[{index+1}/{len(urls)}] 下载失败: {str(e)}"
                print(error_msg)

                if "验证" in str(e) or "频繁" in str(e):
                    print("检测到可能需要验证，请尝试在浏览器中访问以完成验证")
                    # 恢复原始输出目录
                    self.output_dir = original_dir
                    return "下载中断，需要手动完成验证。请在微信中打开链接完成验证后，使用新的cookie重试。"

        # 检查测试批次的成功率
        if success_count == 0 and len(test_urls) > 0:
            print("测试下载全部失败，可能需要验证或cookie已过期")
            # 恢复原始输出目录
            self.output_dir = original_dir
            return (
                "测试下载失败，请检查cookie是否有效或尝试在浏览器中访问文章以完成验证。"
            )

        # 如果测试批次有成功，继续下载剩余文章
        print(f"测试下载成功率: {success_count}/{len(test_urls)}")

        if len(remaining_urls) > 0:
            print(f"继续下载剩余的 {len(remaining_urls)} 篇文章...")

        results = []
        for index, url in enumerate(remaining_urls):
            filename = self._sanitize_filename(url.split('/')[-1])
            print(f"[{index+len(test_urls)+1}/{len(urls)}] 正在下载: {filename}")

            try:
                # 添加延迟，避免频率过高
                self._add_random_delay()

                if format == "html":
                    result = self.download_article(url, mode=4)
                    results.append(result)
                elif format == "pdf":
                    output_path = os.path.join(account_dir, filename)
                    result = self.url2pdf.url_to_pdf(url, title=output_path)
                    results.append(result)
                elif format == "markdown":
                    html_content = self.download_article(url, mode=1)
                    # 检查是否返回了验证提示
                    if isinstance(html_content, str) and "需要手动验证" in html_content:
                        results.append(html_content)
                        break
                    output_path = os.path.join(account_dir, filename)
                    result = self.html2md.convert(html_content, title=output_path)
                    results.append(result)

                print(f"[{index+len(test_urls)+1}/{len(urls)}] 下载完成")

                # 每下载一定数量的文章后增加额外休息时间，避免触发反爬
                if (index + 1) % 3 == 0:
                    extra_time = random.uniform(10, 20)
                    print(
                        f"已下载 {index + len(test_urls) + 1} 篇文章，休息 {extra_time:.2f} 秒..."
                    )
                    time.sleep(extra_time)

            except Exception as e:
                error_msg = f"[{index+len(test_urls)+1}/{len(urls)}] 下载失败: {str(e)}"
                print(error_msg)
                results.append(error_msg)

                # 如果出现错误，增加延迟时间
                if "频繁" in str(e):
                    print("检测到访问频率限制，增加等待时间...")
                    time.sleep(random.uniform(30, 60))

                # 如果错误可能与验证有关，中断下载
                if "验证" in str(e) or "请在微信客户端打开" in str(e):
                    print("检测到需要验证，中断下载")
                    break

        # 恢复原始输出目录
        self.output_dir = original_dir

        # 检查是否有验证需求
        if self.verification_needed or any("需要手动验证" in str(r) for r in results):
            return "下载中断，需要手动完成验证。请在微信中打开链接完成验证后，使用新的cookie重试。"

        total_success = success_count + len(
            [
                r
                for r in results
                if not str(r).startswith('[')
                and '失败' not in str(r)
                and '需要手动验证' not in str(r)
            ]
        )
        summary = f"批量下载完成: 共 {len(urls)} 篇文章，成功 {total_success} 篇，保存在 {account_dir}"
        print(summary)
        return summary
