from aip import AipSpeech
from playsound import playsound

""" 你的 APPID AK SK """
APP_ID = '16087080'
API_KEY = '6r3xXYgLn0xZ0aFfkMBGprfA'
SECRET_KEY = 'OqdNHfKgxUo4j20YKDnaToI6dcvyWAKF'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

result  = client.synthesis('你好吗？', 'zh', 2, {
    'vol': 5,
})
# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('auido.mp3', 'wb') as f:
        f.write(result)

playsound("auido.mp3")