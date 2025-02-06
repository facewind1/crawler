import os
import re
from ebooklib import epub

# 定义文件夹路径和输出 EPUB 文件名
def create_epub(input_folder, title, author):
    # input_folder  存放章节文件的文件夹
    # output_epub  输出的 EPUB 文件名
    # 创建 EPUB 书籍对象
    book = epub.EpubBook()

    # 设置书籍元数据
    book.set_title(title)
    book.set_language("zh-CN")
    book.add_author(author)

    # 获取所有 txt 文件并按章节号排序
    def extract_number(filename):
        """提取文件名中的数字部分，用于排序"""
        match = re.search(r'\d+', filename)  # 提取文件中的数字部分
        return int(match.group()) if match else float('inf')  # 如果没有数字，则放到最后

    files = sorted(
        [f for f in os.listdir(input_folder) if f.endswith(".txt")],
        key=extract_number
    )

    # 定义章节列表
    chapters = []

    # 遍历排序后的文件
    for filename in files:
        filepath = os.path.join(input_folder, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # 创建 EPUB 章节
        chapter_title = os.path.splitext(filename)[0]  # 使用文件名作为章节标题
        chapter = epub.EpubHtml(title=chapter_title, file_name=f"{chapter_title}.xhtml", lang="zh-CN")
        formatted_content = content.replace("\n", "</p><p>")
        chapter.content = f"<h1>{chapter_title}</h1><p>{formatted_content}</p>"

        # 将章节添加到书籍中
        book.add_item(chapter)
        chapters.append(chapter)

    # 定义书籍目录
    book.toc = tuple(chapters)

    # 添加导航文件
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # 定义书籍的阅读顺序
    book.spine = ["nav"] + chapters

    # 保存 EPUB 文件
    output_epub = f"{title}.epub"
    epub.write_epub(output_epub, book, {})

    print(f"EPUB 文件已生成：{output_epub}")
