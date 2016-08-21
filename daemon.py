# -*- coding: utf-8 -*-

import time
import json

from RPi import GPIO
from get_temp_and_humidity import get_temp_and_humidity
from send_email import send_email
from get_linux_ip import get_ip_address
from os.path import split, realpath, join


now_temps = []


def daemon():
    now_dir = split(realpath(__file__))[0]
    with open(join(now_dir, 'temp_monitor.cfg'), 'r') as fr:
        cfg = json.load(fr)
    temp1_pin = cfg['temp1_pin']
    temp2_pin = cfg['temp2_pin']
    safe_temp = cfg['safe_temp']

    nowtime = time.time()
    last_info_send_time = nowtime - (nowtime % (24 * 3600)) - 6 * 3600
    last_warning_send_time = 0
    info_time_interval = 3600 * 24
    warning_time_interval = 2 * 3600

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    notice = ''
    msg = ''
    state = ''
    init = True

    while True:
        temp1, hum1 = get_temp_and_humidity(temp1_pin)
        temp2, hum2 = get_temp_and_humidity(temp2_pin)
        print(str(temp1) + 'C, ' + str(hum1) + '%; ' + str(temp2) + 'C,' + str(hum2) + '%')
        if temp1 and temp2 and hum1 and hum2:
            if init:
                notice = 'Init Success!'
                msg = notice + '\ntemp1: ' + str(temp1) + '*C \ntemp2: ' + str(temp2) + '*C \nhum1: ' + str(hum1) + '% \nhum2: ' + str(hum2) + '% \nIP: ' + get_ip_address('wlan0')
                send_email(notice, msg)
                init = False
            if len(now_temps) > 10:
                now_temps.pop(0)
            now_temps.append(max(temp1, temp2))
            avg_now_temp = sum(now_temps) / len(now_temps)
            print(avg_now_temp)
            if avg_now_temp > safe_temp:
                notice = u'Warning! 警告！温度已超过警戒值！ [' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']'
                msg = notice + '\ntemp1: ' + str(temp1) + '*C \ntemp2: ' + str(temp2) + '*C \nhum1: ' + str(hum1) + '% \nhum2: ' + str(hum2) + '%'
                if state == 'normal':
                    send_email(notice, msg)
                    last_warning_send_time = time.time()
                state = 'warning'
            else:
                if state == 'warning':
                    notice = 'All Clear!'
                    msg = 'All Clear!' + '\ntemp1: ' + str(temp1) + '*C \ntemp2: ' + str(temp2) + '*C \nhum1: ' + str(hum1) + '% \nhum2: ' + str(hum2) + '%'
                    send_email(notice, msg)
                state = 'normal'
            if time.time() - last_warning_send_time > warning_time_interval and state == 'warning':
                send_email(notice, msg)
                last_warning_send_time = time.time()
            if time.time() - last_info_send_time > info_time_interval and state == 'normal':
                notice = 'Daily Info [' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']'
                msg = notice + '\ntemp1: ' + str(temp1) + '*C \ntemp2: ' + str(temp2) + '*C \nhum1: ' + str(hum1) + '% \nhum2: ' + str(hum2) + '%'
                if send_email(notice, msg):
                    last_info_send_time += info_time_interval

        if time.time() - max(last_info_send_time, last_warning_send_time) > 1.1 * info_time_interval:
            if send_email('Something Error!', 'Maybe Can Not Get Data'):
                last_info_send_time += info_time_interval
            print(str(temp1) + 'C, ' + str(hum1) + '%; ' + str(temp2) + 'C,' + str(hum2) + '%')
        time.sleep(3)


if __name__ == '__main__':
    daemon()
