'''
Created on 2016年3月6日

@author: lei
'''
#-*- coding: utf-8 -*-
from project.allLib import NtCallsTree


class TreeNode(object):
    '节点类，初始化时要包含系统调用名和指向左右子树的指针。类的属性包含数据依赖的值和调用是否成功标志'
    def __init__(self, callName):
        self.callName = callName
        self.leftChild = []
        self.rightChild = []
            
class Tree(object):
    def __init__(self):
        self.root = TreeNode('rootNode')
    
    def add(self, callList):
        node = self.root
        for call in callList:
            (branch, isExist) = self.find(node, call)
            if isExist < 0:
                if branch == 'leftChild':
                    #奇怪的是，此处如果调用NtCallDict则会错误，导致新建节点非只包含空孩子，而是包含了当前同名节点的结构
                    newNode = TreeNode(call)
                    node.leftChild.append(newNode)
                    node = node.leftChild[0]
                if branch == 'rightChild':
                    newNode = TreeNode(call)
                    node.leftChild[0].rightChild.append(newNode)
                    node = node.leftChild[0].rightChild[-1]
            else:
                if branch == 'leftChild':
                    node = node.leftChild[0]
                if branch == 'rightChild':
                    node = node.leftChild[0].rightChild[isExist]
                
    
    def find(self, curNode, newCall):
        #当前节点不可能为正在查找的节点，因为是从根节点开始查询的
        if len(curNode.leftChild) == 0:
            return 'leftChild', -1
        elif curNode.leftChild[0].callName == newCall:
            return 'leftChild', 1
        elif len(curNode.leftChild[0].rightChild) == 0:
            return 'rightChild', -1
        elif curNode.leftChild[0].rightChild != []:
            for i in range(len(curNode.leftChild[0].rightChild)):
                if curNode.leftChild[0].rightChild[i].callName == newCall:
                    return 'rightChild', i
            return 'rightChild', -1
        
    def buildTree(self, trees):
        for tree in trees:
            self.add(tree)

class logNode(object):
    '解析log文件获取到的节点类，包含了函数名和获得到的各项参数'
    def __init__(self, callName):
        self.callName = callName  
        self.dependencyPara = ''
        self.concernedPara = []
        self.successStatus = ''
    
class MatchingNode(object):
    '匹配查找时使用的节点，包含了树节点，数据依赖的值，以及要写入最终结果的参数（第一项为行为类别(0:文件类，1:注册表类,2:进程或线程...)，第二项为行为描述，第三项为要输出的具体参数'
    def __init__(self, treeNode, dependencyPara):
        self.treeNode = treeNode
        self.dependencyPara = dependencyPara
        self.concernedPara = ['', '', '']
    