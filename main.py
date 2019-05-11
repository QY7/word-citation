import os
import urllib.request
import requests,time
from random import shuffle
from playsound import playsound

class youdao():
    def __init__(self, type=0, word='hello'):
        '''
        调用youdao API
        type = 0：美音
        type = 1：英音

        判断当前目录下是否存在两个语音库的目录
        如果不存在，创建
        '''
        word = word.lower()  # 小写
        self._type = type  # 发音方式
        self._word = word  # 单词

        # 文件根目录
        self._dirRoot = os.path.dirname(os.path.abspath(__file__))
        if 0 == self._type:
            self._dirSpeech = os.path.join(self._dirRoot, 'Speech_US')  # 美音库
        else:
            self._dirSpeech = os.path.join(self._dirRoot, 'Speech_EN')  # 英音库

        # 判断是否存在美音库
        if not os.path.exists('Speech_US'):
            # 不存在，就创建
            os.makedirs('Speech_US')
        # 判断是否存在英音库
        if not os.path.exists('Speech_EN'):
            # 不存在，就创建
            os.makedirs('Speech_EN')

    def setAccent(self, type=0):
        '''
        type = 0：美音
        type = 1：英音
        '''
        self._type = type  # 发音方式

        if 0 == self._type:
            self._dirSpeech = os.path.join(self._dirRoot, 'Speech_US')  # 美音库
        else:
            self._dirSpeech = os.path.join(self._dirRoot, 'Speech_EN')  # 英音库

    def getAccent(self):
        '''
        type = 0：美音
        type = 1：英音
        '''
        return self._type

    def down(self, word):
        '''
        下载单词的MP3
        判断语音库中是否有对应的MP3
        如果没有就下载
        '''
        word = word.lower()  # 小写
        tmp = self._getWordMp3FilePath(word)
        if tmp is None:
            self._getURL()  # 组合URL
            # 调用下载程序，下载到目标文件夹
            # print('不存在 %s.mp3 文件\n将URL:\n' % word, self._url, '\n下载到:\n', self._filePath)
            # 下载到目标地址
            music_data = requests.get(self._url).content
            #下载到本地
            # print(self._filePath)
            with open(self._filePath,'wb') as f:
                f.write(music_data)
        else:
            pass

        # 返回声音文件路径
        return self._filePath

    def _getURL(self):
        '''
        私有函数，生成发音的目标URL
        http://dict.youdao.com/dictvoice?type=0&audio=
        '''
        self._url = r'http://dict.youdao.com/dictvoice?type=' + str(
            self._type) + r'&audio=' + self._word

    def _getWordMp3FilePath(self, word):
        '''
        获取单词的MP3本地文件路径
        如果有MP3文件，返回路径(绝对路径)
        如果没有，返回None
        '''
        word = word.lower()  # 小写
        self._word = word
        self._fileName = self._word + '.mp3'
        self._filePath = os.path.join(self._dirSpeech, self._fileName)

        # 判断是否存在这个MP3文件
        if os.path.exists(self._filePath):
            # 存在这个mp3
            return self._filePath
        else:
            # 不存在这个MP3，返回none
            return None


if __name__ == "__main__":
    sp = youdao()
    print('输入听写的list')
    lst_id = input()
    print('开始听写')
    wrong_list = []

    # 随机听写

    with open(f'word-citation\\word-list\\red book\\list{lst_id}.txt','r') as f:
        contents = f.read()
        contents = contents.split('\n')
        shuffle(contents)

    for line in contents:
        sp.down(line)
        playsound(sp._filePath)
        input_str = input()
        if(input_str==line):
            pass
        elif(input_str == 'exit'):
            break
        else:
            print('>>Wrong<<')
            wrong_list.append([line,input_str])
        # time.sleep(9)
    print('听写结果')
    print('---------------------------------')
    print(f'{"Your answer":<15}  {"Right answer":<15}')
    print('---------------------------------')
    for item in wrong_list:
        print(f'{item[1]:<15}  {item[0]:<15}')
    print('---------------------------------')
    print("正确率:%.1f%%"%((1-len(wrong_list)/len(contents))*100))
    os.system("pause")