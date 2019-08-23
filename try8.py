from jpype import *
import pandas as pd
from collections import defaultdict
import time
import os,sys
from NewTextRank import WordsDealer, UndirectWeightedGraph, NewTextRank
reference = {("中国","v"):[(("敌视","v"),1),(("属于","v"),1),(("超过","v"),1),(("建设","v"),1)],("西方","v"):[(("敌视","v"),1),(("远离","v"),1),(("超过","v"),1)],("成都","v"):[(("属于","v"),1),(("建设","v"),1),(("远离","v"),1),(("敌视","v"),1)],("属于","v"):[(("西方",'v'),1),(("中国","v"),1),(("成都","v"),1)],("敌视","v"):[(("中国","v"),1),(("西方","v"),1),(("成都","v"),1)],("建设","v"):[(("中国","v"),1),(("西方","v"),1),(("成都","v"),1)],("远离","v"):[(("中国","v"),1),(("西方","v"),1),(("成都","v"),1)],("超过","v"):[(("成都","v"),1),(("西方","v"),1),(("中国","v"),1)]}

sentence = '成都属于中国，中国超过西方，西方敌视中国，中国建设成都，西方远离成都，成都敌视西方，中国建设成都,中国建设成都,中国建设西方'
WordsDealer = WordsDealer()
startJVM(getDefaultJVMPath(),r"-Djava.class.path=C:\Program Files\nlpapi\Hanlp\hanlp-1.7.4\hanlp-1.7.4.jar;C:\Program Files\nlpapi\Hanlp\hanlp-1.7.4","-Xms1g","-Xmx1g")
StandardTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
list1 = StandardTokenizer.segment(sentence)
words = WordsDealer.HanlpDealer(list1)
newwords = []
for i in words:
    wp = i[1]
    if "n" in wp or "v" in wp or "f" in wp:
        newwords += [i]
graph = NewTextRank.PairRank(d = 0.8,words = newwords,center = "成都",itime = 1000,reference = reference)
print(graph)
    
