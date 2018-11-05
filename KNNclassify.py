import json

import redis

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



if __name__=="__main__":
    ConVert(Redis)
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




