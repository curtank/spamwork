import pickle
def generate():
    filename='./trec06c/full/index'
    labels={}
    for line in open(filename):
        word=line.split()
        if len(word)!=2:
            raise Exception(line+'spliterr')
        if word[0].lower()=='spam':
            labels[word[1][7:]]=1
        elif word[0].lower()=='ham':
            labels[word[1][7:]]=0
        else:
            raise Exception(line+'labelerr')
    pickle.dump(labels,open('labels','wb'),protocol=2)

def getlabels():
    return pickle.load(open('labels','rb'))
def main():
    generate()
    

if __name__ == '__main__':
    #main()
    print getlabels()