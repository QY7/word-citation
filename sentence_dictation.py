# -*- coding: UTF-8 -*-
from aip import AipSpeech
from playsound import playsound
import time
import os

def get_audio(s,pos):
    """ 你的 APPID AK SK """
    APP_ID = '16087080'
    API_KEY = '6r3xXYgLn0xZ0aFfkMBGprfA'
    SECRET_KEY = 'OqdNHfKgxUo4j20YKDnaToI6dcvyWAKF'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    result  = client.synthesis(s, 'zh', 2, {
        'vol': 5,
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open("auido"+str(i)+".mp3", 'wb') as f:
            f.write(result)

with open('sentence_dictation.txt','r',encoding="utf8") as file:
    i = 0
    for line in file:
        line=line.strip('\n')
        get_audio(line,i)
        playsound("auido"+str(i)+".mp3")
        i = i+1
        time.sleep(3)
