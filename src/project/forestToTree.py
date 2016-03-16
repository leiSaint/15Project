'''
Created on 2016年3月15日

@author: lei
'''
#-*- coding: utf-8 -*-

from project.treeLib import *

#利用系统调用链库的信息建立包含所有系统调用的树,储存在一个数组中
def forestToTree(trees):
    nodeIndex = 0
    nodeList = []
    nodeList.append(NtCallDict['NtOpenFile'])
    currentNode = nodeList[0]
    for tree in trees:
        for node in tree:
            #边遍历边插入节点
            if currentNode == None:
                nodeList.append(NtCallDict[node])
                nodeIndex += 1
                currentNode = nodeList[nodeIndex]
            if node == currentNode.callName:
                currentNode = currentNode.leftChild
            elif node != currentNode.callName:
                while currentNode.rightChild != None:
                    if node != currentNode.callName:
                        currentNode = currentNode.rightChild
                    if node == currentNode.callName:
                        currentNode == currentNode.leftChild
            else :
                raise ValueError
        currentNode = nodeList[0]
    return nodeList
    