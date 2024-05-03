import os
import re
import json
from dotenv import load_dotenv

load_dotenv()

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

def is_exclude_file(file_name, exclude_file_prefix_list):
    for prefix in exclude_file_prefix_list:
        if file_name.startswith(prefix):
            return True
        
    return False

def find_nodes(directory, exclude_file_prefix_list):
    nodes = []
    markdown_files = find_markdown_files(directory)

    for file_path in markdown_files:
        file_name = os.path.basename(file_path)
        if is_exclude_file(file_name, exclude_file_prefix_list):
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
        node['category'] = default_category
        for category in categories:
            if category in node['name']:
                node['category'] = category
                break            

    return nodes

def get_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config
        
def collate_graph():
    directory = os.getenv('KNOW_LIB_FILE_PATH') 
    config = get_config()
    exclude_file_prefix_list = config['excludeFilePrefixList']
    categories = config['categories']
    default_category = config['defaultCategory']
    workspaces = config['workspaces']

    nodes = find_nodes(directory, exclude_file_prefix_list)
    
    nodes = set_category(nodes, categories, default_category)
    
    return {'categories': categories , 'workspaces': workspaces, 'nodes': nodes}

def output_graph(graph, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=4)
    

if __name__ == '__main__':
    graph = collate_graph()
    output_file = './temp/know_lib.json' 
    output_graph(graph, output_file)
    print(f"output with {output_file}")