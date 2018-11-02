# 计算词典词在每篇文章中的出现频率
# 设计ds    key（该词）：value（dict 文件名：在该文章中出现的频率）
# 本地维护一个list存Key


# 词频（TF） = 某个词在文章中的出现次数 / 文章总词数
#逆文档频率（IDF） = log（语料库的文档总数/包含该词的文档总数+1）
import json
import os
from _tkinter import _flatten
from asyncio import sleep

import nltk
import redis
from Vsm.preProcessing import PreProcessing

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password=123456, db=0)
Redis = redis.Redis(connection_pool=pool)


# 0.产生 keylist
def GenerateKeyList(path, Redis):
    KeyList = Redis.keys()
    f = open(path, 'w', errors='ignore')
    f.write(str(KeyList))
    return KeyList


# 1.input:一片文章的wordlist
#  output:这篇文章的Dict
def Trans(wordlist):
    Dict = {}
    for word in wordlist:
        if word != "" and word in Dict.keys():
            time = Dict[word]
            Dict[word] = time + 1
        elif word != "" and word != " ":
            Dict[word] = 1

    return Dict


# input:文件路径和Redis、
# output:无
# 进行的操作：更新每个词在当前文件里的出现次数
def Getwordlist(Redis):
    keys=Redis.keys()
    return keys

def Trywithfile(path):
    fileTitle= path.split('\\')
    fileTitle=fileTitle[len(fileTitle)-2]+fileTitle[len(fileTitle)-1]
    #print(fileTitle)
    # 1.处理生成每个文章的wordlist
    wordlist = PreProcessing(path)
    DictPerFile = Trans(wordlist)
    #for item in DictPerFile:
     #   print(DictPerFile[item])
    for item in DictPerFile:
        if Redis.exists(item):
            InfoDict=json.loads(Redis.get(item))
            #print(InfoDict)
            if fileTitle in InfoDict.keys():
                time=InfoDict[fileTitle]
                time+=DictPerFile[item]
                InfoDict[fileTitle]=time
                Redis.set(item, json.dumps(InfoDict))
                print('owioff...')
            else:
                InfoDict[fileTitle]=DictPerFile[item]
                Redis.set(item,json.dumps(InfoDict))


# 2.算出一个词在所有文章里的tf，存进Fre
def Deal_all_files(rootdir):
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        '''if os.path.isdir(path):
            Deal_all_files(path)
            print('one dir finished...')
        '''
        if os.path.isfile(path):
            Trywithfile(path)
            #print('f f...')

def Deal_all_Dir(rootdir):
    list=os.listdir(rootdir)
    print(list)
    for i in range(0,len(list)):
        path=os.path.join(rootdir,list[i])
        if os.path.isdir(path):
            Deal_all_files(path)
            print('one dir finished....')


def StoreInDisk(localdir,Redis):
    keylist=Redis.keys()
    Record={}
    for key in keylist:
        info=json.loads(Redis.get(key))
        Record[str(key )]=info
    record=json.dumps(Record)
    print('Finish loading ')
    f=open(localdir,'w',errors='ignore')
    f.write(record)

    f.close()
    print('over')

def CalTF(Redis):
    pass
if __name__ == '__main__':
    #path = 'C:\\20news-18828'
    #keyList = Redis.keys()
    #Deal_all_Dir(path)
    localdir='C:\\Users\\eric\\SDU\\实验\\专业课实验\\DataMining\\Exp\\FinalDictInfo1'
    StoreInDisk(localdir,Redis)
