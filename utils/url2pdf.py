# coding: utf-8
import time
import pdfkit

"""
目前已失效，不再维护

Centos7下中文字体
yum install -y fontconfig ttmkfdir mkfontscale
上传windows的simsun.ttc，至/usr/share/fonts下
"""


class Url2Pdf:
    def __init__(self, wkhtmltopdf_path):
        self.config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        self.options = {
            "page-size": "A4",  # 默认是A4 Letter  etc
            # 'margin-top':'0.05in',   #顶部间隔
            # 'margin-right':'2in',   #右侧间隔
            # 'margin-bottom':'0.05in',   #底部间隔
            # 'margin-left':'2in',   #左侧间隔
            "encoding": "UTF-8",  # 文本个数
            "dpi": "96",
            "image-dpi": "600",
            "image-quality": "94",
            "footer-font-size": "80",  # 字体大小
            "no-outline": None,
            "zoom": 2,  # 网页放大/缩小倍数
        }

    def url_to_pdf(self, url, title):
        pdfkit.from_url(
            url, "{}.pdf".format(title), configuration=self.config, options=self.options
        )


if __name__ == "__main__":
    wkhtmltopdf_path = r"D:\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    url = "http://example.com"
    title = "example"

    url2pdf = Url2Pdf(wkhtmltopdf_path)
    url2pdf.url_to_pdf(url, title)
