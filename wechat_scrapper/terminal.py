import cmd
from .scrapper import WechatScrapper


class WechatTerminal(cmd.Cmd):
    intro = (
        "Welcome to the Wechat Scrapper terminal. Type help or ? to list commands.\n"
    )
    prompt = "(wechat) "

    def __init__(self):
        super().__init__()
        self.scrapper = WechatScrapper(
            appmsg_token="your_appmsg_token", cookie="your_cookie"
        )

    def do_download(self, arg):
        "Download an article: download <url> <mode>"
        args = arg.split()
        if len(args) != 2:
            print("Usage: download <url> <mode>")
            return
        url, mode = args
        result = self.scrapper.download_article(url, int(mode))
        print(result)

    def do_info(self, arg):
        "Get article info: info <url>"
        result = self.scrapper.get_article_info(arg)
        print(result)

    def do_account(self, arg):
        "Get public account info: account <nickname>"
        result = self.scrapper.get_public_account_info(arg)
        print(result)

    def do_exit(self, arg):
        "Exit the terminal"
        print("Goodbye!")
        return True


if __name__ == "__main__":
    WechatTerminal().cmdloop()
