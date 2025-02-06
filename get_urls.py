import requests
import re
from bs4 import BeautifulSoup

def get_urls(url, output_file = "chapters.csv"):
    # 目标 URL
    base_url = "https://ghxs.net/"

    html = get_html(url)

    # 解析 HTML
    soup = BeautifulSoup(html, "html.parser")

    # 查找所有 <li class="hide"> 标签
    hide_items = soup.find_all("li", class_="hide")

    # 结果存储
    chapter_dict = {}

    with open(output_file, "w", encoding="utf-8") as file:
        for item in hide_items:
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
    card_div = soup.find('div', class_='card')
    header_div = card_div.find('div', class_='header line')
    h1_tag = header_div.find('h1')
    title = h1_tag.text
    # 寻找小说作者
    pattern = r'<li>\s*作者：\s*<a\s+href="\/author\/[^"]+\.html"[^>]*>([^<]+)<\/a>\s*<\/li>'
    match = re.search(pattern, html)
    author = match.group(1)
    return title, author

def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    with requests.get(url, headers=headers) as response:
        response.encoding = response.apparent_encoding
        content = response.text
    return content
