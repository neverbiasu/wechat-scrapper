from wechatarticles import Url2Html, ArticlesInfo, PublicAccountsWeb
from .utils import Url2Pdf, Html2Markdown


class WechatScrapper:
    def __init__(self, appmsg_token, cookie, proxies={"http": None, "https": None}):
        self.articles_info = ArticlesInfo(appmsg_token, cookie, proxies)
        self.url2html = Url2Html()
        self.public_accounts_web = PublicAccountsWeb(cookie, appmsg_token, proxies)
        self.url2pdf = Url2Pdf(wkhtmltopdf_path="path_to_wkhtmltopdf")
        self.html2md = Html2Markdown()

    def download(self, url=None, nickname=None, mode=4, format="html"):
        if url:
            return self.download_article(url, mode)
        elif nickname:
            return self.download_articles(nickname, format)

    def download_article(self, url, mode=4):
        return self.url2html.run(url, mode)

    def get_article_info(self, url):
        return self.articles_info.content(url)

    def get_public_account_info(self, nickname):
        return self.public_accounts_web.official_info(nickname)

    def get_all_article_urls(self, nickname):
        urls = []
        begin = 0
        while True:
            articles = self.public_accounts_web.get_urls(nickname, begin=begin, count=5)
            if not articles:
                break
            urls.extend([article['link'] for article in articles])
            begin += 5
        return urls

    def download_articles(self, nickname, format="html"):
        urls = self.get_all_article_urls(nickname)
        for url in urls:
            if format == "html":
                self.download_article(url, mode=4)
            elif format == "pdf":
                self.url2pdf.url_to_pdf(url, title=url.split('/')[-1])
            elif format == "markdown":
                html_content = self.download_article(url, mode=1)
                self.html2md.convert(html_content, title=url.split('/')[-1])
