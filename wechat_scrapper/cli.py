import argparse
from .scrapper import WechatScrapper
from .gui import WechatGUI


def main():
    parser = argparse.ArgumentParser(description="Wechat Scrapper CLI")
    parser.add_argument(
        "action",
        choices=["download", "info", "account", "gui"],
        help="Action to perform",
    )
    parser.add_argument(
        "--url",
        help="URL of the article",
    )
    parser.add_argument(
        "--nickname",
        help="Nickname of the public account",
    )
    parser.add_argument(
        "--mode", type=int, default=4, help="Mode for downloading article"
    )
    parser.add_argument(
        "--format",
        choices=["html", "pdf", "markdown"],
        default="html",
        help="Format for batch download",
    )

    args = parser.parse_args()

    if args.action == "gui":
        WechatGUI().run()
        return

    scrapper = WechatScrapper(appmsg_token="your_appmsg_token", cookie="your_cookie")

    if args.action == "download":
        result = scrapper.download(
            url=args.url, nickname=args.nickname, mode=args.mode, format=args.format
        )
    elif args.action == "info":
        result = scrapper.get_article_info(args.url)
    elif args.action == "account":
        result = scrapper.get_public_account_info(args.nickname)

    print(result)


if __name__ == "__main__":
    main()
