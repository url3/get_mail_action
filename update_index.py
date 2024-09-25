import os
import re  # 添加这个导入

def update_index():
    codes = []
    with open('codes.txt', 'r') as f:
        codes = f.readlines()
    
    index_path = 'index.html'
    with open(index_path, 'r') as file:
        content = file.read()

    # 清除旧的验证码内容，保留其他内容
    new_content = re.sub(r'(<p>验证码:.*?</p>\n*)*', '', content)

    # 将验证码添加到 index.html
    for code in codes:
        new_content += f'<p>验证码: {code.strip()}</p>\n'  # 去除换行符

    with open(index_path, 'w') as file:
        file.write(new_content)

if __name__ == '__main__':
    update_index()
