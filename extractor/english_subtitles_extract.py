import re

def extract_english_text(input_file, output_file):
    english_text = []
    with open(input_file, 'r', encoding='utf-8') as file:
        in_events = False
        for line in file:
            if line.strip().startswith('[Events]'):
                in_events = True
                continue
            if in_events and line.startswith('Dialogue:'):
                # 提取 "Text" 部分的内容
                text = line.split(',', 9)[-1]
                # 使用正则表达式找到 \N{任意内容} 后的部分
                match = re.search(r'\\N{.*?}(.*)', text)
                if match:
                    english_text.append(match.group(1))

    # 将结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write('\n'.join(english_text))

# 获取文件路径输入
input_file_path = input("请输入字幕文件的路径: ")
output_file_path = "./english_text.txt"

# 执行提取并保存结果
extract_english_text(input_file_path, output_file_path)
print(f"提取的英文文本已保存到 {output_file_path}")
