import os
import urllib.request
import requests,time
from random import shuffle
from playsound import playsound
from colorama import init
from colorama import Fore, Back, Style

class youdao():
    def __init__(self, type=0):
        '''
        调用youdao API
        type = 0：美音
        type = 1：英音

        判断当前目录下是否存在两个语音库的目录
        如果不存在，创建
        '''
        self._type = type  # 发音方式
        # self.list_path = 'word-citation\\word-list\\red book'
        self.list_path = 'red book'
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
    def cite_list(self,_word_list):
        _wrong_list = []
        for word in _word_list:
            if(word == ''):
                continue
            self.down(word)
            playsound(self._filePath)
            input_str = input()
            if(input_str==word):
                pass
            elif(input_str == 'exit'):
                break
            else:
                print(Fore.RED+'>>Wrong<<'+Style.RESET_ALL)
                _wrong_list.append([word,input_str])
        
        print()
        print('---------------------------------')
        print(f'{"Your answer":<15}  {"Correct answer":<15}')
        print('---------------------------------')
        if not _wrong_list:
            print("You are the champion!!!") 
        for item in _wrong_list:
            print(f'{item[1]:<15}  {item[0]:<15}')

        print('---------------------------------')
        print(Fore.GREEN+"正确率:%.1f%%(%d/%d)"%((1-len(_wrong_list)/len(_word_list))*100, (len(_word_list)-len(_wrong_list)),len(_word_list))+Style.RESET_ALL)

        return _wrong_list


    def load_list(self,file):
        if not os.path.exists(f'{self.list_path}\\{file}'):
            print("No such file exists!")
            return []
        with open(f'{self.list_path}\\{file}','r') as f:
            _contents = f.read().strip()
            _contents = _contents.split('\n')
            _contents = list(set(_contents))
            _contents = list(filter(None, _contents)) # fastest
            shuffle(_contents)
            # _contents = filter(None, _contents)
        return _contents

    def save_wrong_list(self,id,_wrong_list):
        with open(f'{self.list_path}\\list{id}_wrong.txt','a') as f:
            for item in _wrong_list:
                f.write(item[0])
                f.write('\n')

if __name__ == "__main__":
    init()
    sp = youdao()
    while(1):
        print(Fore.YELLOW + Back.BLUE+'**********************************************')
        print('- insert number "i" to recite list_i          ')
        print('- insert "r i" to review mistakes in list_i   ')
        print('- insert "exit" to exit                       ')
        # print('**********************************************')
        print('**********************************************'+Style.RESET_ALL)
        lst_id = input()
        if(lst_id == 'exit'):
            break
        elif(lst_id[0]=='r'):
            lst_id = lst_id[1:].strip()
            contents = sp.load_list(f'list{lst_id}_wrong.txt')
            if not contents:
                continue
            print('Reviewing')
            wrong_list = sp.cite_list(contents)
            sp.save_wrong_list(lst_id,wrong_list)
        else:
            lst_id = lst_id.strip()
            
            contents = sp.load_list(f'list{lst_id}.txt')
            if not contents:
                continue
            print(Style.RESET_ALL+'Start citation')
            wrong_list = sp.cite_list(contents)
            sp.save_wrong_list(lst_id,wrong_list)
        print()