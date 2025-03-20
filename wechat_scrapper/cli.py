import argparse
import os
import sys
import time
import random
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
    parser.add_argument(
        "--cookie",
        help="Cookie for authentication",
    )
    parser.add_argument(
        "--token",
        help="Token for authentication",
    )
    parser.add_argument(
        "--config",
        help="Path to config file containing cookie and token",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory to save downloaded files",
        default=os.getcwd(),
    )
    parser.add_argument(
        "--delay-min",
        type=float,
        default=3.0,
        help="Minimum delay between requests in seconds",
    )
    parser.add_argument(
        "--delay-max",
        type=float,
        default=8.0,
        help="Maximum delay between requests in seconds",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=3,
        help="Number of articles to download in each batch before resting",
    )
    parser.add_argument(
        "--batch-delay",
        type=float,
        default=15.0,
        help="Delay between batches in seconds",
    )
    parser.add_argument(
        "--user-agent",
        help="Custom User-Agent header",
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    )

    args = parser.parse_args()

    # 显示当前工作目录
    print(f"当前工作目录: {os.getcwd()}")

    # 检查是否提供了配置文件路径
    if args.config:
        try:
            import json

            with open(args.config, 'r', encoding='utf-8') as f:
                config = json.load(f)
                cookie = config.get('cookie', '')
                token = config.get('token', '')
        except Exception as e:
            print(f"Error loading config file: {e}")
            return
    else:
        cookie = args.cookie
        token = args.token

    # 验证是否提供了必需的认证信息
    if args.action != "gui" and not (cookie and token):
        print("错误: 必须提供 cookie 和 token，或使用配置文件")
        return

    if args.action == "gui":
        WechatGUI(token, cookie, output_dir=args.output_dir).run()
        return

    # 创建输出目录
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        print(f"已创建输出目录: {args.output_dir}")
    else:
        print(f"使用现有输出目录: {args.output_dir}")

    scrapper = WechatScrapper(
        appmsg_token=token, cookie=cookie, output_dir=args.output_dir
    )

    # 设置延迟参数
    scrapper.min_delay = args.delay_min
    scrapper.max_delay = args.delay_max

    # 设置批次大小和延迟
    if hasattr(scrapper, "batch_size"):
        scrapper.batch_size = args.batch_size
    if hasattr(scrapper, "batch_delay"):
        scrapper.batch_delay = args.batch_delay

    print(f"设置请求延迟: {scrapper.min_delay}-{scrapper.max_delay}秒")

    # 添加随机启动延迟，避免规律性请求
    start_delay = random.uniform(1, 5)
    print(f"添加随机启动延迟: {start_delay:.2f}秒...")
    time.sleep(start_delay)

    try:
        if args.action == "download":
            if not args.url and not args.nickname:
                print("错误: 必须提供 --url 或 --nickname 参数")
                return
            result = scrapper.download(
                url=args.url, nickname=args.nickname, mode=args.mode, format=args.format
            )
        elif args.action == "info":
            if not args.url:
                print("错误: 必须提供 --url 参数")
                return
            result = scrapper.get_article_info(args.url)
        elif args.action == "account":
            if not args.nickname:
                print("错误: 必须提供 --nickname 参数")
                return
            result = scrapper.get_public_account_info(args.nickname)

        if result and isinstance(result, str) and "需要手动验证" in result:
            print("\n检测到需要环境验证！")
            print("请在微信中手动访问文章链接并完成验证后，再更新cookie重试。")
            sys.exit(1)

        if result:
            print("\n结果:")
            print(result)
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"执行过程中出错: {str(e)}")
        if "验证" in str(e) or "异常" in str(e):
            print("可能是微信反爬机制触发，请更新cookie后重试")
        sys.exit(1)


if __name__ == "__main__":

    main()
