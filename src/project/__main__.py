'''
Created on 2016年5月11日

@author: lei
使用命令 
    python3 project "样本路径"
来调用，样本路径前后要加上引号，防止路径中包含空格
'''



import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project.defDataStruct import *
from project.parseLogToNodes import *
from project.allLib import *
from project.treeMatching import *

#logPath = r'/Users/lei/Desktop/new report/drstrace.changeAttr.exe.04952.0000.log'
#logPath = r'/Users/lei/Desktop/new report/drstrace.console_devil_server.exe.02840.0000.log'
logPath = r'/Users/lei/Desktop/drstrace.console_devil_server.exe.02840.0000.log'
#logPath = r'/Users/lei/Desktop/new report/drstrace.queryValue.exe.03744.0000.log'
#logPath = sys.argv[1]

#先生成树
searchTree = Tree()
searchTree.buildTree(NtCallsTree)

#解析log文件得到所有节点
allStraces = parseLogToNodes(logPath, parseDict)
for node in allStraces:
    print(node.dependencyPara, node.successStatus,node.concernedPara[0])

#开始匹配
results = treeMatching(allStraces, searchTree)
print(len(results))
for result in results:
    print(result.concernedPara[0],result.concernedPara[1], result.concernedPara[2])