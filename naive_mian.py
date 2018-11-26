import os
import numpy as np
from textblob import *
import string
import re
import math

word_freq_train = {}  
word_freq_test = {}     


cur_train_path = './data'    
cur_test_path = './test'


def Preprocess(doc_name, save_name, stop_words, flag):
    global word_freq_train
    global word_freq_test

    with open(doc_name, 'rb') as f:     
        doc_content = f.read()         
    doc_content = str(doc_content, encoding='latin2')   

    regex = re.compile('[%s]' % re.escape(string.punctuation))
    doc_content = regex.sub(' ', doc_content)   
    res = TextBlob(doc_content)     
    res = TextBlob.lower(res)      

    word_list = []      # record the word appeared in the document in order
    word_count = {}     # define a dict {word : count}  record the count of a word in the document; for the word_freq

    for word in res.words:
        word = Word.singularize(word)  
        word = Word.lemmatize(word)    

        if word in stop_words:
            continue                    
        if word.isdigit():              
            continue
        word_list.append(word)         

        if word not in word_count.keys():  
            word_count[word] = 1
        else:
            word_count[word] += 1

    for item in word_count.items():
        w = item[0]
        c = item[1]

        if flag == 1:   # train set
            if w not in word_freq_train.keys():        
                word_freq_train[w] = c
            else:
                word_freq_train[w] += c
        else:           # test set
            if w not in word_freq_test.keys():
                word_freq_test[w] = c
            else:
                word_freq_test[w] += c

    with open(save_name, 'w', encoding='latin2') as f:     
        f.write(' '.join(word_list))


def LoadFileForProcess():

    global word_freq_train
    global word_freq_test

    sw = []
    with open('./data/stopwords') as f:
        for line in f:
            line = line.rstrip()
            sw.append(line)

    doc_path = 'proj_1/data/20news-18828'
    for doc_dir in os.listdir(doc_path):    
        save_dir_test = os.path.join(cur_test_path, doc_dir)
        if not os.path.exists(save_dir_test):
            os.mkdir(save_dir_test)
        save_dir_train = os.path.join(cur_train_path, doc_dir)
        if not os.path.exists(save_dir_train):
            os.mkdir(save_dir_train)

    result = np.load('./data/train_doc.npy')
    train_doc = result.item()
    result = np.load('./data/test_doc.npy')
    test_doc = result.item()

    train_doc_list = []
    train_doc_class = []
    for it in train_doc.items():
        train_doc_list.append(it[0])
        train_doc_class.append(it[1])

    test_doc_list = []
    test_doc_class = []
    for it in test_doc.items():
        test_doc_list.append(it[0])
        test_doc_class.append(it[1])

    for i in range(len(train_doc_list)):
        save_path = os.path.join(cur_train_path, train_doc_list[i][25:])
        Preprocess(train_doc_list[i], save_path, sw, 1)
        print(save_path)

    for i in range(len(test_doc_list)):
        save_path = os.path.join(cur_test_path, test_doc_list[i][25:])
        Preprocess(test_doc_list[i], save_path, sw, 0)
        print(save_path)

    np.save('./data/word_freq_train.npy', word_freq_train)
    np.save('./data/word_freq_test.npy', word_freq_test)


def ProcessTraining(thres):

    class_word = {}            
    class_word_number = []     
    class_propor = []           
    class_propor_log = []      
    class_word_propor = {}     
    class_word_propor_log = {}  
    class_name = []
    word_list = []

    result = np.load('./data/word_freq_train.npy')
    word_freq_train_ = result.item()

    for doc_dir in os.listdir(cur_train_path):
        class_name.append(doc_dir)

    for it in word_freq_train_.items():
        w = it[0]
        c = it[1]
        print('%s   %d' % (it[0], it[1]))
        if c >= thres:
            word_list.append(w)
    for it in word_list:
        print(it)

    for doc_dir in os.listdir(cur_train_path):
        class_number = class_name.index(doc_dir)
        # print('class number is %d' % class_number)
        file_path = os.path.join(cur_train_path, doc_dir)
        for doc in os.listdir(file_path):
            doc_path = os.path.join(file_path, doc)
            print(doc_path)

            content = []
            with open(doc_path, 'r', encoding='latin2') as f:
                for line in f:
                    content = line.split()

            word_count = {}
            for word in content:
                if word not in word_list:
                    continue
                if word not in word_count.keys():  
                    word_count[word] = 1
                else:
                    word_count[word] += 1

            for it in word_count.items():
                w = it[0]
                c = it[1]
                if class_number not in class_word.keys():
                    class_word[class_number] = {w: c}
                else:
                    if w not in class_word[class_number].keys():
                        class_word[class_number][w] = c
                    else:
                        class_word[class_number][w] += c
            # print("pass!")
    np.save('./data/class_word.npy', class_word)



