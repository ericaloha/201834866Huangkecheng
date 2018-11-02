import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password=123456, db=0)
Redis = redis.Redis(connection_pool=pool)



def Frequency(Redis,localdir,size):
    r=Redis.keys()
    length=len(r)
    entryDict={}
    i=0
    for k in r:

        if int(Redis.get(k))>size:
            i += 1
            entryDict[k] = Redis.get(k)
    print(i)
    f = open(localdir,'w',errors='ignore')
    f.write(str(entryDict))
    f.close()
    print('finish.')

if __name__ == '__main__':
    localdir = "C:\\Users\\eric\\SDU\\实验\\专业课实验\\DataMining\\Exp\\FrequentDict5.txt"
    Frequency(Redis,localdir,20)
