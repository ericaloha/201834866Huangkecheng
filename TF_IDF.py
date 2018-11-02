import math

from Vsm.preProcessing import PreProcessing
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password=123456, db=0)
Redis = redis.Redis(connection_pool=pool)
#1.计算文件中word分数
def GetLength(path):
    wordList =PreProcessing(path)
    return len(wordList)
#2.计算TF
def TF(Redis):
    wordList =Redis.keys()
    wordDict ={}
    for item in wordList:
        wordDict[item] =0

    for item in wordList:
        pathList =Redis.get(item)
        for path in pathList:
            length =GetLength(path)
            TF =item[path ] /length
            wordDict[item ] =TF
    return wordDict
#2.计算IDF
def IDF(Redis ,totalFileCount):
    wordList =Redis.keys()
    wordDict ={}
    for item in wordList:
        wordList[item ] =0
    count =0
    for item in wordList:
        info =Redis.get(item)
        for file in info:
            if file in info.keys():
                count +=1
        wordDict[item ] =math.log(totalFileCount / count)
    return wordDict

#3.计算TF_IDF
def TF_IDF(Redis,totalFileCount):
    TF_IDF_Dict ={}
    keyList =Redis.keys()
    for item in keyList:
        TF_IDF_Dict[item ] =0

    TF_Dict =TF(Redis)
    IDF_Dict =IDF(Redis,totalFileCount)
    for item in keyList:
        TF_IDF_Dict[item ] =TF_Dict[item ] * IDF_Dict[item]
    return TF_IDF_Dict


def GetTotalfileCount(localdir):
    list = os.listdir(localdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(localdir, list[i])
        if os.path.isdir(path):
            return GetTotalfileCount(path)
        elif os.path.isfile(path):
            return 1+GetTotalfileCount(path)
    


if __name__=='__main__':
    localdir='C:\\20news-18828'
    totalFileCount =GetTotalfileCount(localdir)


    TF_IDF(Redis, totalFileCount)