def cacl_nb_necessary():
    class_word_number = []      
    class_propor = []          
    class_propor_log = []      
    class_word_propor = {}     
    class_word_propor_log = {} 
    word_list = []

    result = np.load('./data/class_word.npy')
    class_word = result.item()  

    for it in class_word.items():
        c_n = it[0]
        for it1 in it[1].items():
            print('%d  %s  %d' % (c_n, it1[0], it1[1]))

    total_number = 0
    for it in class_word.items():
        class_total = 0
        for it1 in it[1].items():
            class_total += it1[1]
        class_word_number.append(class_total)
        total_number += class_total

    for i in range(len(class_word)):
        class_propor.append(class_word_number[i]/total_number)
        class_propor_log.append(math.log(class_word_number[i]/total_number))

    for it in class_word.items():
        for it1 in it[1].items():
            w = it1[0]
            if w not in word_list:
                word_list.append(w)
    word_list_length = len(word_list)

    for it in class_word.items():
        c_n = it[0]
        for it1 in it[1].items():
            w = it1[0]
            c = it1[1]

            propor = (c+1)/(class_word_number[c_n]+word_list_length)
            propor_log = math.log((c+1)/(class_word_number[c_n]+word_list_length))

            if c_n not in class_word_propor.keys():
                class_word_propor[c_n] = {w: propor}
            else:
                class_word_propor[c_n][w] = propor

            if c_n not in class_word_propor_log.keys():
                class_word_propor_log[c_n] = {w: propor_log}
            else:
                class_word_propor_log[c_n][w] = propor_log
    np.save('./data/class_propor_log.npy', class_propor_log)
    np.save('./data/class_word_propor_log.npy', class_word_propor_log)
    np.save('./data/class_word_number.npy', class_word_number)
    np.save('./data/word_list.npy', word_list)


def ProcessTesting(thres):
    result = np.load('./data/word_freq_test.npy')
    word_freq_test_ = result.item()
    word_list_test = []

    for it in word_freq_test_.items():
        w = it[0]
        c = it[1]
        if c >= thres:
            word_list_test.append(w)

    for doc_dir in os.listdir(cur_test_path):
        doc_dir = os.path.join(cur_test_path, doc_dir)
        for doc in os.listdir(doc_dir):
            doc = os.path.join(doc_dir, doc)
            new_content = []
            with open(doc, 'r', encoding='latin2') as f:
                for line in f:
                    content = line.split()
            for word in content:
                if word in word_list_test:
                    new_content.append(word)
            with open(doc, 'w', encoding='latin2') as f:
                f.write(' '.join(new_content))

def NavieBayes():
    result = np.load('./data/class_propor_log.npy')
    class_propor_log = list(result)
    result = np.load('./data/class_word_propor_log.npy')
    class_word_propor_log = result.item()
    result = np.load('./data/class_word_number.npy')
    class_word_number = list(result)
    result = np.load('./data/word_list.npy')
    word_list = list(result)
    result = np.load('./data/test_doc.npy')
    test_doc = result.item()
    word_list_length = len(word_list)

    test_doc_list = []
    test_doc_class = []
    for it in test_doc.items():
        test_doc_list.append(it[0])
        test_doc_class.append(it[1])

    correct_number = 0
    for i in range(len(test_doc_list)):
        file_path = os.path.join(cur_test_path, test_doc_list[i][25:])
        content = []
        with open(file_path, 'r', encoding='latin2') as f:
            for line in f:
                content = line.split()
        prob = []
        for k in range(20):
            s = class_propor_log[k]
            for word in content:
                if word in class_word_propor_log[k].keys():
                    s += class_word_propor_log[k][word]
                else:
                    s += math.log(1/(class_word_number[k]+word_list_length))
            prob.append(s)

        max_index = 0
        for j in range(20):
            # print(prob[j])
            if prob[j] > prob[max_index]:
                max_index = j
        if max_index == test_doc_class[i]:
            correct_number += 1
            print('correct!  %d/%d' % (i, len(test_doc_list)))
        else:
            print('wrong!  %d/%d' % (i, len(test_doc_list)))

    accuracy = correct_number/len(test_doc_list)
    print('Accuracy:  {:.4f}'.format(accuracy))


def open_doc():
    with open('./data/test/alt.atheism/49960', 'r', encoding='latin2') as f:
        for line in f:
            content = line.split()
    for it in content:
        print(it)


if __name__ == '__main__':
    NavieBayes()
    print('finish')
