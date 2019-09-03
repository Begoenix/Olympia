# -*- encoding: gbk -*-
# By Begoenix


from __future__ import absolute_import, unicode_literals
from operator import itemgetter
import networkx as nx
import random as rd
from collections import defaultdict




#-------------------------------ScoreInitializer--------------------------------
#===============================================================================



class VertexInitializer():
    """��Hanlp�����ķִʽ��Ϊ��׼��̬����"word/wp"����list����ʽչʾ��

    ��obj = ['word1/wp1','word2/wp2'......]

    �����н���̬Ϊ������Ե�Ԫ����ɵ�list��

    ��self.object = [(word1,wp1),(word2,wp2)......]
    
    ����Ľ��Ϊһ��������Ԫ��Ϊkey���ֵ䣬ֵΪȨ��,

    ��self.score = {word1:weight1,word2:weight2......}

    """
    
    def __init__(self, obj):
        list_word = []
        
        for word in obj:
            tem = word.split("/")
            tuple_word = (tem[0], tem[1])
            list_word += [tuple_word]
            
        self.object = list_word
        self.score = defaultdict(float)
        

        
class RandomScoreInitializer(VertexInitializer):
    """����random��������Ȩ�ؽ��г�ʼ��"""
    

    def __init__(self, obj):
        self.type = "RANDOM"
        super(RandomScoreInitializer, self).__init__(obj)

    def unit(self):
        """��ʼ��Ȩ����0-1֮��"""

        for word in self.object:
            self.score[word] = rd.random()

        return self.score

    def radint(self, start, end):
        """��ʼ��Ȩ��Ϊ����������֮��ȡ�����ֵ"""

        for word in self.object:
            self.score[word] = rd.randint(start, end)

        return self.socre

    def uniform(self, start, end):
        """��ʼ��Ȩ��Ϊ��������֮��ȡ�������ֵ"""

        for word in self.object:
            self.score[word] = rd.uniform(start, end)

        return self.score

        

        


class AverageScoreInitializer(VertexInitializer):
    """ƽ������ʼ��"""


    def __init__(self, obj):
        self.type = "AVERAGE"
        super(AverageScoreInitializer, self).__init__(obj)

    def simple(self):
        for word in self.object:
            self.score[word] = 1/len(self.object)

        for k,v in self.score.items():
            self.score[k] = 1/len(self.score)

        return self.score



class CustomeInitializer(VertexInitializer):
    """ʹ�����е��ֵ���и�Ȩ���ֵ�ĸ�ʽΪ{tuple1:weight1,tuple2:weight2......}"""


    def __init__(self, obj, reference):
        self.type = "CUSTOM"
        self.reference = reference
        super(CustomeInitializer,self).__init__(obj)
        
    def reference(self):
        for word in self.object:
            if word in self.reference:
                self.score[word] = self.reference[word]
            else:
                self.score[word] = 1 / len(sel.object)

        return self.score


#===============================================================================







#-------------------------------GraphConstructor--------------------------------
#===============================================================================


class GraphConstructor():
    """�ڵ�Ϊ�����ԵΪ�������ﰴ��ĳ��Ҫ��

    ��ʹ�����Զ����ʹ�õ�ǰ�汾��ʼ���ĺ�����ǰ����ֵĴ���

    �ڵ�ĳ�ʼ�����С�Ȩ�ء��������ԡ��롰�ôʳ��ֵĴ�������

    ��Ե������ֻ�С����ʹ�ͬ���ֵĴ�����

    ����֧���Զ������ԣ��������
    
    ��ʼ�������У�dict_weight�Ǵ���Ȩ�صĴʵ䣬

                  ��ʽΪ{(word1,wp1):weight1,(word2,wp2):weight2......}
    
                  list_relation�ǰ���ԭ�ķִʲ����������Ĵ��б�

                  ������ֵ��Ⱥ�˳�����������г��ֵ��Ⱥ�˳��Ϊ׼��

                  ��ʽΪ[(word1,wp1),(word2,wp2)......]
                  
    ʹ�õ�ͼ������networkx��
    
    """


    def __init__(self, dict_weight, list_relation):
        self.graph = nx.Graph(
                        wp = str, weight = float,
                        occur_times = int)
        self.dict_weight = dict_weight
        self.list_relation = list_relation

    def add_tag(self, tag_name, dict_tag, flag):
        """������Ӻ���������

                        tag_nameΪҪ��ӵ����ԣ�

                        dict_tagΪ��ΪĿ�����ƣ�ֵΪĿ��ֵ���ֵ䣻

                        flagΪ��Ҫ������Եı�ʶ��

                        "N"Ϊ��ڵ����ֵ��"E"Ϊ���Ե���ֵ

        dict_tag�������ʽӦΪ:

                        flagΪ"N"ʱ��
        
                        dict_tag

                        = {(word1,wp1):tag_value1,......}

                        flagΪ"E"ʱ��

                        dict_tag

                        = {(word1,word2):tag_value1,......}

        """
        
        if flag == "N":            
            for k,v in dict_tag.items():
                if k[0] in self.graph.nodes:
                    self.graph.add_node(k[0], tag_name = v)
                else:
                    self.graph.add_node(
                            k[0], wp = k[1],
                            weight = 1 / len(dict_tag),
                            occur_times = 0, tag_name = v)

        elif flag == "E":
            for k,v in dict_tag.items():
                if (k[0], k[1]) in self.graph.edges():
                    self.graph.add_edge(
                            k[0], k[1],
                            tag_name = v)
                    self.graph[k[0]][k[1]]["co_times"] += 1
                else:
                    self.graph.add_edge(
                            k[0], k[1],
                            co_times = 1, tag_name = v)

        



