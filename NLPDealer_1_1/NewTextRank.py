# -*- coding: utf-8 -*-
# By Begoenix

from __future__ import absolute_import, unicode_literals
from operator import itemgetter
from collections import defaultdict
import jieba.posseg 
import numpy as np
import random
from jpype import *
from rest import Dealer



class WordsDealer():

    def __init__(self):
        self.type = ""

    def HanlpDealer(self,sentence = list):
        OutCome = []
        for i in sentence:
            i = i.toString()
            OutCome += [(i[:i.index("/")],i[i.index("/")+1:])]

        return OutCome



class UndirectWeightedGraph():
    d = 0.85


    def __init__(self,Type):
        if Type == "G":
            self.graph = defaultdict(list)
        elif Type == "V":
            self.graph = defaultdict(dict)
        self.type = Type

    def addEdge(self,start,end,weight):
        if self.type == "G":
            self.graph[start].append((start,end,weight))
            self.graph[end].append((start,end,weight))
        else:
            raise("方法调用不符合图表类型,该图表是{}".format(self.type))

    def addPair(self,former,later,weight):
        if self.type == "V":
            tem = self.graph[former]
            if later in tem:
                tem[later] += weight
            else:
                tem[later] = weight
        else:
            raise("方法调用不符合图表类型,该图表是{}".format(self.type))


    def rank(self,itime):
        ws = defaultdict(float)
        outSum = defaultdict(float)

        wsdef = 1.0/(len(self.graph) or 1.0)
        for name,out in self.graph.item():
            ws[name] = wsdef
            outSum[name] = sum((e[2] for e in out), 0.0)

        sorted_keys = sorted(self.graph.keys())
        for x in range(itime):
            for n in sorted_keys:
                s = 0
                for e in self.graph[n]:
                    s += e[2] / outSum[e[1]] * ws[e[1]]
                ws[n] = (1 - d) + d * s

        return ws


