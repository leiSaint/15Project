'''
Created on 2016年3月20日

@author: lei
'''
from project.allLib import *
from project.defDataStruct import *
from project.parseLogToNodes import parseLogToNodes
#from project.__main__ import sampleAddress
sampleAddress = r'c:\TrojanHorse\console_devil_server.exe'

def getFlashDiskPath():
    

def behaviorClassify(resultNode):
    '''输入查找树完成后的节点，将其根据ClassifyDict定义的类别信息进行分类，返回分类后的信息，包括类别，API名称，API参数'''
    classifyResult = ['', '', '']
    if resultNode.concernedPara[1] in classifyDict:
        classParaList = classifyDict[resultNode.concernedPara[1]]
        for classPara in classParaList:
            if resultNode.concernedPara[2] == sampleAddress and 'sample address' in list(classPara.values())[0]:
                classifyResult[0] = list(classPara.keys())[0]
                classifyResult[1] = resultNode.concernedPara[1]
                classifyResult[2] = resultNode.concernedPara[2]
            if resultNode.concernedPara[2] in list(classPara.values())[0]:
                classifyResult[0] = list(classPara.keys())[0]
                classifyResult[1] = resultNode.concernedPara[1]
                classifyResult[2] = resultNode.concernedPara[2]            
    return classifyResult

