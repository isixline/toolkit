import os
import re
import json
from dotenv import load_dotenv

def find_markdown_files(directory):
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def parse_links_and_content_from_file(file_path):
    links = []
    references = []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        matches = re.findall(r'\[\[(.*?)\]\]', content)
        links.extend([match for match in matches if match != '📄'] if matches else matches)  
        references.extend([match for match in matches if match == '📄'] if matches else matches)
        cleaned_content = re.sub(r'\[\[.*?\]\]', '', content).replace('- \n', '')

    return links, cleaned_content, references

def is_exclude_file(file_name):
    exclude_file_prefix_list =  os.getenv('KNOW_LIB_EXCLUDE_FILE_PREFIX_LIST')
    for prefix in exclude_file_prefix_list:
        if file_name.startswith(prefix):
            return True
        
    return False

def find_nodes(directory):
    nodes = []
    markdown_files = find_markdown_files(directory)

    for file_path in markdown_files:
        file_name = os.path.basename(file_path)
        if is_exclude_file(file_name):
            continue
        file_name_without_extension = file_name[:-3]
        
        links, content, references = parse_links_and_content_from_file(file_path)
        
        nodes.append({
            "name": file_name_without_extension,
            "links": links,
            "content": content,
            "references": references
        })
    return nodes

def set_category(nodes, categories, default_category):
    for node in nodes:
        first_letter = node['name'][0]

        if first_letter in categories:
            category = first_letter
        else:
            category = default_category

        node['category'] = category

    return nodes
        

def output_graph(directory, output_file):
    nodes = find_nodes(directory)

    categories = os.getenv('KNOW_LIB_CATEGORIES').split(',')
    default_category = os.getenv('KNOW_LIB_DEFAULT_CATEGORY')
    nodes = set_category(nodes, categories, default_category)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({'categories': categories , 'nodes': nodes}, f, ensure_ascii=False, indent=4)

def handle():
    load_dotenv()
    directory = os.getenv('KNOW_LIB_FILE_PATH') 
    output_file = './temp/know_lib.json' 
    output_graph(directory, output_file)
    print(f"output with {output_file}")
    return output_file

if __name__ == '__main__':
    handle()
