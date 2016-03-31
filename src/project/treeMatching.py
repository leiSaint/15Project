'''
Created on 2016年3月20日

@author: lei
'''
from project.forestToTree import *
from project.allLib import *

#测试用此例子，以后用预处理.log文件后的结果替换
NtCalls = ['NtOpenFile', 'NtClose','NtOpenFile', 'NtSetInformationFile.FileBasicInformation', 'NtClose',
           'NtOpenFile', 'NtQueryInformationFile.FileAttributeTagInformation', 'NtSetInformationFile.FileDispositionInformation', 'NtClose'
               ]

#先生成树
behaviorTree = forestToTree(NtCallsTree)
node = behaviorTree[0]

#比较新读入节点和所有根节点，以及所有currentNodes的第一层左子树和左子树的所有第一层右子树，返回应创建新的API头还是继续遍历当前分支
#def matchingAllChild(newNode, currentNodes):
    
def treeMatching(allStraces, tree):
    #因为可能有多个API同时执行，所以要用数组保存每个API执行至的当前节点
    curMatchingIndex = 0    
    curMatchingNodes = []
    curMatchingNode = tree[0]
    curMatchingNodes.append(curMatchingNode)
    for call in allStraces:     
        if call == curMatchingNode.callName:
            print(curMatchingNode.callName)
            curMatchingNode = curMatchingNode.leftChild
            if curMatchingNode.callName[:3] == 'Leaf' and curMatchingNode.leftChild == None and curMatchingNode.rightChild == None:
                print(curMatchingNode.callName)
        #else:

treeMatching(NtCalls, behaviorTree)