def processAfterMatched(call, curMatchingNode):
    '''先分类，再根据参数等单独处理。最后如果有需要，则写入concernedPara[2]，其中存储了路径等信息'''
    if call.callName == 'NtCreateFile':
        curMatchingNode.concernedPara[0] = '0'
        if call.concernedPara[1] == 'FILE_NON_DIRECTORY_FILE':
            curMatchingNode.concernedPara[1] = 'open or create file'
        else:
            curMatchingNode.concernedPara[1] = 'open or create directory'
            
        curMatchingNode.concernedPara[2] = call.concernedPara[0]
    
    if call.callName == 'NtOpenFile':
        curMatchingNode.concernedPara[0] = '0'
        curMatchingNode.concernedPara[1] = 'open file'
        curMatchingNode.concernedPara[2] = call.concernedPara[0]
    
    if call.callName == 'NtSetInformationFile.FileBasicInformation':
        curMatchingNode.concernedPara[1] = 'change file attribute'
    
    if call.callName == 'NtClose':
        curMatchingNode.dependencyPara = 0xffff
    
    if call.callName == 'NtSetValueKey':
        curMatchingNode.concernedPara[0] = '1'
        if call.concernedPara[0] == r'"Software\Microsoft\Windows\Currentversion\run"':
            curMatchingNode.concernedPara[1] = 'create a autostart item'
        curMatchingNode.concernedPara[2].append('\\' + call.concernedPara[0])
    
    if call.callName == 'NtCreateKey':
        curMatchingNode.concernedPara[0] = '1'
        curMatchingNode.concernedPara[1] = 'open or create a key'
        curMatchingNode.concernedPara[2] = call.concernedPara[0]
    
    if call.callName == 'NtOpenProcessToken':
        curMatchingNode.concernedPara[0] = '2'
        if curMatchingNode.concernedPara[2] == '0xffffffff':
            curMatchingNode.concernedPara[1] = 'open current process token'
        else:
            curMatchingNode.concernedPara[1] = 'open process token'
    
    if call.callName == 'NtOpenThreadToken':
        curMatchingNode.concernedPara[0] = '2'
        if curMatchingNode.concernedPara[2] == '0xffffffff':
            curMatchingNode.concernedPara[1] = 'open current thread token'
        else:
            curMatchingNode.concernedPara[1] = 'open thread token'
    
    if call.callName == 'NtCreateUserProcess':
        curMatchingNode.concernedPara[0] = '2'
        curMatchingNode.concernedPara[1] = 'create process'
    
    if call.callName == 'NtSetInformationFile.FileDispositionInformation':
        curMatchingNode.concernedPara[0] = '0'        
        if call.concernedPara[0] == '0xd':
            curMatchingNode.concernedPara[1] = 'delete file'
        
    if call.callName == 'NtWriteFile':
        curMatchingNode.concernedPara[0] = '0'
        curMatchingNode.concernedPara[1] = 'write file'
    
    if call.callName == 'NtCreateThreadEx':
        curMatchingNode.concernedPara[0] = '0'
        if curMatchingNode.concernedPara[1] == 'open process':
            curMatchingNode.concernedPara[1] = 'create remote thread'
            curMatchingNode.dependencyPara = call.dependencyPara
        else:
            curMatchingNode.concernedPara[1] = 'create thread'
            curMatchingNode.dependencyPara = call.dependencyPara   
    
    if call.callName == 'NtDeleteKey':
        curMatchingNode.concernedPara[0] = '1'
        curMatchingNode.concernedPara[1] = 'delete register key'
        
    if call.callName == 'NtQueryValueKey':
        curMatchingNode.concernedPara[0] = '1'
        curMatchingNode.concernedPara[1] = 'query value of key'
        curMatchingNode.concernedPara[2] = curMatchingNode.concernedPara[2] + '\\' + call.concernedPara[1]
    
    if call.callName == 'NtOpenKeyEx':
        curMatchingNode.concernedPara[0] = '1'
        curMatchingNode.concernedPara[1] = 'open register key'
        curMatchingNode.concernedPara[2] = call.concernedPara[0]
        
    if call.callName == 'NtOpenKey':
        curMatchingNode.concernedPara[0] = '1'
        curMatchingNode.concernedPara[1] = 'open register key'
        curMatchingNode.concernedPara[2] = call.concernedPara[0]
        
    if call.callName == 'NtDeleteValueKey':
        curMatchingNode.concernedPara[0] = '1'
        if curMatchingNode.concernedPara[1] == 'open register key':
            curMatchingNode.concernedPara[2].append('\\'+call.concernedPara[1])
        curMatchingNode.concernedPara[1] = 'delete key value'
    
    if call.callName == 'NtQueryDirectoryFile.FileBothDirectoryInformation':
        curMatchingNode.concernedPara[0] = '0'
        if curMatchingNode.concernedPara[1] == 'open file':
            curMatchingNode.concernedPara[2].append('\\'+call.concernedPara[0])
        curMatchingNode.concernedPara[1] = 'query file in specified directory'
    
    '''可以暂不关注unmap
    if call.callName == 'NtUnmapViewOfSection':
        curMatchingNode.concernedPara[0] = '3'
    '''
        
    if call.callName == 'NtMapViewOfSection':
        curMatchingNode.concernedPara[0] = '3'
        curMatchingNode.concernedPara[1] = 'map file into memory'
                
    if call.callName == 'NtEnumerateKey.KeyBasicInformation':
        curMatchingNode.concernedPara[0] = '1'
        curMatchingNode.concernedPara[1] = 'enumerate register key'
        
    if call.callName == 'NtTerminateProcess':
        curMatchingNode.concernedPara[0] = '2'
        curMatchingNode.concernedPara[1] = 'terminate specified process'
    
    if call.callName == 'NtOpenProcess':
        curMatchingNode.concernedPara[0] = '2'
        curMatchingNode.concernedPara[1] = 'open process'
        
    if call.callName == 'NtCreateSection':
        curMatchingNode.concernedPara[0] = '3'
        curMatchingNode.concernedPara[1] = 'create map file object'
    
    if call.callName == 'NtMapViewOfSection':
        curMatchingNode.concernedPara[0] = '3'
        curMatchingNode.concernedPara[1] = 'create map view'
    
    

def find(curNode, newCall):
#未找到时返回0，找到时返回匹配的节点
        #当前节点不可能为正在查找的节点，因为是从根节点开始查询的
        curNode = curNode.treeNode
        try:
            if len(curNode.leftChild) == 0:
                return 0
            elif curNode.leftChild[0].callName == newCall.callName:
                return curNode.leftChild[0]
            elif len(curNode.leftChild[0].rightChild) == 0:
                return 0
            elif curNode.leftChild[0].rightChild != []:
                for i in range(len(curNode.leftChild[0].rightChild)):
                    if curNode.leftChild[0].rightChild[i].callName == newCall.callName:
                        return curNode.leftChild[0].rightChild[i]
                return 0
            else:
                return 0
        except:
            print('find error')

