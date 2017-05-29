import filewalker
from pyltp import Segmentor
import pickle
import os
def wordbucketdict(indexto10):
    #wordscounter=pickle.load(open('wordscounter','rb'))
    #dupwordscount=wordscounter.most_common(indexto10)
    wordCHI=pickle.load(open('wordCHI','rb'))
   
    wordscount=[x for x in wordCHI.items() if x[1]>100]
    dupwordscount=sorted(wordscount,key=lambda t:-t[1])
    print (len(dupwordscount))
    index=0
    result={}
    for s in dupwordscount:
        result[s[0]]=index
        index+=1
    return result
def main():
    rootdir='./trec06c/data'
    #stortdir='./wordbucket'
    stortdir='./wordCHIbucket'
    
    errcount=0
    segmentor = Segmentor()
    segmentor.load("/home/curtank/Documents/ltp_data/cws.model")
    bucketsize=10000

    worddict=wordbucketdict(bucketsize)
    for f,filename,parent in filewalker.walkinrootdir(rootdir):
        bucket=[0 for i in range(bucketsize)]
        try:
            contextbeginflag=False
            for line in f: 
                if line=="\n":
                    contextbeginflag=True
                if contextbeginflag==False:
                    continue
                #print(line)
                words = segmentor.segment(line)
                for word in words:
                    if word in worddict:
                        bucket[worddict[word]]+=1
            
            storefilename=stortdir+'/'+parent.split('/')[-1]
            if os.path.exists(storefilename):
                pass
            else:
                os.makedirs(storefilename)
            f=open(storefilename+'/'+filename,'wb')
            pickle.dump(bucket,f,protocol=2)
        except:
            print('err'+parent+'/'+filename)
            errcount+=1
            
            pass
        
    print (errcount)

if __name__ == '__main__':
    #worddict=wordbucketdict(10000)
    #print(len(worddict))
    main()
    