import requests
import re
from bs4 import BeautifulSoup

def get_urls(url, output_file = "chapters.csv"):
    # 基础URL -> 主网站网址
    base_url = re.sub(r'\d+/$', '/', url).rstrip('index/')

    html = get_html(url)

    # 解析 HTML
    soup = BeautifulSoup(html, "html.parser")

    # 查找所有 <div class="listmain"> 标签
    listmain = soup.find("div", class_="listmain")
    dl = listmain.find("dl")
    items = dl.find_all('dd', class_=False)

    # 结果存储
    chapter_dict = {}

    with open(output_file, "w", encoding="utf-8") as file:
        for item in items:
            link_tag = item.find("a")
            if link_tag:
                chapter_url = base_url + link_tag["href"]  # 拼接完整链接
                chapter_title = link_tag.text.strip()  # 获取章节名称
                chapter_dict[chapter_url] = chapter_title
                file.write(f"{chapter_url},{chapter_title}\n")

    return chapter_dict

def title_author(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    # 寻找小说名字
    info = soup.find('div', class_='info')
    h1_tag = info.find('h1')
    title = h1_tag.text
    # 寻找小说作者
    small = soup.find('div', class_='small')
    author = small.find('span').text
    author = author.lstrip('作者：')
    return title, author

def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    with requests.get(url, headers=headers) as response:
        response.encoding = response.apparent_encoding
        content = response.text
    return content
