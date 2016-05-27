'''
Created on 2016年3月27日

@author: lei
'''
# -*-encoding: UTF-8 -*-
from project.defDataStruct import logNode
from project.allLib import *
import re

def parseLogToNodes(logPath, parseDict):
    NtCallNodes = []
    with open(logPath, 'r') as logFile:
        lineCount = 0
        lines = logFile.readlines()
        for line in lines:
            lineCount += 1
            
            if line[:1] != '\t' and line[:1] != ' ':
                key = line.strip()
                
                if key in parseDict.keys():
                    #创建对应的logNode节点
                    node = logNode(key)
                                                                  
                    parseValue = parseDict[key]
                    #print(parseValue)
                    
                    #开始解析parseDict中定义的关注参数，并将结果存放至NtCallNodes列表中
                    #paraCount指示当前处理的是调用名键对应的列表类型键值的第几项，dicPara指向其中的一个字典成员
                    paraCount = 0
                    errorFlag = 0
                    for dicPara in parseValue:
                        
                        for key in dicPara:
                            if isinstance(key, int):
                                try:
                                    reSource = lines[lineCount + key]
                                except:
                                    print("element out of range in lines[]")
                                    errorFlag = 1
                                    break
                                pattern = re.compile(dicPara[key])
                                
                                #获取到还未去除无关字符的参数字符串
                                try:
                                    tempPara = re.search(pattern, reSource).group(0)
                                except:
                                    if node.callName != 'NtCreateFile':
                                        print("parse error")
                                    errorFlag = 1
                                    break
                                
                                #如果有strip项，则切除无关字符
                                if 'strip' in dicPara:
                                    realPara = tempPara.strip(dicPara['strip'])
                                else:
                                    realPara = tempPara
                        if errorFlag is not 1:
                            if paraCount == 0:
                                node.dependencyPara = realPara
                            if paraCount == 1:
                                node.successStatus = realPara
                            if paraCount >= 2:
                                node.concernedPara.append(realPara)
                        if errorFlag == 1 and (node.callName == 'NtTerminateProcess' or node.callName == 'NtTerminateThread'):
                            node.successStatus == 'succeeded'
                            node.concernedPara = '0x0'                                                        
                        paraCount += 1
                        errorFlag = 0
                    #将填充完的node添加至列表
                    NtCallNodes.append(node)
                else:
                    continue
    return NtCallNodes