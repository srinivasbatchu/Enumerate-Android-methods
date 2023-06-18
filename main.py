import os, fnmatch

path = r"C:\Users\Srinivas\AppData\Local\Android\Sdk\sources\android-30\android"
# filename = 'MediaDrm.java'
# filePath = os.path.join(path, filename)
package = ''
methods = []
currentBlockCount = 0
classnamesState = ['']

def isPackage(line):
    return 'package ' in line

def getPackage(line):
    if(isPackage(line)):
        return (line.split("package ")[1]).strip()[:-1]

def isClass(line):
    return ' class ' in line

def getClassName(line):
    if(isClass(line)):
        return (line.split('class ')[1]).split()[0]

def isMethod(line):
    return ' public ' in line and '(' in line and ' class ' not in line

def getMethodName(line):
    if(isMethod(line)):
        words = line.split()
        for word in words:
            if "(" in word:
                return word.split('(')[0]

def getChangeInBlocks(line):
    return line.count('{')-line.count('}')

# Tracking nested classes based on current block in nested blocks. Below an example, explaining the state of multiple levels of nested classes.
# ---------
# 0 ''
# 1 'A'
# 2 'A'
# 3 'A.B'
# 4 'A.B'
# 5 'A.B'
# 6 'A.B.C'
# 7 'A.B.C'
# ---------
# 0 ''
# 1 'A'
# 2 'A'
# 3 'A.B'
# 4 'A.B'
# 5 'A.B'
# 6 'A.B.D'
# 7 'A.B.D'
# 8 'A.B.D'
# 9 'A.B.D'
# ---------
# 0 ''
# 1 'A'
# 2 'A'
# 3 'A.C'
# 4 'A.C'
# ---------
def getCurrentBlockClassname(line):
    global currentBlockCount
    changeInBlocks = getChangeInBlocks(line)
    currentBlockCount = currentBlockCount + changeInBlocks

    if isClass(line):
        if classnamesState[-1] == '':
            newClassName = getClassName(line)
        else:
            newClassName = classnamesState[-1]+'.'+getClassName(line)
        classnamesState.append( newClassName )
    elif changeInBlocks > 0:
        for i in range(changeInBlocks):
            classnamesState.append( classnamesState[-1] )
    elif changeInBlocks < 0:
        del classnamesState[changeInBlocks:]

    return classnamesState[-1]

def resetForNewFile():
    package = ''
    methods = []
    currentBlockCount = 0
    classnamesState = ['']

filePaths = []
for root, dirnames, filenames in os.walk(path):
    for filename in fnmatch.filter(filenames, '*.java'):
        filePaths.append(os.path.join(root, filename))


for i, filePath in enumerate(filePaths):
    res = []
    # res.append(filePath)
    print("{} {}".format(i, filePath))

    with open(filePath, encoding="utf-8") as f:
        fileContent = f.read()

        lines = fileContent.splitlines()
        linesWithoutComments = list(filter(lambda x: ('/' not in x) and ('*' not in x), lines))
        InterestedLines = list(filter(lambda x: ('{' in x) or ('}' in x) or (isMethod(x)) or (isClass(x)) or (isPackage(x)), linesWithoutComments))
        
        for line in InterestedLines:
            # try:
                if package == '':
                    package = getPackage(line)
                
                # currentClassName = getCurrentBlockClassname(line)
                # print("filePath: {}".format(filePath))
                # print("Line: {}".format(line))
                # print("isPackage(): {}".format(isPackage(line)))
                # print("getPackage(): {}".format(getPackage(line)))
                # print("isClass(): {}".format(isClass(line)))
                # print("getClassName(): {}".format(getClassName(line)))
                # print("isMethod(): {}".format(isMethod(line)))
                # print("getMethodName(): {}".format(getMethodName(line)))
                # print("getChangeInBlocks(): {}".format(getChangeInBlocks(line)))
                # # print("getCurrentBlockClassname(): {}".format(currentClassName))
                # print("currentBlockCount: {}".format(currentBlockCount))
                # print("classnamesState: {}".format(classnamesState))

                if(isMethod(line)):
                    # res.append("{} / {} / {}.{}()".format(filePath, package, currentClassName, getMethodName(line)))
                    res.append("{} / {} / {}()".format(filePath, package, getMethodName(line)))
                
                # print("--------------------------------------")
                # print("")
            # except:
            #     print("Error while parsing line:")
            #     print(line)
    
    resetForNewFile()
    
    resStr = "\r\n".join(res)

    wf = open('output.txt', 'a')
    wf.write(resStr+"\r\n")
    wf.close()

