'''
Created on 2016年3月20日

@author: lei
'''
from project.allLib import *
from project.defDataStruct import *
from project.parseLogToNodes import parseLogToNodes

logPath = r"/Users/lei/Desktop/15Project/report/drstrace.create.exe.08960.0000.log"

#测试用此例子，以后用预处理.log文件后的结果替换
NtCalls = ['NtOpenFile', 'NtClose','NtOpenFile', 'NtSetInformationFile.FileBasicInformation', 'NtClose',
           'NtOpenFile', 'NtQueryInformationFile.FileAttributeTagInformation', 'NtSetInformationFile.FileDispositionInformation', 'NtClose'
               ]

#先生成树
searchTree = Tree()
searchTree.buildTree(NtCallsTree)

def find(curNode, newCall):
        #当前节点不可能为正在查找的节点，因为是从根节点开始查询的
        curNode = curNode.treeNode
        if len(curNode.leftChild) == 0:
            return 0
        elif curNode.leftChild[0].callName == newCall.callName:
            return curNode.leftChild[0]
        elif len(curNode.leftChild[0].rightChild) == 0:
            return 0
        elif curNode.leftChild[0].rightChild != []:
            for i in range(len(curNode.leftChild[0].rightChild)):
                if curNode.leftChild[0].rightChild[i] == newCall:
                    return curNode.leftChild[0].rightChild[i]
        else:
            return 0
                
#解析log文件得到所有节点
allStraces = parseLogToNodes(logPath, parseDict)

#开始匹配
def treeMatching(allStraces, tree):
    #因为可能有多个API同时执行，所以要用数组保存每个API执行至的当前节点
    curMatchingIndex = 0    
    curMatchingNodes = []
    curTreeRoot = MatchingNode(tree.root, 0)
    for call in allStraces:        
        if len(curMatchingNodes) == 0:
            curMatchingNode = MatchingNode(tree.root, call.dependencyPara)
            curMatchingNodes.append(curMatchingNode)
        for i in range(len(curMatchingNodes)):
            if call.dependencyPara == curMatchingNode.dependencyPara:
                if find(curMatchingNode, call) != 0:
                    curMatchingNode.treeNode = find(curMatchingNode,call)
                    curMatchingNodes[i] = curMatchingNode
            else:
                if find(curTreeRoot, call) != 0:
                    curMatchingNode = MatchingNode(find(tree.root, call), call.dependencyPara)
                    curMatchingNodes.append(curMatchingNode)
            if call.successStatus == 'failed' or curMatchingNode.treeNode.leftChild[0].callName[:4] == 'leaf' and len(curMatchingNode.treeNode.leftChild[0].rightChild) == 0:
                print(curMatchingNode.treeNode.leftChild[0].callName)
                curMatchingNodes.pop(i)

treeMatching(allStraces, searchTree)