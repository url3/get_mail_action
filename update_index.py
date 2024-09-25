import os

def update_index():
    codes = []
    with open('codes.txt', 'r') as f:
        codes = f.readlines()
    
    index_path = 'index.html'
    with open(index_path, 'r') as file:
        content = file.read()
    
    # 将验证码添加到 index.html
    for code in codes:
        content += f'<p>验证码: {code.strip()}</p>\n'  # 去除换行符

    with open(index_path, 'w') as file:
        file.write(content)

if __name__ == '__main__':
    update_index()
