import json
import string

import redis

from Vsm.preProcessing import PreProcessing

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password=123456, db=0)
Redis = redis.Redis(connection_pool=pool)

keys=Redis.keys()
print(keys)
for key in keys:
    key=key.decode()
    print(key)
    print(key[0:3])
    if key[0:3] == '123':
        Redis.delete(key)
        print('1')

def Convert(Redis):
    keys=Redis.keys()
    for key in keys :
        info=json.loads(Redis.get(key))
        #print(info)
        for path in info:
            pathkey=path
            pathkey=pathkey.rstrip(string.digits)
            pathkey = '12315' + pathkey
            if not Redis.exists(pathkey):

                Redis.set(pathkey,json.dumps({'huang':0}))
                print('2')
            else:
                WordInfo=json.loads(Redis.get(pathkey))
                s=''
                if key in WordInfo.keys():
                    s=WordInfo[key.decode()]
                    WordInfo[key.decode()]=info[path]+s
                else:
                    WordInfo[key.decode()] = info[path]
                Redis.set(pathkey,json.dumps(WordInfo))
                print('1')


def localtf(item):



def localidf(word):
    pass


def CalculateKNN(file1,file2):
    pass


def CalKNN(Redis,Inputfile):
    InputWordList=PreProcessing(Inputfile)
    InputWordDict={}
    for item in InputWordList:
        InputWordDict[item]=localtf(item)*localidf(item)
    keys=Redis.keys()
    for key in keys:
        if key[0:3] == '123':
            continue
        else:
            Redis.delete(key)
    print('update finishing..')
    files=Redis.keys()
    cosList=[]
    for file in files:
        cos=CalculateKNN(json.loads(Redis.get(file)),InputWordDict)
        cosList.append({file:cos})
    print("KNN Processing finished")
    cosList.sort()
    print(cosList[0][0],"  :::  ",cosList[1][0],"--------- are likey to be the same as input...")



if __name__=="__main__":
    Convert(Redis)
    print('finishing')
