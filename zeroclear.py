rootdir='./wordbucket'
import pickle
import os
zerofile=[]
for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        try:
            f=open(parent+'/'+filename,'rb')
            s=pickle.load(f)
            f.close()
            if sum(s)==0:
                zerofile.append(parent+filename)
                os.remove(parent+'/'+filename)     
        except:
            print('err'+parent+'/'+filename)
            errcount+=1
            pass
print(len(zerofile))