def popItemInOpenedRes(call, openedRes):
    indexes = []
    try:    
        for i in range(len(openedRes)):
            if openedRes[i].dependencyPara == call.dependencyPara:
                indexes.append(i)       
    except:
        print("call.callName:" + call.callName)
    finally:
        if len(indexes) > 0:
            for i in indexes:
                openedRes.pop(i)
        return openedRes
        

def treeMatching(allStraces, tree):
    found = 0
    #因为可能有多个API同时执行，所以要保存指向每个API执行至的当前节点的指针
    curMatchingNodes = []
    
    #因为可能打开资源后进行多个操作，所以要保存所有打开的资源，在数组中保存指向打开资源操作的节点的指针
    curOpenedRes = []
    
    #保存匹配结果，以数组结构存储指向最后结果的节点的指针
    resultNodes = []
    unfinishedNodes = []
    
    curTreeRoot = MatchingNode(tree.root, 0)
    for call in allStraces:
        #如果curMatchingNodes为空，则将curMatchingNode添加至其中
        print(call.callName)
        if call.successStatus != 'failed':        
            if len(curMatchingNodes) == 0:
                curMatchingNode = MatchingNode(tree.root, call.dependencyPara)
                processAfterMatched(call, curMatchingNode)
                
                if curMatchingNode.concernedPara[2] == r'\Registry\Machine\Software\Policies\Microsoft\Windows\System':
                    print('none type')
                curMatchingNodes.append(curMatchingNode)
                
                #如果是打开资源操作，则先将curOpenedRes中相同依赖值的项删除，再将新资源添加至curOpenedRes中
                if call.callName in NtOpenRes:
                    popItemInOpenedRes(call, curOpenedRes)
                    curOpenedRes.append(curMatchingNode)
                    
            #以依赖参数为主要依据，符合才会继续在curMatchingNodes中查找
            for i in range(len(curMatchingNodes)):
                curMatchingNode = curMatchingNodes[i]
                if call.dependencyPara == curMatchingNode.dependencyPara:
                    print(curMatchingNode.treeNode.callName)
                    if find(curMatchingNode, call) != 0:
                        curMatchingNode.treeNode = find(curMatchingNode,call)
                        processAfterMatched(call, curMatchingNode)
                        curMatchingNodes[i] = curMatchingNode
                        found = 1
                        
                        #找到后，如果为NtClose，则从CurOpenedRes[]中删除对应dependencyPara的项
                        if call.callName == 'NtClose':
                            curOpenedRes = popItemInOpenedRes(call, curOpenedRes)
                        
                        #已经到达树的最后，则将当前分支的叶子节点添加至resultNodes中，并弹出curMatchingNodes中的当前节点 
                        if curMatchingNode.treeNode.leftChild[0].callName[:4] == 'leaf' and (len(curMatchingNode.treeNode.leftChild[0].rightChild) == 0):
                            if curMatchingNode.treeNode.leftChild[0].callName in leafSet:
                                curMatchingNode.concernedPara[1] = curMatchingNode.treeNode.leftChild[0].callName[4:]
                            resultNodes.append(curMatchingNode)
                            curMatchingNodes.pop(i)
                        break
            
            #如果未找到，则在打开的资源中查找，因为有可能是对同一资源进行的另一种操作
            if found == 0:
                for i in range(len(curOpenedRes)):
                    curMatchingNode = curOpenedRes[i]
                    if call.dependencyPara == curMatchingNode.dependencyPara:
                        #print(curMatchingNode.treeNode.callName)
                        if find(curMatchingNode, call) != 0:
                            curMatchingNode.treeNode = find(curMatchingNode,call)
                            processAfterMatched(call, curMatchingNode)
                            curMatchingNodes[i] = curMatchingNode
                            found = 1
                            
                            #找到后，如果为NtClose，则从CurOpenedRes[]中删除对应dependencyPara的项
                            if call.callName == 'NtClose':
                                curOpenedRes = popItemInOpenedRes(call, curOpenedRes)
                            
                            #已经到达树的最后，则将当前分支的叶子节点添加至resultNodes中，并弹出curMatchingNodes中的当前节点
                            if curMatchingNode.treeNode.leftChild[0].callName[:4] == 'leaf' and (len(curMatchingNode.treeNode.leftChild[0].rightChild) == 0):
                                if curMatchingNode.treeNode.leftChild[0].callName in leafSet:
                                    curMatchingNode.concernedPara[1] = curMatchingNode.treeNode.leftChild[0].callName[4:]
                                resultNodes.append(curMatchingNode)
                                curMatchingNodes.pop(i)
                            break        
                    
            #在curMatchingNodes中没有查找到，则从查找树的根重新查起            
            if found == 0:
                if find(curTreeRoot, call) != 0:
                    if find(MatchingNode(tree.root, call.dependencyPara), call) != 0 and find(MatchingNode(tree.root, call.dependencyPara), call) is not None:
                        curMatchingNode = MatchingNode(find(MatchingNode(tree.root, call.dependencyPara), call), call.dependencyPara)
                        processAfterMatched(call, curMatchingNode)
                        curMatchingNodes.append(curMatchingNode)
                    else: 
                        continue
                    
                    #如果是打开资源操作，则将其添加至curOpenedRes中
                    if call.callName in NtOpenRes:
                        popItemInOpenedRes(call, curOpenedRes)
                        curOpenedRes.append(curMatchingNode)
                        
                    if call.callName == 'NtClose':
                        curOpenedRes = popItemInOpenedRes(call, curOpenedRes)
                    
                    #已经到达树的最后，则将当前分支的叶子节点添加至resultNodes中，并弹出curMatchingNodes中的当前节点
                    if curMatchingNode.treeNode.leftChild[0].callName[:4] == 'leaf' and (len(curMatchingNode.treeNode.leftChild[0].rightChild) == 0):
                        if curMatchingNode.treeNode.leftChild[0].callName in leafSet:
                            curMatchingNode.concernedPara[1] = curMatchingNode.treeNode.leftChild[0].callName[4:]
                        resultNodes.append(curMatchingNode)
                        curMatchingNodes.pop(-1)
            found = 0
    
    #添加前先检查下个节点是否是leaf，或者下个节点是NtClose，下下个节点是leaf这两种情况，是的话则加入到resultNodes, 如果都不匹配，则将其加入unfinishedNodes中
    closeFlag = 0
    finishedFlag = 0
    
    for lastNode in curMatchingNodes:
        if len(lastNode.treeNode.leftChild) != 0:
            if lastNode.treeNode.leftChild[0].callName[:4] == 'leaf':
                if lastNode.treeNode.leftChild[0].callName in leafSet:
                    lastNode.concernedPara[1] = lastNode.treeNode.leftChild[0].callName[4:]
                resultNodes.append(lastNode)
                finishedFlag = 1
            elif len(lastNode.treeNode.leftChild[0].rightChild) != 0:
                for node in lastNode.treeNode.leftChild[0].rightChild:
                    if node.callName[:4] == 'leaf':
                        if node.callName in leafSet:
                            lastNode.concernedPara[1] = node.callName[4:]
                        resultNodes.append(lastNode)
                        finishedFlag = 1
                        break
            else:
                if lastNode.treeNode.leftChild[0].callName == 'NtClose':
                    closeFlag = 1
                elif len(lastNode.treeNode.leftChild[0].rightChild) != 0:
                    for node in lastNode.treeNode.leftChild[0].rightChild:
                        if node.callName == 'NtClose':
                            closeFlag = 1
                if closeFlag == 1:
                    if lastNode.treeNode.leftChild[0].leftChild[0].callName[:4] == 'leaf':
                        if lastNode.treeNode.leftChild[0].leftChild[0].callName in leafSet:
                            lastNode.concernedPara[1] = lastNode.treeNode.leftChild[0].leftChild[0].callName[4:]
                        resultNodes.append(lastNode)
                        finishedFlag = 1
                    elif len(lastNode.treeNode.leftChild[0].leftChild[0].rightChild) != 0:
                        for node in lastNode.treeNode.leftChild[0].leftChild[0].rightChild:
                            if node.callName[:4] == 'leaf':
                                if node.callName in leafSet:
                                    lastNode.concernedPara[1] = node.callName[4:]
                                resultNodes.append(lastNode)
                                finishedFlag = 1
        
        if finishedFlag == 0:
            unfinishedNodes.append(lastNode)
        closeFlag = 0
        finishedFlag = 0
    
    return resultNodes

