'''
Created on 2016年3月6日

@author: lei
'''
#-*- coding: utf-8 -*-

from project.defDataStruct import *

NtOpenRes = ['NtOpenThreadToken', 'NtOpenProcess', 'NtOpenProcessToken', 'NtCreateSection', 
             'NtOpenKey', 'NtOpenFile', 'NtCreateFile', 'NtOpenKeyEx', 'NtCreateThreadEx', 
             'NtCreateKey', 'NtCreateUserProcess']

#建立系统调用链库，从链的第一个调用开始，到该链代表的API名字节点结束
NtCallsTree = [
               ['NtOpenFile', 'leafOpenFile'],
               ['NtOpenFile', 'NtClose', 'LeafOpenFile'],
               ['NtOpenFile', 'NtSetInformationFile.FileBasicInformation', 'NtClose', 'LeafSetFileAttributes'],
               ['NtOpenFile', 'NtQueryInformationFile.FileDispositionInformation', 'NtClose', 'leafDeleteFileOrDir'],
               ['NtOpenFile', 'NtQueryDirectoryFile.FileBothDirectoryInformation', 'NtClose', 'leafFindFirstFile'],
               ['NtOpenFile', 'NtQueryDirectoryFile.FileBothDirectoryInformation', 'NtQueryDirectoryFile.FileBothDirectoryInformation', 'NtClose', 'leafFindNextFile'],
               ['NtCreateFile', 'NtWriteFile', 'NtClose', 'leafWriteFile'],
               ['NtCreateFile', 'NtClose', 'leafCreateFile'],
               ['NtOpenProcessToken', 'leafOpenProcessToken'],
               ['NtOpenThreadToken', 'leafOpenThreadToken'],
               ['NtOpenProcessTokenEx', 'leafOpenProcessToken'],
               ['NtOpenThreadTokenEx', 'leafOpenThreadToken'],
               ['NtOpenKeyEx', 'NtQueryValueKey', 'NtClose', 'leafQueryValueKey'],
               ['NtOpenKeyEx', 'leafOpenKey'],
               ['NtOpenKey', 'leafOpenKey'],
               ['NtCreateKey', 'leafCreateKey'],
               ['NtCreateKey', 'NtSetValueKey', 'NtClose', 'leafRegSetKeyValue'],
               ['NtOpenKeyEx', 'NtClose','leafRegOpenKey'],
               ['NtOpenKey', 'NtDeleteKey', 'NtClose', 'leafRegDeleteKey'],
               ['NtOpenKeyEx', 'NtDeleteValueKey', 'NtClose', 'leafDeleateKeyValue'],
               ['NtEnumerateKey.KeyBasicInformation', 'leafEnumKey'],
               ['NtCreateFile', 'leafCreateFile'],
               ['NtCreateUserProcess', 'leafCreateProcess'],
               ['NtTerminateProcess', 'leafExitProcess'],
               ['NtOpenProcess', 'NtCreateThreadEx', 'leafCreateRemoteThread'],
               ['NtOpenProcess', 'leafOpenProcess'],
               ['NtCreateThreadEx', 'leafCreateThread'],
               ['NtCreateSection', 'NtMapViewOfSection', 'NtUnmapViewOfSection', 'leafCreateToolhelp32SnapShot'],
               ['NtCreateSection', 'NtMapViewOfSection', 'NtUnmapViewOfSection', 'NtClose', 'leafCreateToolhelp32SnapShot&CloseHandle'],
               ['NtCreateSection', 'NtMapViewOfSection', 'NtUnmapViewOfSection', 'NtMapViewOfSection', 'NtUnmapViewOfSection', 'NtClose', 'leafCreateToolhelp32SnapShot&Process32First&Process32Next'],
               ]
callSet = ['NtSetValueKey', 'NtSetInformationFile.FileBasicInformation', 'NtCreateKey', 'NtOpenProcessToken', 'LeafOpenFile', 'NtOpenThreadToken', 'NtCreateUserProcess', 
           'NtQueryInformationFile.FileDispositionInformation', 'NtWriteFile', 'NtMapViewOfSection', 'NtCreateThreadEx', 'NtDeleteKey', 
           'NtQueryValueKey', 'NtCreateSection', 'NtOpenProcess',
             ]

