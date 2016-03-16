'''
Created on 2016年3月6日

@author: lei
'''
#-*- coding: utf-8 -*-

class treeNode(object):
    '节点类，初始化时要包含系统调用名和指向左右子树的指针。类的属性包含数据依赖的值和调用是否成功标志'
    dependencyValue = ''
    isSuccess = 0
    def __init__(self, callName, leftChild = None, rightChild = None):
        self.callName = callName
        self.leftChild = leftChild
        self.rightChild = rightChild