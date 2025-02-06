import re
import os
import time
import requests
import concurrent.futures
import argparse
from bs4 import BeautifulSoup
from get_urls import get_urls, title_author
from chinese2arabic import chinese2arabic
from create_epub import create_epub

# 初始信息
chapters_url_folder = "./chapters.csv"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

def content_extract(chapter_url):
    try:
        with requests.get(chapter_url, headers=headers) as response:
            response.encoding = "utf-8"
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')

            # 文件内容处理
            # print(chapter_url)
            # print(response.status_code)
            #https://www.bqg128.com/book/44949/2.html
            content_div = soup.find("div", id="chaptercontent")
            novel_text = content_div.get_text(separator="\n", strip=True)
            return novel_text
    except Exception as e:
        print(f"出错：{e}")
        return ""

def write_to_file(content, output_folder, file_name):
    with open(f"{output_folder}/{file_name}.txt", "w", encoding="utf-8") as txt_file:
        txt_file.write(content)
    print(f"提取的内容已保存到 {output_folder}/{file_name}.txt")

def convert_charptnum(text):
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    def replace_match(match):
        chinese_number = match.group(1)
        arabic_number = chinese2arabic(chinese_number)
        return f'第{arabic_number}章'
    pattern = r'第([零一二三四五六七八九十百千万亿]+)章'
    return re.sub(pattern, replace_match, text)

def process_chapter(chapter_url, chapters_url_dict, txt_folder):
    """处理单个章节：提取内容并写入文件"""
    content = content_extract(chapter_url)
    file_name_raw = chapters_url_dict[chapter_url]
    file_name = convert_charptnum(file_name_raw)
    write_to_file(content, txt_folder, file_name)
    time.sleep(0.5)  # 避免对服务器压力过大

if __name__ == "__main__":
    # 接受位置参数输入
    parser = argparse.ArgumentParser()
    parser.add_argument('param1', type=str, help='第一个参数')
    args = parser.parse_args()
    url = args.param1
    # 小说名字和作者
    title, author = title_author(url)
    print(title, author)

    txt_folder = f"./小说/{title}"
    if not os.path.exists(txt_folder):
        os.mkdir(txt_folder)
        print(f"文件夹 '{txt_folder}' 创建成功。")
    else:
        print(f"文件夹 '{txt_folder}' 已经存在。")

    chapters_url_dict = get_urls(url, chapters_url_folder)
    max_workers = 10
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_chapter, chapter_url, chapters_url_dict, txt_folder)
            for chapter_url in chapters_url_dict.keys()
        ]
        
        # 等待所有任务完成
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # 捕获异常
            except Exception as e:
                print(f"处理章节时出错: {e}")
    create_epub(txt_folder, title, author)
