# -*- coding: utf-8 -*-
# By Begoenix



from jpype import *
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException,TimeoutException, NoSuchElementException
import selenium.webdriver.support.ui as ui
import time
from selenium.webdriver import ActionChains
import random as rd
import re
from rest import Dealer
from NewTextRank import WordsDealer,UndirectWeightedGraph,NewTextRank
from PathDict import Xpath,Web


class NewsReader():
    

    def __init__(self,end_page = 0,Type = str):
        self.type = "{}新闻阅读器".format(Type)
        self.gateway = Type
        self.Xpath = Xpath()
        self.browser = webdriver.Chrome()
        self.wait = ui.WebDriverWait(self.browser,10)
        self.browser.get(Web[Type])

        self.WordsDealer = WordsDealer()
        self.ToolBox = NewTextRank()
        self.Dealer = Dealer()
        startJVM(getDefaultJVMPath(),r"-Djava.class.path=C:\Program Files\nlpapi\Hanlp\hanlp-1.7.4\hanlp-1.7.4.jar;C:\Program Files\nlpapi\Hanlp\hanlp-1.7.4","-Xms1g","-Xmx1g")
        self.StandardTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
        
        self.page = 1

        self.allowed_list = ["n","f","v"]
        self.special_list = ["ALC"]

        if end_page > 0:
            self.end = end_page
        else:
            self.wait.until(lambda browser:self.browser.find_element_by_xpath(self.Xpath.PageNumXpath[self.gateway]))
            button = self.browser.find_element_by_xpath(self.Xpath.PageNumXpath[self.gateway])
            self.end = int(button.text)-1

    def Turner(self):
        self.page += 1
        self.end -= 1
        
        self.wait.until(lambda browser:self.browser.find_element_by_xpath(self.Xpath.PageInXpath[self.gateway]))
        self.browser.find_element_by_xpath(self.Xpath.PageInXpath[self.gateway]).send_keys(self.page)

        self.wait.until(lambda browser:self.browser.find_element_by_xpath(self.Xpath.PageTurnerXpath[self.gateway]))
        button = self.browser.find_element_by_xpath(self.Xpath.PageTurnerXpath[self.gateway])
        self.browser.execute_script('arguments[0].click()',button)

        print("现在是第{}页啦！".format(self.page))



    def ListClicker(self,news_num):
        newslist = self.Xpath.ListClickerXpath[self.gateway].format(news_num)
        try:
            self.wait.until(lambda browser:self.browser.find_element_by_xpath(newslist))
            button = self.browser.find_element_by_xpath(newslist)
            self.browser.execute_script('arguments[0].click()',button)

            windows = self.browser.window_handles
            self.browser.switch_to.window(windows[-1])
            print("现在是本页第{}条哦。".format(news_num))
        except (WebDriverException,TimeoutException,NoSuchElementException):
            print("我找这一页找不第{}条诶。".format(news_num))

    def WindowsChanger(self):
        
        self.browser.close()
        windows = self.browser.window_handles
        self.browser.switch_to.window(windows[0])

    def TextLearner(self,text_xpath,TYPE, Tag = str, Target = str):
        
        self.wait.until(lambda browser:self.browser.find_element_by_xpath(text_xpath))
        button = self.browser.find_element_by_xpath(text_xpath)
        sentence = button.text

        sentence_tem = ""
        sentence = sentence.split("\n")
        for i in range(len(sentence)-4):
                    sentence_tem += sentence[i]
        sentence = sentence_tem

        sentence_list = self.StandardTokenizer.segment(sentence)
        words = self.WordsDealer.HanlpDealer(sentence_list)


        words = self.ToolBox.selecter(words,self.allowed_list,self.special_list)

        if TYPE == "Pair":
            NV,VN = self.ToolBox.NVNPair(words = words)

            for k,v in NV.graph.items():
                self.Dealer.VectorRenewer(v,k)
            for k,v in VN.graph.items():
                self.Dealer.VectorRenewer(v,k)

        elif TYPE == "Vector":

            OutCome = self.ToolBox.PairRank(d = 0.8,words = words,center = Target,itime = 100)

            self.Dealer.VectorRenewer(OutCome,Tag)

            
        
        
            

    def THSTextDealer(self,Learner = False,PairBuilder = False):
        
        text_xpath = self.Xpath.TextXpath[self.gateway]
        direction_xpath = self.Xpath.TagXpath[self.gateway]
        company_xpath = self.Xpath.THSXpath["company"]

        if Learner and not PairBuilder:
                
            try:
                self.wait.until(lambda browser:self.browser.find_element_by_xpath(direction_xpath))
                button = self.browser.find_element_by_xpath(direction_xpath)
                direction = button.text

                if "利好" in direction or "利空" in direction:
                    
                    if "利好"in direction:
                        direction = (direction,"a")
                    else:
                        direction = (direction,"a")

                    self.wait.until(lambda browser:self.browser.find_element_by_xpath(company_xpath))
                    button = self.browser.find_element_by_xpath(company_xpath)
                    company_name = button.text
                        
                    self.TextLearner(text_xpath = text_xpath,TYPE = "Vector",Tag = direction[0],Target = company_name)

                    print("学到了一个{}消息。".format(direction[0]))

                elif "中性" in direction:
                    print("这条没用。")
                    pass

            except (WebDriverException,TimeoutException, NoSuchElementException):
                print("不是同花顺标准格式，我看不懂诶")
                pass

        elif Learner and PairBuilder:
            try:
                self.TextLearner(text_xpath = text_xpath,TYPE = "Pair")
                print("学了一条新闻。")

            except (WebDriverException,TimeoutException, NoSuchElementException):
                print("诶?")
                pass

            
            

                        

                        

                        
                        

                        

                        
                        
                        
                
    
