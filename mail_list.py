import os
import email
import datetime
import email
import imaplib
import random
import time
import smtplib
import pprint
import re
import pickle
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 配置信息
imap_server = 'imap.qq.com'
imap_username = '123@qq.com'
imap_password = ''
# smtp
smtp_server = '.fsg.com'  # smtp服务器地址
smtp_user = '.@fsg.com'  # 邮件转发目标地址
smtp_pass = ''  # 邮件转发目标地址
# mail info
reply_to = 'discussion@fsg.com'  # 邮件回复地址
sender_name = "discussion"  # 发件人姓名
# 设置群发列表
bcc_addr = ""
# 已经转发的邮件message-ID记录文件，根据您的实际情况进行修改
LOG_FILE = os.getcwd() + '/mail-transfer.log'
EMAIL_FILE = os.getcwd() + "/maillist.txt"

# 每隔多久检查当前邮箱，单位为秒，根据您的实际情况进行修改
CHECK_INTERVAL = 60
# 查找多少天的邮件
DAYS_SINCE = 1


def read_email_list():
    # with open(EMAIL_FILE, 'r') as log:
    #     lines = log.readlines()
    #     return set([line.strip() for line in lines])
    with open(EMAIL_FILE, 'rb') as f:
        # file = open(EMAIL_FILE, 'rb')
        return pickle.load(f)


# 记录订阅的邮件
def log_email_list(e):
    # with open(EMAIL_FILE, 'a') as log:
    #     log.write(str(email).lower() + '\n')
    e = str(e).lower()

    emails = read_email_list()
    # 只允许fsg.com的邮件加入
    if re.search(r"\b[A-Z0-9._%+-]+@fsg.com", e, re.IGNORECASE):
        emails.add(e)
    emails.discard(str(smtp_user))
    with open(EMAIL_FILE, 'wb') as f:
        pickle.dump(emails, f)


# 记录退订的邮件
def del_email_list(e):
    emails = read_email_list()
    emails.discard(str(e).lower())
    with open(EMAIL_FILE, 'wb') as f:
        pickle.dump(emails, f)


# 记录已经转发的邮件message-ID到日志文件
def log_message_id(msg_id):
    with open(LOG_FILE, 'a') as log:
        log.write(str(msg_id.strip()) + '\n')


# 从日志文件读取已经转发的邮件message-ID
def read_message_ids():
    with open(LOG_FILE, 'r') as log:
        lines = log.readlines()
        return set([line.strip() for line in lines])


def check_new_emails():
    """
    检查新邮件并转发
    """

    sent_msg_ids = read_message_ids()

    imap_obj = imaplib.IMAP4_SSL(imap_server)
    imap_obj.login(imap_username, imap_password)
    imap_obj.select('inbox')

    # 设置搜索条件
    # reply_to="monit@coolxigua.com"
    date = (datetime.date.today() - datetime.timedelta(days=DAYS_SINCE)).strftime('%d-%b-%Y')
    # criteria = f'SINCE "{date}"  FROM "{reply_to}"'
    # criteria = f'SINCE "{date}"  TO "{reply_to}"'
    criteria = f'SINCE "{date}"'
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),

    # 搜索符合条件的邮件
    print(criteria),
    result, data = imap_obj.search(criteria)
    print(data),

    # pprint.pprint((data))
    # pprint((result))
    for num in data[0].split():

        print("for loop in checkmail" + "*" * 30)
        bcc_addr = ','.join(read_email_list())

        typ, msg_data = imap_obj.fetch(num, '(RFC822)')
        email_message = email.message_from_bytes(msg_data[0][1])
        # 如果不是给discussion的邮件，跳过
        msg_to = email.utils.parseaddr(email_message['To'])[1]

        if str(msg_to).lower() != reply_to:
            print('To:', msg_to),
            print("not " + reply_to + " mail"),
            continue
        # print(email_message._headers)

        # 从邮件头中获取有用信息（如发件人、主题等）
        msg_from = email.utils.parseaddr(email_message['From'])[1]
        msg_from = str(msg_from).lower()
        print('From:', msg_from, end='', flush=True),
        msg_id = hashlib.md5(email_message.as_string().encode("utf-8")).hexdigest()

        # 如果处理过，跳过
        if str(msg_from).lower() == smtp_user or msg_id.strip() in sent_msg_ids:
            print(" processed mail")
            continue
        else:
            print('Message-ID:', msg_id.strip()),

        # 获取解码后的subject
        msg_subject = email.header.decode_header(email_message['Subject'])
        # print(msg_subject)
        decoded_str = ''
        # 解码元组 (原始字符串，编码方式)
        for dh in msg_subject:
            if (isinstance(dh[0], bytes)):
                decoded_str += dh[0].decode(dh[1] if dh[1] is not None else 'utf-8')
            else:
                decoded_str += dh[0]
        msg_subject = decoded_str
        print('Subject:', msg_subject),
        # 取消订阅
        if re.search(r"\bunsubscribe\b", msg_subject, re.IGNORECASE):
            print("unsubscribe" + msg_from),
            del_email_list(msg_from)
            send_bye(msg_from)
            log_message_id(msg_id)
            continue
        # 如果是订阅
        # if "subscribe" in email_message['Subject']:
        if re.search(r"\bsubscribe\b", msg_subject, re.IGNORECASE):
            log_email_list(msg_from)
            log_message_id(msg_id)
            send_welcome(msg_from)
            continue

        # 发送帮助邮件
        if re.search(r"\bhelpme\b", msg_subject, re.IGNORECASE):
            log_message_id(msg_id)
            send_help(msg_from)
            continue

        # 仅转发发件人在列表里邮箱的邮件
        if not (msg_from in read_email_list()):
            print("email not in list, do not forward"),
            log_message_id(msg_id)
            continue

        print("new mail"),
        # print(email_message)
        forward_email(email_message)
        log_message_id(msg_id)
        #print("*" * 47)
    # 断开连接
    imap_obj.logout()


