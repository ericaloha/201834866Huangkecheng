import codecs
import string
import  nltk
from nltk.corpus import stopwords
def DealwithFile(filename):
    #fw = codecs.open(filename, 'r', )
    f = open(filename,'r',errors='ignore')
    text = f.read()
    #去除读取文件后的格式（换行 缩进）
    text = text.replace('\r',' ').replace('\n',' ').replace('\t',' ')
    remove_digits = str.maketrans('', '', string.digits)
    text = text.translate(remove_digits)
    f.close()
    return text
#(2)去除标点和大写,数字，分词
def remove_tokens(text):
    lowers = text.lower()  # 大小写
    # 去除标点符号
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    no_punctuation = lowers.translate(remove_punctuation_map)
    tokens = nltk.word_tokenize(no_punctuation)
    return tokens

#（2）提取词干
def Stemming(wordlist):
    LancasterStem = nltk.LancasterStemmer()
    stemmed = []
    for item in wordlist:
        root=LancasterStem.stem(item)
        stemmed.append(root)
    return stemmed


#(3)移除stopwords
def remove_stopwords(wordlist):
    filtered = [w for w in wordlist if not w in stopwords.words('english')]  # 过滤stopwords
    return filtered



#orgnize_preProcessing
#input:filname
#output:words in the file saving in a list
def PreProcessing(filename):
    text=DealwithFile(filename)
    wordlist1 = remove_tokens(text)
    wordlist2 = Stemming(wordlist1)
    wordlist3 = remove_stopwords(wordlist2)
    return wordlist3


if __name__== '__main__':
    path="C:\\Users\\eric\\SDU\\实验\\专业课实验\\DataMining\\20news-18828\\alt.atheism\\49960"
    print(PreProcessing(path))
    #nltk.download()


