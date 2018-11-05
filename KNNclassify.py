
import json

import redis

from Vsm.preProcessing import PreProcessing
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password=123456, db=0)
Redis = redis.Redis(connection_pool=pool)


if __name__ == '__main__':
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

    



