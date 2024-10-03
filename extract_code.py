import imaplib
import email
from email.header import decode_header
import re
import os
from datetime import datetime, timedelta

# 邮箱配置
username = os.getenv('EMAIL_USERNAME')
password = os.getenv('EMAIL_PASSWORD')
imap_server = os.getenv('EMAIL_IMAP')
code_blockwords = os.getenv('CODE_BLOCKWORDS')  # ['找回', '重置', '密保', '二级']
print('code_blockwords:', code_blockwords)

def connect_to_email():
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    return mail

def fetch_latest_emails(mail, num=8):
    mail.select('inbox')
    status, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()
    latest_ids = email_ids[-num:]
    emails = []

    for e_id in latest_ids:
        _, msg = mail.fetch(e_id, '(RFC822)')
        emails.append(msg[0][1])

    return emails

def contains_keywords(text):
    keywords = code_blockwords
    return any(keyword in text for keyword in keywords)

def convert_to_beijing_time(timestamp):
    # 将 UTC 时间转换为北京时间
    beijing_time = timestamp + timedelta(hours=8)
    return beijing_time.strftime('%Y-%m-%d %H:%M:%S')

def extract_codes(emails):
    codes = []
    for msg in emails:
        email_msg = email.message_from_bytes(msg)
        if email_msg.is_multipart():
            for part in email_msg.walk():
                if part.get_content_type() == 'text/plain':
                    text = part.get_payload(decode=True).decode()
                    match = re.search(r'\b\d{4,6}\b', text)  # 查找第一组验证码
                    if match:
                        # 获取发信时间
                        date_tuple = email.utils.parsedate_tz(email_msg['Date'])
                        if date_tuple:
                            timestamp = email.utils.mktime_tz(date_tuple)
                            beijing_time = convert_to_beijing_time(datetime.fromtimestamp(timestamp))
                        else:
                            beijing_time = "未知时间"

                        # 检查是否包含关键词
                        code = match.group()
                        if contains_keywords(text):
                            code = '******'  # 替换为******
                        codes.append(f"验证码: {code} 接码时间: {beijing_time}")  # 保存格式化字符串
                        break  # 找到后跳出内层循环
    return codes

def main():
    mail = connect_to_email()
    latest_emails = fetch_latest_emails(mail)
    codes = extract_codes(latest_emails)
    mail.logout()

    # 打印提取到的验证码
    print('Extracted Codes:', codes)

    with open('codes.txt', 'w') as f:
        for code in codes:
            f.write(f"{code}\n")

if __name__ == '__main__':
    main()