class CooccurenceConstructor(GraphConstructor):
    """�������ݴ���ǰ����ֹ�ϵΪ���ӵ�ͼ��"""


    def __init__(self, dict_weight, list_relation, span):
        """����

        spanΪ�����Ѱ�Ĵ�����

        ����spanΪ2ʱ��word1����������ʶ��������ӹ�ϵ���Դ����ơ�

        """
        
        self.type = "COOCCURENCE"
        super(CooccurenceConstructor,self).__init__(dict_weight, list_relation)

        
        for k,v in self.dict_weight.items():
            self.graph.add_node(
                    k[0], wp = k[1],
                    weight = v, occur_times = 0)


        for n in range(len(self.list_relation)):
            word_now = self.list_relation[n][0]
            num_now = n
            
            for w in range(num_now+1, num_now+1+span):
                if w >= len(self.list_relation):
                    break
                else:
                    word_next = self.list_relation[w][0]
                    if (word_now, word_next) in self.graph.edges():
                        self.graph[word_now][word_next]["co_times"] += 1
                    else:
                        self.graph.add_edge(word_now, word_next, co_times = 1)
                    self.graph.nodes[word_now]["occur_times"] += 1
                    self.graph.nodes[word_next]["occur_times"] += 1
                    






#===============================================================================







#----------------------------------TextRanker-----------------------------------
#===============================================================================

class TextRanker():
    """��֧��ʹ��networkx���������޷���ͼ"""
    

    def __init__(self, d, graph):
        """����

        dΪ����������

        graphΪ������޷���ͼ��

        """

        self.block = d
        self.graph = graph
        self.weight = dict # δ�����Ȩ�شʵ�
        self.sorted_dict = list # �����Ĵ����б�

    def rank(self, args = int):
        """��Graph����Walk, ��������Vertex Score

        ����argsΪ�����Ĵ���

        """
        for i in range(args):
            for word in self.graph.nodes():
                weight_sum = sum(self.graph.edges[word, e]["co_times"]
                                 * self.graph.nodes[e]["weight"]
                                 for e in self.graph.adj[word])
                
                occur_times = self.graph.nodes[word]["occur_times"]
                weight_final = weight_sum / occur_times
                                
                self.graph.nodes[word]["weight"] = \
                (1 - self.block) + self.block * weight_final

        self.weight = nx.get_node_attributes(self.graph, "weight")
        self.sorted_list = sorted(
                            self.weight.items(),
                            key = lambda x:x[1],
                            reverse = True)

    def get_tokens(self, threshold, withScore = True):
        """����score����threshold������token

        ��withScoreΪTrue���򷵻�һ�������Ĵʵ䣬��Ϊ�ʣ�ֵΪȨ��
        
        ��withScoreΪFalse���򷵻�һ���������б�����Ԫ��Ϊ��

        """

        list_out = []
        
        for k in self.sorted_list:
            if k[1] >= threshold:
                list_out += [k[0]]
            else:
                break

        if withScore:
            dict_out = {}
            for word in list_out:
                dict_out[word] = self.weight[word]
                
            return dict_out

        else:
            
            return list_out

    def get_topk(self, topk = int, withScore = True):
        """����topk������Ҫ��token

        ��withScoreΪTrue���򷵻�һ�������Ĵʵ䣬��Ϊ�ʣ�ֵΪȨ��
        
        ��withScoreΪFalse���򷵻�һ���������б�����Ԫ��Ϊ��
        
        """

        if withScore:
            dict_out = {}
            for i in range(topk):
                dict_out[self.sorted_list[i][0]] = \
                self.weight[self.sorted_list[i][0]]

            return dict_out

        else:
            list_out = []
            for i in range(topk):
                list_out += [self.sorted_list[i][0]]

            return list_out


    def get_token_score(self, token):
        """�����ض�token��score"""

        return self.weight[token]
            

        
        

        
        



    

    










    
