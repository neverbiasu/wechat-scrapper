import os
from wechatarticles import Url2Html


def main():
    url = "https://mp.weixin.qq.com/s?__biz=MzUzNjk1NDIyNg==&mid=2247506248&idx=1&sn=c9a8b4d2e11fd1b6ae924877da3f0ea8&chksm=faeccd55cd9b44432ea81578b1e33db2ae5ce938ed5a90e32847cb0ea88916a16ac47c92e135&scene=132#wechat_redirect"
    uh = Url2Html()
    res = uh.run(url, mode=4)
    print(res)


if __name__ == "__main__":
    main()