help_msg = '''<p>您有问题可以发送邮件到discussion@fsg.com。所有加入的小伙伴都会收到你的邮件。同样回复给邮箱discussion@fsg.com的时候，所有加入的小伙伴也都会收到这个邮件。 </p>

<p>目前共有''' + str(len(read_email_list())) + '''人加入。</p>'''


def send_help(from_mail):
    msg = MIMEMultipart()
    # 设置文本内容
    html = '''<html><body><p>您好''' + from_mail.split("@")[0] + '''：</p>
<p> 欢迎使用discussion邮件讨论组。</p>
    ''' + help_msg + '''
</body></html>'''
    msg.attach(MIMEText(html, 'html'))
    # 设置邮件主题、发件人、收件人信息
    msg['Subject'] = '感谢参与讨论组，有什么问题需要'
    msg['To'] = from_mail
    send_mail(msg)


def send_bye(from_mail):
    msg = MIMEMultipart()
    # 设置文本内容
    html = '''<html><body><p>您好''' + from_mail.split("@")[0] + '''：</p>
<p> 感谢你参与discussion邮件讨论组。</p>
<p>再见，有问题请联系hui.ju@fsg.com</p>
<p>目前共有''' + str(len(read_email_list())) + '''人加入。</p></body></html>'''
    msg.attach(MIMEText(html, 'html'))
    # 设置邮件主题、发件人、收件人信息
    msg['Subject'] = '感谢参与讨论组，再见'
    msg['To'] = from_mail
    send_mail(msg)


def send_welcome(from_mail):
    msg = MIMEMultipart()
    # 设置文本内容
    html = '''<html><body><p>您好''' + from_mail.split("@")[0] + '''：</p>
<p> 欢迎加入discussion邮件讨论组。</p>
''' + help_msg + '''</body></html>'''
    msg.attach(MIMEText(html, 'html'))
    # 设置邮件主题、发件人、收件人信息
    msg['Subject'] = '欢迎加入讨论组'
    msg['To'] = from_mail
    send_mail(msg)


def print_email(email):
    print("*" * 1)
    # pprint.pprint(email.items())
    # print("*" * 80)


def forward_email(email_msg):
    # email_msg.replace_header("Bcc", bcc_addr)
    # print_email(email_msg)
    # message_dict = {k.lower(): v for k,v in email_msg.items()}
    msg_from = email.utils.parseaddr(email_msg['From'])[1]
    headers_to_keep = ['subject', 'content-type', 'mime-version', 'content-transfer-encoding', 'references',
                       'content-id', 'contents', 'attachments']
    # print(email_msg.keys())
    for header_name in email_msg.keys():
        if header_name.lower() not in headers_to_keep:
            # print(header_name)
            # msg.replace_header(header_name, None)
            del email_msg[header_name.lower()]

    # print(email_msg.keys())
    # print_email(email_msg)
    bcc_addr = ','.join(read_email_list())
    # email_msg.replace_header('From', '{} <{}>'.format(sender_name, smtp_user))
    email_msg['To'] = reply_to
    email_msg['Cc'] = msg_from
    email_msg['Bcc'] = bcc_addr

    # email_msg.replace_header("Message-Id", "<%s@fsg.com>" % (
    #         str(int(datetime.datetime.timestamp(datetime.datetime.now()))) + str(random.random())))
    print("bcc:" + bcc_addr)
    # print_email(email_msg)
    send_mail(email_msg)


def send_mail(email_msg):
    # # 发送邮件
    print("do send_mail. Subject is :" + email_msg['Subject'])
    email_msg['From'] = '{} <{}>'.format(sender_name, smtp_user)
    email_msg['Reply-To'] = reply_to
    email_msg['Date'] = email.utils.formatdate()
    email_msg['Message-Id'] = "<%s@fsg.com>" % (
            str(int(datetime.datetime.timestamp(datetime.datetime.now()))) + str(random.random()))

    # print(email_msg)
    with smtplib.SMTP(smtp_server) as smtp:
        smtp.login(smtp_user, smtp_pass)
        smtp.send_message(email_msg)


if __name__ == "__main__":
    # 循环检查新邮件并转发
    # while True:
    print("checking..."),
    check_new_emails()
    # send_welcome("phpbird@gmail.com")

    #
    # my_set = set()
    # with open(EMAIL_FILE, 'wb') as f:
    #    pickle.dump(my_set, f)

