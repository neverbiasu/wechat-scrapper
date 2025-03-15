# coding: utf-8
import os
from pprint import pprint
from wechatarticles import PublicAccountsWeb

if __name__ == "__main__":
    # 模拟登录微信公众号平台，获取微信文章的url
    cookie = "ua_id=0880e8QgBZLtL50BAAAAACyk7XeUVkEE02Seq-fsuDU=; wxuin=42047251064025; _clck=1vbq8u5|1|fu8|0; uuid=b7538d61568dfa45877327dae6445bcb; rand_info=CAESIOe2AJ5JFUuzfCuO7nyDclhGd954TAmsC8Ca0GyDron6; slave_bizuin=3946314452; data_bizuin=3946314452; bizuin=3946314452; data_ticket=omFNKsIwbQ0dCYjFXQLS/1MULCA5nqN2/z8aHzfpdq004j3yZG4cO4LwO+hVmO4K; slave_sid=UXRzY2pibklLeXpTbWIxZ1d0S2FxQzdqSG03X2tuNEFFNWg1bmdHVkdrNE53czRRXzhhSXJJczd5YWVYcUxNX19CTDRfVWNpeGdoMERMcUlQS1JNUFNLQkNNWkhWNDlrcjREenlzam5EdmdxSUZxUklVeGU2UWhoMDVZc3IzODhTeDE5NHo4TGpBMFU3SGZO; slave_user=gh_e2aadf0925f7; xid=077bff11be40f5160c0dd0c523756821; mm_lang=zh_CN; rewardsn=; wxtokenkey=777; _clsk=8uq8k5|1742060438400|6|1|mp.weixin.qq.com/weheat-agent/payload/record"
    token = "983779335"
    nickname = "陌北有棵树"
    biz = "biz"

    paw = PublicAccountsWeb(cookie=cookie, token=token)
    # articles_sum = paw.articles_nums(nickname)
    article_data = paw.get_urls(nickname, begin="0", count="5")
    # official_info = paw.official_info(nickname)

    # print("articles_sum:", end=" ")
    # print(articles_sum)
    print("artcles_data:")
    pprint(article_data)
    # print("official_info:")
    # pprint(official_info)
