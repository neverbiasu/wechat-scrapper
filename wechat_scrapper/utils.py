import os
import requests
from bs4 import BeautifulSoup
import html2text
from pyhtml2pdf import converter
import tempfile
import random
import time
import webbrowser


class Url2Pdf:
    def __init__(self, *args, **kwargs):
        # 不需要外部依赖
        pass

    def url_to_pdf(self, url, title):
        """
        使用 pyhtml2pdf 将 URL 转换为 PDF
        """
        try:
            print(f"  正在获取HTML内容...")
            # 获取 HTML 内容，使用更好的请求头
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Referer": "https://mp.weixin.qq.com/",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            }

            # 添加随机延迟
            delay = random.uniform(1, 3)
            time.sleep(delay)

            response = requests.get(url, headers=headers)
            html_content = response.text

            # 检查是否需要验证
            if "当前环境异常" in html_content or "完成验证" in html_content:
                print("\n\n" + "=" * 50)
                print("检测到环境异常验证！请按照以下步骤操作：")
                print("1. 请用微信扫描验证码，或手动访问以下链接验证")
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
                return "需要手动验证，请按照指示操作"

            # 创建临时HTML文件
            print(f"  正在创建临时HTML文件...")
            with tempfile.NamedTemporaryFile(
                'w', suffix='.html', delete=False, encoding='utf-8'
            ) as temp_html:
                temp_html.write(html_content)
                temp_html_path = temp_html.name

            # 输出PDF文件路径
            if not title.endswith('.pdf'):
                pdf_file_path = f"{title}.pdf"
            else:
                pdf_file_path = title

            # 确保目录存在
            os.makedirs(os.path.dirname(os.path.abspath(pdf_file_path)), exist_ok=True)

            # 转换HTML为PDF
            print(f"  正在转换HTML为PDF...")
            converter.convert(temp_html_path, pdf_file_path)

            # 删除临时HTML文件
            print(f"  清理临时文件...")
            os.unlink(temp_html_path)

            return f"PDF 已保存为 {pdf_file_path}"
        except Exception as e:
            if "请在微信客户端打开" in str(e) or "当前环境异常" in str(e):
                print("\n检测到需要验证，请尝试在浏览器中访问该链接进行验证")
                try:
                    webbrowser.open(url)
                except:
                    pass
                return "需要手动验证，请按照指示操作"
            return f"生成PDF时出错: {str(e)}"


class Html2Markdown:
    def __init__(self):
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = False
        self.converter.ignore_images = False
        self.converter.unicode_snob = True
        self.converter.escape_snob = True

    def convert(self, html_content, title):
        """
        使用 html2text 将 HTML 转换为 Markdown
        """
        try:
            # 检查是否是字符串类型，不是则无法处理
            if not isinstance(html_content, str):
                return f"无法转换非文本内容为Markdown: {type(html_content)}"

            # 检查是否需要验证
            if "当前环境异常" in html_content or "完成验证" in html_content:
                print("\n\n检测到环境异常验证！请按照以下步骤操作：")
                print("1. 请用微信扫描验证码，或手动访问以下链接验证")
                print("2. 完成验证后，更新cookie")
                print("3. 使用新的cookie重试\n")
                return "需要手动验证，请按照指示操作"

            print(f"  正在解析HTML...")
            # 解析 HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # 提取正文内容
            body = soup.find('body') or soup

            # 转换为 Markdown
            print(f"  正在转换为Markdown...")
            markdown_content = self.converter.handle(str(body))

            # 确保文件路径有效
            if not title.endswith('.md'):
                md_file_path = f"{title}.md"
            else:
                md_file_path = title

            # 确保目录存在
            os.makedirs(os.path.dirname(os.path.abspath(md_file_path)), exist_ok=True)

            # 保存 Markdown 文件
            print(f"  正在保存Markdown文件...")
            with open(md_file_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            return f"Markdown 已保存为 {md_file_path}"
        except Exception as e:
            return f"转换为Markdown时出错: {str(e)}"
