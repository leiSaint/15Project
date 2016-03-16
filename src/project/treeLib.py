'''
Created on 2016年3月6日

@author: lei
'''
#-*- coding: utf-8 -*-

from project.defDataStruct import *

#建立基础调用的库
NtCallDict = {
              'NtOpenFile':treeNode("NtOpenFile"),
              'NtClose':treeNode("NtClose"), 
              'NtSetInformationFile.FileBasicInformation':treeNode('NtSetInformationFile.FileBasicInformation'), 
              'NtQueryInformationFile.FileAttributeTagInformation':treeNode('NtQueryInformationFile.FileAttributeTagInformation'), 
              'NtSetInformationFile.FileDispositionInformation':treeNode('NtSetInformationFile.FileDispositionInformation'), 
              'LeafChangeFileAttr':treeNode('Change file attribute'), 
              'LeafDeleteFile':treeNode('Delete file'), 
              'LeafOpenFile':treeNode('Open file')
}

#建立系统调用链库，从链的第一个调用开始，到该链代表的API名字节点结束
NtCallsTree = [['NtOpenFile', 'NtClose', 'LeafOpenFile'],
               ['NtOpenFile', 'NtSetInformationFile.FileBasicInformation', 'NtClose', 'LeafChangeFileAttr'],
               ['NtOpenFile', 'NtQueryInformationFile.FileAttributeTagInformation', 'NtSetInformationFile.FileDispositionInformation', 'NtClose', 'LeafDeleteFile']
               ]