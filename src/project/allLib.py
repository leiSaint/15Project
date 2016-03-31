'''
Created on 2016年3月6日

@author: lei
'''
#-*- coding: utf-8 -*-

from project.defDataStruct import *

#建立基础调用的库
NtCallDict = {
              'NtOpenFile':TreeNode('NtOpenFile'),
              'NtClose':TreeNode('NtClose'), 
              'NtSetInformationFile.FileBasicInformation':TreeNode('NtSetInformationFile.FileBasicInformation'), 
              'NtQueryInformationFile.FileAttributeTagInformation':TreeNode('NtQueryInformationFile.FileAttributeTagInformation'), 
              'NtSetInformationFile.FileDispositionInformation':TreeNode('NtSetInformationFile.FileDispositionInformation'), 
              'LeafChangeFileAttr':TreeNode('Change file attribute'), 
              'LeafDeleteFile':TreeNode('Delete file'), 
              'LeafOpenFile':TreeNode('Open file')
}

#建立系统调用链库，从链的第一个调用开始，到该链代表的API名字节点结束
NtCallsTree = [['NtOpenFile', 'NtClose', 'LeafOpenFile'],
               ['NtOpenFile', 'NtSetInformationFile.FileBasicInformation', 'NtClose', 'LeafChangeFileAttr']
               ]

#定义各个系统调用node的创建方式，包括关注的参数及该参数对应的正则表达式和要去掉的字符
parseDict = {'NtCreateFile': [{12:'=> .*? ', 'strip': '=> '},{11:'succeed|failed'},{2:'\?\?.*?\"','strip':'\?\?\"'}]}