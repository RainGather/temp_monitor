# -*- coding: utf-8 -*- 

import smtplib
import time
import json

from email.mime.text import MIMEText
from os.path import exists, split, realpath, join


def send_email(subject, msg='No Msg'):
    now_dir = split(realpath(__file__))[0]
    with open(join(now_dir, 'temp_monitor.cfg'), 'r') as fr:
        cfg = json.load(fr)
    if not exists(join(now_dir, 'last_email_send_time.txt')):
        with open(join(now_dir, 'last_email_send_time.txt'), 'w') as fw:
            fw.write('0')
    with open(join(now_dir, 'last_email_send_time.txt'), 'r') as fr:
        if time.time() - float(fr.read()) < 300:
            print('Too Short Time. Sleep 300s.')
            time.sleep(300)
    msg = MIMEText(msg.encode('utf-8'), 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = cfg['send_email']
    msg['To'] = cfg['recv_email']

    s = smtplib.SMTP(cfg['smtp'])
    s.login(cfg['send_email'], cfg['passwd'])
    s.sendmail(cfg['send_email'], cfg['recv_email'], msg.as_string())
    print('Email Sent!')
    s.quit()
    with open(join(now_dir, 'last_email_send_time.txt'), 'w') as fw:
        fw.write(str(time.time()))
    return True


if __name__ == '__main__':
    from get_linux_ip import get_ip_address
    send_email('Test Title', get_ip_address('wlp2s0'))
