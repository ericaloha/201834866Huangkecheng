import json
import os

import redis

from Vsm.Doing import mainfuc
from Vsm.TF_IDF_Redis import CalcIDF
from Vsm.preProcessing import PreProcessing
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password=123456, db=0)
Redis = redis.Redis(connection_pool=pool)

#1.convert matrix to file version
def ConVert(Redis):
    keys=Redis.keys()
    for key in keys:
        print('1')
        #Insert file key to db
        infoDict=json.loads(Redis.get(key))
        for path in infoDict:
            if Redis.exists(path):
                print('2')
                wordinfo=json.loads(Redis.get(path))
                wordinfo[key]=infoDict[path]
                #Redis.delete(path)
                Redis.set(('1235'+path),json.dumps(wordinfo))
            else:
                print('3')
                dict={'huang':0}
                Redis.set(path,json.dumps(dict))
#2.now we get the fileDict Try KNN
def calcKNN(wordDict, path):
    pass


def TryKNN(Redis,newfile):
    #1, deal with new file
    wordlist=PreProcessing(newfile)
    wordDict={}
    KNNList={}
    IDF=CalcIDF(Redis,newfile)
    for word in wordlist:
        wordDict[word]=json.dumps(Redis.get(word))
    #2.calc KNN
    paths=Redis.keys()
    for path in paths:
        KNN=calcKNN(wordDict,path)
        KNNList.append({path,KNN})
    max=0
    maxpath=''
    for item in KNNList:
        if item[path]>max:
            max= item[path]
            maxpath=path

    print (maxpath,"is the nearnest Neighbor")

def KNNmain():
    # 1.预处理测试集
    Dict={}
    input='C:\\20news-18828\\comp.graphics\\37261'
    input_wordlist=PreProcessing(input)
    #print(input_wordlist)
    for word in input_wordlist:
        ##预处理Dict
        Dict[word]=0
    for word in Dict:
        if Redis.exists(word):
            Dict[word]=json.loads(Redis.get(word))
    # 2. 测试比较
    #挑出最大的tfidf,然后剔除，以此类推获得前k个最近的group
    K =1 #can be changed by need
    while K:
        K-=1
        max=0
        maxpath=''
        for word in Dict:
            info=Dict[word]
            if info ==0:
                continue
            for path in info:
                if info[path]>max:
                    max=info[path]
                    maxpath=path
        print(maxpath)
        Dict.pop(maxpath)
    print('finishing....')
fileDict1={}
def createfileDict(rootdir):
    list = os.listdir(rootdir)
    print(list)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isdir(path):
           createfileDict(path)
        elif os.path.isfile(path):
            fileDict1[path]=0


def FindInRedis(file):
    keys=Redis.keys()
    worddict={}
    for key in keys:
        info=json.loads(Redis.get(key))
        if file in info.keys():
            worddict[key]=info[file]
    return worddict



def fillinFileDict(fileDict1):
    for file in fileDict1:
        worddict=FindInRedis(file)
        fileDict1[file]=worddict
        print('123')

def calcKNN(input,fileDict1):
    wordList=PreProcessing(input)
    s=0
    for file in fileDict1:
        info=fileDict1[file]
        for item in info:
            if item in wordList:
                s+=pow((wordList[item]-info[item]),2)
    return s
if __name__=='__main__':

    root='C:\\20news-18828'
    createfileDict(root)
    print(fileDict1)
    fillinFileDict(fileDict1)
    f=open('C:\\20news-18828\\test','w',errors='ignore')
    f.write(fileDict1)
    filedir='C:\\20news-18828\\test'
    slist=[]
    for file in filedir:
        s=calcKNN(file,fileDict1)
        slist.append(s)
