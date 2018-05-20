from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd

def open_ptt_url(url):
    # 幫request 加上包裝紙 (即加上request headers)
    r = Request(url)
    r.add_header("user-agent", "Mozilla/5.0")
    response = urlopen(r)
    html = BeautifulSoup(response)
    return  html

def extract(content, tag, dict):
    removes = content.find_all(tag, dict)
    for remove in removes:
        remove.extract()
    return content

url = "https://www.ptt.cc/bbs/movie/index.html"
# print(html)
html = open_ptt_url(url)
posts = html.find_all("div", {"class": "r-ent"})

df = pd.DataFrame(columns=["title", "url", "content"])

for post in posts:
    aDom = post.find("div", {"class": "title"}).find("a")
    if aDom:
        href = "https://www.ptt.cc" + aDom["href"]
        anchor_content = aDom.string
        #  .string 為簡化版之.contents => 只有在dom內無其他元素時可使用
        if not "公告" in anchor_content:
            post_html = open_ptt_url(href)
            main_content = post_html.find("div", {"id": "main-content"})
            # print(main_content)
            main_content = extract(main_content, "div", {"class": "article-metaline"})
            main_content = extract(main_content, "div", {"class": "article-metaline-right"})
            main_content = extract(main_content, "span", {"class": "f2"})
            main_content = extract(main_content, "div", {"class": "push"})

            #  remove new line => \r in Mac and \n in Windows
            revise = main_content.text.replace("\r", "").replace("\n", "")

            # text 相當於 innerText
            s = pd.Series([anchor_content, href, revise], index = ["title", "url", "content"])
            df = df.append(s, ignore_index=True)

            # print(main_content)
    print(anchor_content, href)

df.to_csv("result.csv", encoding="utf-8", index=False)