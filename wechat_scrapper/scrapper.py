from wechatarticles import Url2Html, ArticlesInfo, PublicAccountsWeb


class WechatScrapper:
    def __init__(self, appmsg_token, cookie, proxies={"http": None, "https": None}):
        self.articles_info = ArticlesInfo(appmsg_token, cookie, proxies)
        self.url2html = Url2Html()
        self.public_accounts_web = PublicAccountsWeb(cookie, appmsg_token, proxies)

    def download_article(self, url, mode=4):
        return self.url2html.run(url, mode)

    def get_article_info(self, url):
        return self.articles_info.content(url)

    def get_public_account_info(self, nickname):
        return self.public_accounts_web.official_info(nickname)
