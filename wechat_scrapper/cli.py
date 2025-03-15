import argparse
from .scrapper import WechatScrapper


def main():
    parser = argparse.ArgumentParser(description="Wechat Scrapper CLI")
    parser.add_argument(
        "action", choices=["download", "info", "account"], help="Action to perform"
    )
    parser.add_argument(
        "url_or_nickname", help="URL of the article or nickname of the public account"
    )
    parser.add_argument(
        "--mode", type=int, default=4, help="Mode for downloading article"
    )

    args = parser.parse_args()

    scrapper = WechatScrapper(appmsg_token="your_appmsg_token", cookie="your_cookie")

    if args.action == "download":
        result = scrapper.download_article(args.url_or_nickname, args.mode)
    elif args.action == "info":
        result = scrapper.get_article_info(args.url_or_nickname)
    elif args.action == "account":
        result = scrapper.get_public_account_info(args.url_or_nickname)

    print(result)


if __name__ == "__main__":
    main()
