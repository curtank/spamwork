import os
def walkinrootdir(rootdir):
    errcount=0
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            try:
                f=open(parent+'/'+filename,'r',encoding='gb18030')
                yield f,filename,parent
            except:
                print('err'+parent+'/'+filename)
                errcount+=1
                pass
def main():
    rootdir='./trec06c/data'
    for f,_,_ in walkinrootdir(rootdir):
        print(f)
        pass

if __name__ == '__main__':
    main()