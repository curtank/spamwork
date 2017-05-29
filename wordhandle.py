import pickle
wordscounter=pickle.load(open('wordscounter','rb'))
#more than 10 frequence words
indexto10=10000
dupwordscount=wordscounter.most_common(indexto10)

print(dupwordscount)
