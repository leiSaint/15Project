'''
Created on 2016年3月27日

@author: lei
'''
# -*-encoding: UTF-8 -*-
from project.defDataStruct import logNode
from project.allLib import *
import re
logPath = r"/Users/lei/Desktop/15Project/report/drstrace.create.exe.08960.0000.log"
def parseLogToNodes(logPath, parseDict):
    NtCallNodes = []
    with open(logPath, 'r') as logFile:
        lineCount = 0
        lines = logFile.readlines()
        for line in lines:
            lineCount += 1
            
            if line[:1] != '\t' and line[:1] != ' ':
                key = line.strip()
                
                #创建对应的logNode节点
                node = logNode(key)
                                                
                parseValue = parseDict[key]
                #print(parseValue)
                
                #开始解析parseDict中定义的关注参数，并将结果存放至NtCallNodes列表中
                #paraCount指示当前处理的是调用名键对应的列表类型键值的第几项，dicPara指向其中的一个字典成员
                paraCount = 0
                for dicPara in parseValue:
                    
                    for key in dicPara:
                        if isinstance(key, int):
                            reSource = lines[lineCount + key]
                            pattern = re.compile(dicPara[key])
                            
                            #获取到还未去除无关字符的参数字符串
                            tempPara = re.search(pattern, reSource).group(0)
                            
                            #如果有strip项，则切除无关字符
                            if 'strip' in dicPara:
                                realPara = tempPara.strip(dicPara['strip'])
                            else:
                                realPara = tempPara
                    if paraCount == 0:
                        node.dependencyPara = realPara
                    if paraCount == 1:
                        node.successStatus = realPara
                    if paraCount == 2:
                        node.concernedPara = realPara                                                        
                    paraCount += 1
                #将填充完的node添加至列表
                NtCallNodes.append(node)
    return NtCallNodes

'''nodes = parseLogToNodes(logPath, parseDict)
print(len(nodes))
for node in nodes:
    print(node.concernedPara, node.dependencyPara, node.successStatus)'''             