#定义各个系统调用node的创建方式，使用字典来存储，包括关注的参数及该参数对应的正则表达式和要去掉的字符,数字表示从系统调用名数起的行数
parseDict = {'NtCreateFile': [{12:'=> .*? ', 'strip': '=> '},{11:'succeeded|failed'},{2:'\?\?.*?\"','strip':'\?\?\"'}, {8:'FILE_DIRECTORY_FILE'}, {8:'FILE_NON_DIRECTORY_FILE'}],
             'NtClose': [{0:'0x.*? ', 'strip': ' '}, {1:'succeeded|failed'}, {2:' ', 'strip': ' '}],
             'NtOpenFile': [{7: '=> .*? ', 'strip': '=> '}, {6:'succeeded|failed'}, {2:'\?\?.*?\"','strip':'\?\?\"'}], 
             'NtSetValueKey': [{0:'0x.*? '},{6:'succeeded|failed'},{1:'\".*?\"', 'strip':'\"'}],
             'NtSetInformationFile.FileBasicInformation':[{0:'0x.*? ', 'strip':' '},{5:'succeeded|failed'},{2:'0x.*? ', 'strip':' '}],
             'NtCreateKey': [{8:'=> .*? ', 'strip': '=> '},{7:'succeeded|failed'},{2:'".*?"'}],
             'NtOpenProcessToken': [{4:'=> .*? ', 'strip': '=> '},{3:'succeeded|failed'},{0:'0x.*? '}],
             'NtOpenProcessTokenEx': [{5:'=> .*? ', 'strip': '=> '},{4:'succeeded|failed'},{0:'0x.*? '}],
             'NtOpenThreadToken': [{5:'=> .*? ', 'strip': '=> '},{3:'succeeded|failed'},{0:'0x.*? '}],
             'NtCreateUserProcess': [{12:'=> .*? ', 'strip': '=> '},{11:'succeeded|failed'},{1:'0x.*? '}],
             'NtSetInformationFile.FileDispositionInformation': [{0:'0x.*? ', 'strip': ' '}, {5:'succeeded|failed'}, {3:'0x.*? ', 'strip': ' '}],
             'NtWriteFile': [{0:'0x.*? '},{9:'succeeded|failed'},{5:'0x.*? '}],
             'NtCreateThreadEx': [{12:'=> .*? ', 'strip': '=> '},{11:'succeeded|failed'},{3:'0x.*? '}],
             'NtDeleteKey': [{0:'0x.*? '}, {1:'succeeded|failed'}, {2:'\?\?.*?\"','strip':'\?\?\"'}],
             'NtQueryValueKey': [{0:'0x.*? '}, {6:'succeeded|failed'}, {3:'0x.*? ', 'strip': ' '}, {1:'\".*?\"', 'strip': '\"'}],
             'NtOpenKeyEx': [{5: '=> .*? ', 'strip': '=> '}, {4:'succeeded|failed'}, {2:'\".*?\"', 'strip':'\"'}],
             'NtOpenKey': [{4: '=> .*? ', 'strip': '=> '}, {3:'succeeded|failed'}, {2:'\".*?\"', 'strip':'\"'}],
             'NtDeleteValueKey': [{0:'0x.*? ', 'strip': ' '}, {2:'succeeded|failed'}, {2:'\".*?\"', 'strip':'\"'}],
             'NtQueryDirectoryFile.FileBothDirectoryInformation':[{0:'0x.*? ', 'strip': ' '}, {11:'succeeded|failed'}, {9:'\".*?\"', 'strip':'\"'}],
             'NtUnmapViewOfSection':[{0:'0x.*? ', 'strip': ' '}, {2:'succeeded|failed'}, {3:'0x.*? ', 'strip': ' '}],
             'NtEnumerateKey.KeyBasicInformation': [{0:'0x.*? ', 'strip': ' '}, {6:'succeeded|failed'}, {8:'=> .*? ', 'strip': '=> '}],
             'NtTerminateProcess': [{0:'0x.*? ', 'strip': ' '}, {2:'succeeded|failed'}, {3:'0x.*? ', 'strip': ' '}],
             'NtOpenProcess':[{5:'=> .*? ', 'strip': '=> '},{4:'succeeded|failed'}, {2:'name=.*?,', 'strip':'name=,'}],
             'NtCreateSection':[{8:'=> .*? ', 'strip': '=> '}, {7:'succeeded|failed'}, {2:'\".*?\"|<null>', 'strip':'\"'}],
             'NtMapViewOfSection':[{0:'0x.*? ', 'strip': ' '}, {10:'succeeded|failed'}, {1:'0x.*? ', 'strip': ' '}]
             }    

leafSet = ['leafCreateToolhelp32SnapShot&CloseHandle', 'leafFindNextFile', ]