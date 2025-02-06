from get_urls import title_author
from create_epub import create_epub

# 初始信息
url = "https://ghxs.net/21093/"
txt_folder = "./小说"
chapters_url_folder = "./chapters.csv"

# title = "大明：开局请朱元璋退位"
# author = "姜阿山小树"
title, author = title_author(url)

create_epub(txt_folder, title, author)
