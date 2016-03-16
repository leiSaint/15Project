#-*- coding: utf-8 -*-

from project.forestToTree import *
from project.treeLib import *

testList = forestToTree(NtCallsTree)
print(len(testList))
for nodes in testList:
    print(nodes.callName)