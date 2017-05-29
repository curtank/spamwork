import sys
from pyltp import Segmentor
import os
from collections import Counter
import pickle
import numpy as np

def main():
    rootdir='./trec06c/data'
    segmentor = Segmentor()
    segmentor.load("/home/curtank/Documents/ltp_data/cws.model")

    errcount=0
    totalwordsset=set()
    positiveappear=Counter()
    negetiveappear=Counter()
    positivenum=0
    negetivenum=0
    labels=pickle.load(open('labels','rb'))
    print(positivenum)
    print(negetivenum)
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            index=parent[14:]+'/'+filename
            label=labels[index]
            try:
                f=open(parent+'/'+filename,'r',encoding='gb18030')
                contextbeginflag=False
                wordset=set()
                for line in f:
                    if line=="\n":
                        contextbeginflag=True
                    if contextbeginflag==False:
                        continue
                    #print(line)
                    words = segmentor.segment(line)
                    for word in words:
                        wordset.add(word)
                        totalwordsset.add(word)
                for word in wordset:
                    if label==1:
                        positiveappear[word]+=1
                        
                    else:
                        negetiveappear[word]+=1
                if label==1:
                    positivenum+=1
                else:
                    negetivenum+=1
                pass
            except:
                print('err'+parent+'/'+filename)
                errcount+=1
               
    print(positivenum)
    print(negetivenum)
    pickle.dump([positivenum,negetivenum],open('pnnum','wb'))
    pickle.dump(negetiveappear,open('negetiveappear','wb'))
    pickle.dump(positiveappear,open('positiveappear','wb'))
    pickle.dump(totalwordsset,open('totalwordsset','wb'))
    print(len(wordset))
    print(errcount)
    segmentor.release()
    wordCHI={}
    positivenum,negetivenum=pickle.load(open('pnnum','rb'))
    positiveappear=pickle.load(open('positiveappear','rb'))
    negetiveappear=pickle.load(open('negetiveappear','rb'))
    totalwordsset=pickle.load(open('totalwordsset','rb'))
    for word in totalwordsset:
        N=positivenum+negetivenum
        A=positiveappear[word]/N
        B=negetiveappear[word]/N
        C=(positivenum)/N-A
        D=(negetivenum)/N-B
        smoth=0.00001
        wordCHI[word]=N*((A*D-B*C)**2)/(A+C+smoth)/(A+B+smoth)/(B+D+smoth)/(B+C+smoth)
        pass
    
    from collections import OrderedDict
    s=OrderedDict(sorted(wordCHI.items(),key=lambda t: -t[1]))
    #print(s)
    pickle.dump(wordCHI,open('wordCHI','wb'))
    
    pass

if __name__ == '__main__':
    #main()
    wordCHI=pickle.load(open('wordCHI','rb'))
    s=[x for x in wordCHI.items() if x[1]>500.25]
    print(s)
    print(len(s))



