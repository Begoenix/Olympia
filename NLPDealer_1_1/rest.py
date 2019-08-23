import json,os
import codecs
import sys
from collections import defaultdict


class Dealer():

    def __init__(self):
        self.size = 0
        
    def PairReader(self,key,encode = "gbk"):


        DictOut = defaultdict(int)
        st = ""
        
        with open("Data/{}/{}.txt".format(key[1],key[0]),"r",encoding = encode) as f:
            for line in f:
                st += line

        DictIn = eval(st)
                

        for k,v in DictIn.items():

            DictOut[k] = v
            

        return DictOut

    #针对defaultdict使用
    def PairSaver(self,DictIn,key,encode = "gbk"):

        DictOut = {}

        for k ,v in DictIn.items():
            
            DictOut[k] = v

        with open("Data/{}/{}.txt".format(key[1],key[0]),"w",encoding = encode)as f:
            f.write(str(DictOut))
            f.write("\n")

        return "Done"
    

    

    def VectorRenewer(self,add,key):
        st = ""
        try:
            with open ("Data/{}/{}.txt".format(key[1],key[0]),"r",encoding = "gbk") as f:
                for line in f:
                    st += line
            old = eval(st)
            for k,v in add.items():
                if k in old:
                    old[k] += v
                else:
                    old[k] = v

            with open ("Data/{}/{}.txt".format(key[1],key[0]),"w",encoding = "gbk") as f:
                f.write(str(old))
                f.write("\n")

        except FileNotFoundError:
            if os.path.exists("Data/{}".format(key[1])):
                with open ("Data/{}/{}.txt".format(key[1],key[0]),"w",encoding = "gbk") as f:
                    f.write(str(add))
                    f.write("\n")
            else:
                path = r'E:\量化\ONE\Data\{}'.format(key[1])
                os.makedirs(path)
                with open ("Data/{}/{}.txt".format(key[1],key[0]),"w",encoding = "gbk") as f:
                    f.write(str(add))
                    f.write("\n")
                    
                    
                
                
                    
                    
                
        

    
                
        
        