#直接输入切好的词的list，标准格式为(word,wp)
class NewTextRank():

    def __init__(self):
        self.span = 6
        emotion = "?"#此处需要一个tuple来保存情绪词语
        self.Dealer = Dealer()
        
        

    def selecter(self,inlist,allowed_list = list,special_list = list):
        outlist = []
        for i in inlist:
            wp = i[1]
            if wp in special_list:
                outlist += [i]
            else:
                for j in allowed_list:
                    if wp[0] == j :
                        outlist += [i]
                        break
        return outlist
        #return"?"#判断是否是形容词后返回词语


    def OriginTextRank(self,words,itime):
        tem_words = list
        new_words = defaultdict(int)
        for i in range(len(words)):
            name = words[i][0]
            wp = words[i][0]
            if self.selected(wp):
                tem_words += [words[i]]
        for i in range(len(tem_words)):
            for j in range(i+1,i+span):
                if j >= len(tem_words):
                    break
                new_words[(tem_words[i][0],tem_words[j][0])] += 1
                
        for terms,w in new_words.items():
            self.graph.addEdge(terms[0],terms[1],w)
        nodes_rank = self.graph.rank(itime)

        return nodes_rank

    def PairRank(self,d,words,center,itime,Graph = False,wanted_name = False,enhanced = False):
        GS = UndirectWeightedGraph(Type = "G")
        WordGraph = defaultdict(int)
        WordPair = defaultdict(int)
        for i in range(len(words)):
            word = words[i]
            wp_now = words[i][1]
            
            best_word = tuple
            best_fre = 0
            try:
                refer_dict = self.Dealer.PairReader(word)
            except KeyError:
                continue
                
            tem_list = []
            for j in range(i+1,len(words)):
                word_next = words[j]
                wp_next = words[j][1]
                if wp_now[0] == "v" and wp_next[0] != "v":
                    tem_list += [word_next]
                elif wp_now[0] != "v" and wp_next[0] == "v":
                    tem_list += [word_next]                    
            for m in range(len(tem_list)):
                words_ite = tem_list[m]
                try:
                    if d**m*refer_dict[words_ite] > best_fre:
                        best_words = words_ite
                        
                        best_fre = refer_dict[words_ite]
                except KeyError:
                    refer_dict[words_ite] = 1
                    if d**m*refer_dict[words_ite] > best_fre:
                        best_words = words_ite
                        
                        best_fre = refer_dict[words_ite]

            WordPair[(word,best_words)] += 1

        for terms,w in WordPair.items():
            GS.addEdge(terms[0],terms[1],w)

        ws = defaultdict(float)
        OutSum = defaultdict(float)
        centerword = tuple

        for name,out in GS.graph.items():
            if name[0] == center:
                ws[name] = 1
                centerword = name
            else:
                ws[name] = 1/(len(GS.graph))
            OutSum[name] = sum(e[2] for e in out)


        sorted_keys = sorted(GS.graph.keys())   
        
        for x in range(itime):
            for n in sorted_keys:
                if ws[n] > ws[centerword]:
                    ws[centerword] = ws[n]
            for n in sorted_keys:
                s = 0
                for e in GS.graph[n]:
                    s += e[2] / OutSum[e[1]] * ws[e[1]]
                ws[n] = (1 - d) + d * s
        sorted_graph = sorted(ws.items(),key = lambda x : x[1],reverse = True)

        if Graph:
            return GS.graph[name]
        else:
            return sorted_graph


    


    #标准词向量为15个
    def Comparer(graph,comparer = "DataFrame",length = 15):
        graph = graph[:length]
        comparer = comparer.head(15)
        series_test = pd.DataFrame([i for i in graph.items()],index = [j for j in graph.key()],columns = ["test"])
        best_match = ""
        best_cos = -1
        for i in range(len(compare.columns)):
            series_refer = compare[compare.columns[i]]
            tem_data = pd.concat([series_test,series_refer],axis = 1)
            tem_data.fillna(0, inplace = True)
            cos = (sum(tem_data[0][v]*tem_data[1][v] for v in range(len(tem_data))))/(sum((tem_data[0][v1])**2 for v1 in range(len(tem_data)))*sumsum((tem_data[1][v1])**2 for v1 in range(len(tem_data))))
            if cos > best_cos:
                best_match = compare.columns[i]
                best_cos = cos
        return best_match
            
            
            
                    
                


    def NVNPair(self,words = list,target_flag = True):
        NVwords = defaultdict(int)
        VNwords = defaultdict(int)
        former = ""
        later = ""
        x_flag = 0
        start = 0
        for i in range(len(words)):
            if "n" in words[i][1]:
                former = words[i]
                start = i
                break
            elif "v" in words[i][1]:
                later = words[i]
                start = i
                break
        for i in range(start+1,len(words)-1):
            if "n" in words[i][1] and later != "" and former == "" and words[i+1][0] != "的" and words[i][1] != "vn":
                VNwords[(later,words[i])] += 1
                later = ""
                former = words[i]
        
            if "n" in words[i][1] and later == "" and former != "":
                former = words[i] 
            if "v" in words[i][1] and former != "" and later == "" and words[i+1][0] != "的" :
                NVwords[(former,words[i])] += 1
                former = ""
                later = words[i]
            if words[i][1] == "vn" and former != "" and later == "" and words[i+1][0] != "的":
                NVwords[(former,words[i])] += 1
                former = ""
                later = words[i]
            if "v" in words[i][1] and former == "" and later != "":
                later = words[i]
            if "w" in words[i][1]:
                former = ""
                later = ""
                for j in range(i+1,len(words)-1):
                    if "n" in words[j][1]:
                        former = words[j]
                
                        break
                    elif "v" in words[j][1]:
                        later = words[j]
                        
                        break
        if target_flag:        
            NVgraph = UndirectWeightedGraph(Type = "V")
            VNgraph = UndirectWeightedGraph(Type = "V")
            for terms,w in NVwords.items():
                NVgraph.addPair(terms[0],terms[1],w)
            for terms,w in VNwords.items():
                VNgraph.addPair(terms[0],terms[1],w)

        else:
            NVgraph = NVwords
            VNgraph = VNwords
        
        #生成值为{():{():int}}
        return NVgraph,VNgraph
        
                
                
                
                
        
        
            
        
