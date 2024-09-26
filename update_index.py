import os
import re
from datetime import datetime, timedelta

# 获取当前北京时间
def get_beijing_time():
    utc_time = datetime.utcnow()
    beijing_time = utc_time + timedelta(hours=8)  # 北京时间是 UTC+8
    return beijing_time.strftime('%Y-%m-%d %H:%M:%S')

def update_index():
    # 读取 codes.txt 中的验证码
    codes = []
    with open('codes.txt', 'r') as f:
        codes = f.readlines()

    # 去除每个验证码的换行符，并按照提取顺序反转
    codes = [code.strip() for code in codes][::-1]  # 从后往前排列

    # 获取当前北京时间
    current_time = get_beijing_time()

    index_path = 'index.html'
    with open(index_path, 'r') as file:
        content = file.read()

    # 清除旧的验证码内容，保留其他内容
    new_content = re.sub(r'(<p>验证码:.*?</p>\n*)*', '', content)
    new_content = re.sub(r'(<p>获取时间:.*?</p>\n*)*', '', content)

    # 添加最新获取验证码时间
    new_content += f'<p>获取时间: {current_time}</p>\n'

    # 按从后往前的顺序将验证码添加到 index.html
    for code in codes:
        new_content += f'<p>验证码: {code}</p>\n'

    # 写入更新后的内容
    with open(index_path, 'w') as file:
        file.write(new_content)

if __name__ == '__main__':
    update_index()
