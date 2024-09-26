import imaplib
import email
from email.header import decode_header
import re
import os

# 邮箱配置
username = os.getenv('EMAIL_USERNAME')
password = os.getenv('EMAIL_PASSWORD')
imap_server = 'imap.qiye.aliyun.com'

def connect_to_email():
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    return mail

def fetch_latest_emails(mail, num=5):
    mail.select('inbox')
    status, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()
    latest_ids = email_ids[-num:]
    emails = []

    for e_id in latest_ids:
        _, msg = mail.fetch(e_id, '(RFC822)')
        emails.append(msg[0][1])
    
    return emails

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
                        codes.append(match.group())  # 只添加第一组验证码
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
