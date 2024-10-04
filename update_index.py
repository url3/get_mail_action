import os
import re
from datetime import datetime, timedelta

code_phonenumber = os.getenv('CODE_PHONENUMBER')
code_blackwords = os.getenv('CODE_BLACKWORDS') or []  # [888777, 1600, 2024]
keywordx = code_blackwords.split("|")
print('Black关键词:', keywordx)

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
    new_content = re.sub(r'(<h1>.*?</h1>\n*)*', '', content)
    new_content += f'<h1>{code_phonenumber}</h1>\n'

    new_content = re.sub(r'(<p><span>时间</span>:.*?</p>\n*)*', '', new_content)

    # 按从后往前的顺序将验证码添加到 index.html
    for code in codes:
        match_code = re.search(r'\b\d{4,6}\b', code)
        if match_code is not None:
            get_code = match_code.group()
        # 如果 get_code 在列表中，跳过；如果不在，追加
        if get_code is not None and get_code in keywordx:
            continue  # 忽略特定的 code
        else:
            new_content += f'<p>{code}</p>\n'  # 追加代码

    # 添加最新获取验证码时间
    new_content = re.sub(r'(<p><b>最后更新.*?</p>\n*)*', '', new_content)
    new_content += f'<p><b>最后更新时间: {current_time} (每2分钟自动刷新)</b></p>\n'

    new_content = re.sub(r'(</div></body></html>.*?\n*)*', '', new_content)
    new_content += f'</div></body></html>\n'

    # 写入更新后的内容
    with open(index_path, 'w') as file:
        file.write(new_content)

if __name__ == '__main__':
    update_index()
