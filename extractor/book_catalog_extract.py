import zipfile
from lxml import etree
import sys
import re

# 定义函数来解析 toc.ncx 文件
def parse_toc_ncx(epub_path):
    catalog = []
    # 打开 EPUB 文件
    with zipfile.ZipFile(epub_path, 'r') as epub_file:
        # 列出 EPUB 文件中的所有文件
        file_list = epub_file.namelist()
        
        # 查找 toc.ncx 文件的路径
        toc_ncx_path = None
        for file_path in file_list:
            if file_path.endswith('toc.ncx'):
                toc_ncx_path = file_path
                break
        
        if toc_ncx_path is None:
            print("找不到 toc.ncx 文件")
        else:
            # 读取 toc.ncx 文件的内容
            with epub_file.open(toc_ncx_path) as toc_ncx_file:
                # 使用 lxml 解析 toc.ncx 文件
                tree = etree.parse(toc_ncx_file)
                root = tree.getroot()
                
                # 获取所有 navPoint 节点
                nav_points = root.findall(".//{http://www.daisy.org/z3986/2005/ncx/}navPoint")
                
                # 遍历 navPoint 节点，提取目录信息
                for nav_point in nav_points:
                    # 获取标题
                    title = nav_point.findtext(".//{http://www.daisy.org/z3986/2005/ncx/}text")
                    catalog.append(title)
    
    return catalog

def write_catalog_to_file(catalog, output_file_path, only_main_title):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for title in catalog:
            if not only_main_title or re.match(r'^\d', title):
                    file.write("- " + title + '\n')
                
    
    print("目录提取完成！输出文件路径:", output_file_path)

def main():
    args = sys.argv
    
    catalog = parse_toc_ncx(args[1])

    output_file_path = args[2] if len(args) > 2 else 'temp/catalog.txt'
    write_catalog_to_file(catalog, output_file_path, True)

if __name__ == '__main__':
    main()
