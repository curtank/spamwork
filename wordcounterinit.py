import sys
f=open('./trec06c/data/000/002','r',encoding='gb18030')
for line in f:
    print(line)
from pyltp import Segmentor
segmentor = Segmentor()
segmentor.load("/home/curtank/Documents/ltp_data/cws.model")
words = segmentor.segment("元芳你怎么看")
print( "|".join(words))

import os
from collections import Counter
import generatelabels
rootdir='./trec06c/data'
errcount=0
wordset=[]
wordscounter=Counter()
positiveappear=Counter()
negetiveappear=Counter()
positiveabse=Counter()
negetiveabse=Counter()
labels=generatelabels.getlabels()
for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        index=parent[14:]+'/'+filename
        label=labels[index]
        try:
            f=open(parent+'/'+filename,'r',encoding='gb18030')
            contextbeginflag=False
            for line in f:
                if line=="\n":
                    contextbeginflag=True
                if contextbeginflag==False:
                    continue
                #print(line)
                words = segmentor.segment(line)
                for word in words:
                    wordscounter[word]+=1
            pass
        except:
            print('err'+parent+'/'+filename)
            errcount+=1
            pass


import pickle
pickle.dump(wordscounter,open('wordscounter','wb'))
print(len(wordset))
print(errcount)
segmentor.release()