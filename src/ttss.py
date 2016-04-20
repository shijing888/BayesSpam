#encoding=utf-8
'''
Created on 2016年4月18日

@author: lenovo
'''

from spam.spamEmail import spamEmailBayes
import re
#spam类对象
spam=spamEmailBayes()
#保存词频的词典
spamDict={}
normDict={}
testDict={}
#保存每封邮件中出现的词
wordsList=[]
wordsDict={}
#保存预测结果,key为文件名，值为预测类别
testResult={}
#分别获得正常邮件、垃圾邮件及测试文件名称列表
normFileList=spam.get_File_List(r"E:\EclipseWorkspace\BayesSpam\data\normal")
spamFileList=spam.get_File_List(r"E:\EclipseWorkspace\BayesSpam\data\spam")
testFileList=spam.get_File_List(r"E:\EclipseWorkspace\BayesSpam\data\test")
#获取训练集中正常邮件与垃圾邮件的数量
normFilelen=len(normFileList)
spamFilelen=len(spamFileList)
#获得停用词表，用于对停用词过滤
stopList=spam.getStopWords()
#获得正常邮件中的词频
for fileName in normFileList:
    wordsList.clear()
    for line in open("../data/normal/"+fileName):
        #过滤掉非中文字符
        rule=re.compile(r"[^\u4e00-\u9fa5]")
        line=rule.sub("",line)
        #将每封邮件出现的词保存在wordsList中
        spam.get_word_list(line,wordsList,stopList)
    #统计每个词在所有邮件中出现的次数
    spam.addToDict(wordsList, wordsDict)
normDict=wordsDict.copy()  

#获得垃圾邮件中的词频
wordsDict.clear()
for fileName in spamFileList:
    wordsList.clear()
    for line in open("../data/spam/"+fileName):
        rule=re.compile(r"[^\u4e00-\u9fa5]")
        line=rule.sub("",line)
        spam.get_word_list(line,wordsList,stopList)
    spam.addToDict(wordsList, wordsDict)
spamDict=wordsDict.copy()

# 测试邮件
for fileName in testFileList:
    testDict.clear( )
    wordsDict.clear()
    wordsList.clear()
    for line in open("../data/test/"+fileName):
        rule=re.compile(r"[^\u4e00-\u9fa5]")
        line=rule.sub("",line)
        spam.get_word_list(line,wordsList,stopList)
    spam.addToDict(wordsList, wordsDict)
    testDict=wordsDict.copy()
    #通过计算每个文件中p(s|w)来得到对分类影响最大的15个词
    wordProbList=spam.getTestWords(testDict, spamDict,normDict,normFilelen,spamFilelen)
    #对每封邮件得到的15个词计算贝叶斯概率  
    p=spam.calBayes(wordProbList, spamDict, normDict)
    if(p>0.9):
        testResult.setdefault(fileName,1)
    else:
        testResult.setdefault(fileName,0)
#计算分类准确率（测试集中文件名低于1000的为正常邮件）
testAccuracy=spam.calAccuracy(testResult)
for i,ic in testResult.items():
    print(i+"/"+str(ic))
print(testAccuracy)  