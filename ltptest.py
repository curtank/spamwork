#-*- coding: utf-8 -*-
from pyltp import Segmentor
segmentor = Segmentor()
segmentor.load("/home/curtank/Documents/ltp_data/cws.model")
words = segmentor.segment("于老师的父亲，王老爷子，爱去巴黎吃火烧，这么长的猪大肠，整根吃。")
segmentor.release()
print('\t'.join(words))
exceptposttag=['e','p','o','u','wp']
from pyltp import Postagger
postagger = Postagger() # 初始化实例
postagger.load('/home/curtank/Documents/ltp_data/pos.model')  # 加载模型
postags = postagger.postag(words)  # 词性标注
for i in range(0,len(words)):
    if postags[i] in exceptposttag:
        continue
    print(words[i])
print ('\t'.join(postags))
postagger.release()  # 释放模型

from pyltp import NamedEntityRecognizer
recognizer = NamedEntityRecognizer() # 初始化实例
recognizer.load('/home/curtank/Documents/ltp_data/ner.model')  # 加载模型
netags = recognizer.recognize(words, postags)  # 命名实体识别
print ('\t'.join(netags))
recognizer.release()  # 释放模型

from pyltp import Parser
parser=Parser()
parser.load('/home/curtank/Documents/ltp_data/parser.model')
arcs = parser.parse(words, postags)  # 句法分析
print ("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
parser.release()  # 释放模型

from pyltp import SementicRoleLabeller
labeller = SementicRoleLabeller() # 初始化实例
labeller.load('/home/curtank/Documents/ltp_data/srl')  # 加载模型
roles = labeller.label(words, postags, netags, arcs)  # 语义角色标注
for role in roles:
    print( role.index, "  ".join(
        ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
labeller.release()  # 释放模型