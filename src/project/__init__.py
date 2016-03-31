#-*- coding: utf-8 -*-

from project.defDataStruct import *
from project.allLib import *

searchTree = Tree()
searchTree.buildTree(NtCallsTree)
print(searchTree.root.leftChild[0].callName)