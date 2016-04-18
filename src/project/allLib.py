'''
Created on 2016年3月6日

@author: lei
'''
#-*- coding: utf-8 -*-

from project.defDataStruct import *

#建立基础调用的库
NtCallDict = [
              'NtOpenFile',
              'NtClose', 
              'NtSetInformationFile.FileBasicInformation', 
              'NtQueryInformationFile.FileAttributeTagInformation', 
              'NtSetInformationFile.FileDispositionInformation', 
              'LeafChangeFileAttr', 
              'LeafDeleteFile', 
              'LeafOpenFile'
              ]

#建立系统调用链库，从链的第一个调用开始，到该链代表的API名字节点结束
NtCallsTree = [
               ['NtOpenFile', 'leafOpenFile'],
               ['NtOpenFile', 'NtClose', 'LeafOpenFile'],
               ['NtOpenFile', 'NtSetInformationFile.FileBasicInformation', 'NtClose', 'LeafSetFileAttributes'],
               ['NtOpenFile', 'NtQueryInformationFile.FileDispositionInformation', 'NtClose', 'leafDeleteFileOrDir'],
               ['NtOpenFile', 'NtQueryDirectoryFile.FileBothDirectoryInformation', 'NtClose', 'leafFindFirstFile'],
               ['NtOpenFile', 'NtQueryDirectoryFile.FileBothDirectoryInformation', 'NtQueryDirectoryFile.FileBothDirectoryInformation', 'NtClose', 'leafFindNextFile'],
               ['NtCreateFile', 'NtWriteFile', 'NtClose', 'leafWriteFile'],
               ['NtOpenProcessToken', 'leafOpenProcessToken'],
               ['NtOpenThreadToken', 'leafOpenThreadToken'],
               ['NtOpenKeyEx', 'NtQueryValueKey', 'NtClose'],
               ['NtCreateKey', 'leafCreateKey'],
               ['NtCreateKey', 'NtSetValueKey', 'NtClose', 'leafRegSetKeyValue'],
               ['NtOpenKeyEx', 'NtClose','leafRegOpenKey'],
               ['NtOpenKey', 'NtDeleteKey', 'NtClose', 'leafRegDeleteKey'],
               ['NtOpenKeyEx', 'NtDeleteValueKey', 'NtClose', 'leafDeleateKeyValue'],
               ['NtEnumerateKey.KeyBasicInformation', 'leafEnumKey']
               ['NtCreateFile', 'leafCreateFile'],
               ['NtCreateUserProcess', 'leafCreateProcess'],
               ['NtTerminateProcess', 'leafExitProcess'],
               ['NtOpenProcess', 'NtCreateThreadEx', 'leafCreateRemoteThread'],
               ['NtOpenProcess', 'leafOpenProcess'],
               ['NtCreateThreadEx', 'leafCreateThread']
               ['NtCreateSection', 'NtMapViewOfSection', 'NtUnmapViewOfSection', 'leafCreateToolhelp32SnapShot'],
               ['NtCreateSection', 'NtMapViewOfSection', 'NtUnmapViewOfSection', 'NtClose', 'leafCreateToolhelp32SnapShot&CloseHandle'],
               ['NtCreateSection', 'NtMapViewOfSection', 'NtUnmapViewOfSection', 'NtMapViewOfSection', 'NtUnmapViewOfSection', 'NtClose', 'leafCreateToolhelp32SnapShot&Process32First&Process32Next'],
               ]

#定义各个系统调用node的创建方式，使用字典来存储，包括关注的参数及该参数对应的正则表达式和要去掉的字符,数字表示从系统调用名数起的行数
parseDict = {'NtCreateFile': [{12:'=> .*? ', 'strip': '=> '},{11:'succeed|failed'},{2:'\?\?.*?\"','strip':'\?\?\"'}],
             'NtClose': [{1:'0x.* '}, {2:'succeed|failed'}, {3:' ', 'strip': ' '}],
             'NtOpenFile': [{8: '=> .*? ', 'strip': '=> '}, {7:'succeed|failed'}, {2:'\?\?.*?\"','strip':'\?\?\"'}]}             