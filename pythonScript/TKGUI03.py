import os
import uuid
import json
import time
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msgBox
from ToolLib import testTool as ttool
cDir = os.getcwd()

listDirs = os.listdir(cDir)
# print(listDirs)
print(os.path.dirname(cDir))

root = tk.Tk()
winHeight = 700
winWidth = 1200

parentPath = os.path.dirname(cDir)
listOnlyFiles = []
listOnlyDirs = []
jsonDir = "pathFiles"
jsonFileName = "pathComment.json"
newChangeFrame = None

def getUIDD():
    return str(uuid.uuid4())

def getRoot():

    return root
def getDirs():
    for path in listDirs:
        if os.path.isfile(os.path.join(cDir, path)):
            listOnlyFiles.append(path)
            ttool.printInfo(path)
        else:
            listOnlyDirs.append(path)
            ttool.printInfo(path)

class FileReadExceptions(Exception):
    def __init__(self, msg):
        self.msg=msg
class FileRUpdateExceptions(Exception):
    def __init__(self, msg):
        self.msg=msg
# Analyze path informations
def getDirsByParams(childPath,flag=0):
    # 0 list of directory
    # 1 list of file
    childListDirs = os.listdir(childPath)
    cListOnlyFiles = []
    cListOnlyDirs = []
    for path in childListDirs:
        if os.path.isfile(os.path.join(childPath, path)):
            cListOnlyFiles.append(path)
            print("---output dirs:",path)
        else:
            cListOnlyDirs.append(path)
            print("***output files:",path)
    if flag == 0:
        return cListOnlyDirs
    elif flag == 1:
        return cListOnlyFiles
def createDir():
    if not os.path.exists(jsonDir):
        os.mkdir(jsonDir)
        print("Directory {} created successfully".format(jsonDir))
    else:
        print("Directory {} already exists".format(jsonDir))
def getJsonFile():
    saveLists=[]
    pahtJson = str(os.path.join(cDir,jsonDir,jsonFileName))
    try :
        with open(pahtJson,"r") as f:
            saveLists = json.load(f)
        print("*****getJsonFile****",saveLists)
    except FileNotFoundError:
        raise
    return saveLists

def getAnalyseJsonFile():
    saveLists =[]
    try :
        saveLists = getJsonFile()
    except FileNotFoundError:
        raise
    jsonFiles = {}
    for itemJson in saveLists:
        jsonFiles[itemJson['id']] = itemJson['fileName']

    return jsonFiles


def createJsonFile(checkJsons):
    saveJons = {}
    cListFiles = []
    saveCompleteJsons = []
    # Start running the program
    if len(checkJsons) == 0:
        cListFiles = listOnlyFiles
    # Only deleted files to end the program
    elif len(checkJsons) != 0 and checkJsons[0]==-1:
        return -1
    else:
        # pathJson = cDir + "\\" + \
        #    jsonDir + "\\" + \
        #    jsonFileName
        # fJson = open(pathJson,'r')
        # saveJons = json.load(fJson)
        # fJson.close()
        saveCompleteJsons = getJsonFile()
        saveJons = getAnalyseJsonFile()

        cListFiles = cListFiles + checkJsons
        # dictionary changed size during iteration lead to a error
        # Deleting key-value can lead to a error above
        recordDelDicts = []
        for keyName,itemJson in saveJons.items():
            for itemFile in cListFiles:
                if itemJson == itemFile:
                    recordDelDicts.append(keyName)
                    # del saveJons[keyName]
                    cListFiles.remove(itemFile)
                    break
        # Delete key-value in the Dicts and value in the lists
        for record in recordDelDicts:
            del saveJons[record]
        for itemJson in saveCompleteJsons:
            for record in recordDelDicts:
                # del saveJons[record]
                if record == itemJson['id']:
                    saveCompleteJsons.remove(itemJson)
    # create and add
    # temp = "path:" + "\n" + "createTime:"+"\n" + "comment:"+"\n"
    temp = "comment:"+"\n"
    dateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # Only deleted files
    if len(cListFiles) == 0:
        pahtJson = str(os.path.join(cDir,jsonDir,jsonFileName))
        with open(pahtJson, 'w') as f:
            json.dump(saveCompleteJsons, f)
        print(saveCompleteJsons)

    # create the json and comment files
    # add some comment files
    saveLists = saveCompleteJsons
    for itemFileName in cListFiles:
        uuidObj = getUIDD()
        uuidObjStr = cDir+ "\\" + jsonDir + "\\" + uuidObj  + '.txt'
        # saveJons[uuidObj] = itemFileName
        saveJons ={}
        # dateTime = time.localtime(time.time())
        dateJsonTime = time.time()

        saveJons["id"] = uuidObj
        saveJons["fileName"] = itemFileName
        saveJons["createTime"] = dateJsonTime
        saveJons["updateTime"] = dateJsonTime
        saveLists.append(saveJons)

        temp = "fileName:"+ itemFileName +"\n"+ \
            "path:" + uuidObjStr+ "\n" + \
            "createTime:"+dateTime+"\n"+ temp
        commentFile = open(uuidObjStr,'w')
        commentFile.write(temp)
        commentFile.close()
        temp = "comment:" + "\n"
    #Save a json file
    pahtJson = str(os.path.join(cDir,jsonDir,jsonFileName))
    with open(pahtJson, 'w') as f:
        json.dump(saveLists, f)
    print(saveLists)

def checkFiles():
    checkJsons = []
    pathJson = cDir + "\\" + \
           jsonDir + "\\" + \
           jsonFileName
    try:

        # fJson = open(pathJson,'r')
        # jsonDatas = json.load(fJson)
        # Retrieve JSON data from local saving location
        jsonDatas = getAnalyseJsonFile()
        print("---output jsonDatas:",jsonDatas)
        # Deal with json file associated with the comment file
        # fJson.close()
        flagExist = True
        recordDelDicts = []
        for itemFile in listOnlyFiles:
            flagExist = False
            # for itemJson in jsonDatas.values():
            for keyName,itemJson in jsonDatas.items():
                # print(itemJson)
                if itemFile == itemJson:
                    print("A File has been exist already")
                    recordDelDicts.append(keyName)
                    # del jsonDatas[keyName]
                    flagExist = True
                    break
            if flagExist == False:
                checkJsons.append(itemFile)
        for record in recordDelDicts:
            del jsonDatas[record]
        #delete file
        if len(jsonDatas) == 0 and len(checkJsons) == 0:
            raise FileRUpdateExceptions("Files not any changes")
        else:
            # Delete comment  file  associated with file which need to be noted
            for keyName,itemFile in jsonDatas.items():
                checkJsons.append(itemFile)
                keyName = str(keyName+".txt")
                if os.path.exists(os.path.join(cDir,jsonDir,keyName)):
                    os.remove(os.path.join(cDir,jsonDir,keyName))
                else:
                    raise FileReadExceptions("A File fail to delete")
        print("***checkJsons***:",checkJsons)
        # Not add files
        if len(checkJsons) == 0:
            checkJsons.append(-1)

    except FileNotFoundError:
        print("File not found, please is that file path")
        createDir()
        createJsonFile(checkJsons)
        raise
    except FileReadExceptions as e:
        print("---error:",e.msg)
        sys.exit(-1)
    except FileRUpdateExceptions as e:
        print("---warning:",e.msg)
        raise
    return checkJsons





def center_window(croot,width,height):
    screen_width = croot.winfo_screenwidth()
    screen_height = croot.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    croot.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

def setNewChangeFrame(newTChangeFrame):
    print("++++++++++++",newTChangeFrame)
    global newChangeFrame
    newChangeFrame = newTChangeFrame

def getNewChangeFrame():
    return newChangeFrame



# 鼠标选中一行回调
def selectTree(tree,croot,cFrame):
    newFrame=None
    for item in tree.selection():
        # print(cFrame)
        item_text = tree.item(item,"values")
        if str(item) == "oneItem":
            newFrame = firstChangeFrame(croot,cFrame)
        else:
            newFrame = generalChangeFrame(croot,cFrame,item)
        setNewChangeFrame(newFrame)
        print(item_text,item)

def style_treeview(ctree):
    style = ttk.Style()
    # Heading style
    style.configure('Treeview.Heading', font=('Arial bold', 14), foreground='black', background='gray')
    # 设置Treeview的背景色
    # "light blue"
    style.configure("mystyle.Treeview", background='gray',font=('Sans-Serif', 14),rowheight=28,borderwidth=3,bordercolor="blue")

    # style.configure("Treeview", background="white", bordercolor="blue", borderwidth=2)
    ctree.tag_configure('oddrow', background='#FFEFD5')
    ctree.tag_configure('evenrow', background='#FFFACD')
    # 设置Treeview中奇数行的背景色
    # style.map("mystyle.Treeview", background=[('rowaltshift', "light green")])
    # style.map("mystyle.Treeview", )
    return style

def saveTextCallBack(croot,cFrame,cText,uuid):
    try:
        uuidNameFile = uuid + ".txt"
        # uuidNameFile = uuid
        textContext = cText.get('0.0',tk.END)
        commentNameFile = os.path.join(cDir,jsonDir,uuidNameFile)

        if not os.path.exists(commentNameFile):
            with open(commentNameFile,"w") as f:
                f.write(textContext)
        else:
           with open(commentNameFile,"w") as f:
                f.write(textContext)
        msgBox.showinfo("Save","Save successfully")

    except FileExistsError:
        print("FileSaveError")

def insertTextCallBack(saveText,insertText):

     textContext = insertText.get('0.0',tk.END)
     textContext = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+": "+textContext+"\n"
     saveText.insert(tk.END,textContext)


def generalChangeFrame(croot,cFrame,uuid):

    saveLists = getJsonFile()
    newRightFrame = tk.Frame(croot)

    newRightFrameChild01 = tk.Frame(newRightFrame,background="#FFFFFF")
    newRightFrameChild02 = tk.Frame(newRightFrame,background="#FFFFFF")
    newRightFrameChild03 = tk.Frame(newRightFrame,background="#FFFFFF")
    newRightFrameChild04 = tk.Frame(newRightFrame,background="#FFFFFF")
    newRightFrameChild05 = tk.Frame(newRightFrame,background="#FFFFFF")
    newRightFrameChild06 = tk.Frame(newRightFrame,background="#DCDCDC")
    newRightFrameChild01.pack(side="top",fill="both")
    newRightFrameChild02.pack(side="top",fill="both")
    newRightFrameChild03.pack(side="top",fill="both")
    newRightFrameChild04.pack(side="top",fill="both")
    newRightFrameChild05.pack(side="top",fill="both")
    newRightFrameChild06.pack(side="top",fill="both")

    newRightFrameChild03_01 = tk.Frame(newRightFrameChild03,background="#FFFFFF")
    newRightFrameChild03_02 = tk.Frame(newRightFrameChild03,background="#FFFFFF")
    newRightFrameChild03_01.pack(fill="both",expand=True,side="left")
    newRightFrameChild03_02.pack(fill="both",expand=True,side="left")
    newRightFrameChild05_01 = tk.Frame(newRightFrameChild05,background="#000000")
    newRightFrameChild05_02 = tk.Frame(newRightFrameChild05,background="#000000")
    newRightFrameChild05_01.pack(fill="both",expand=True,side="left")
    newRightFrameChild05_02.pack(fill="both",side="left")

    titleLabel = tk.Label(newRightFrameChild01,text="Files details",height=3,bd=5,font="Helvetica 14",bg='yellow')
    titleLabel.pack(fill="both",expand=True)
    fileName = None
    createTime = None
    updateTime = None

    for itemJosn in getJsonFile():
        if itemJosn["id"] == uuid:
            fileName = itemJosn["fileName"]
            createTime = itemJosn["createTime"]
            updateTime = itemJosn["updateTime"]
            break


    fileNameLable = tk.Label(newRightFrameChild02,text="File Name:",height=2,font="Helvetica 14",background="#FFFFFF")
    fileContentLable = tk.Label(newRightFrameChild02,text=fileName,font="Helvetica 12",background="#FFFFFF")
    fileNameLable.pack(fill="both",side="left")
    fileContentLable.pack(fill="both",side="left")



    createTimeNameLabel = tk.Label(newRightFrameChild03_01,text="Create Time:",height=2,font="Helvetica 14",background="#FFFFFF")
    createTimeContentLabel = tk.Label(newRightFrameChild03_01,text=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(createTime)),height=2,font="Helvetica 12",background="#FFFFFF")
    createTimeNameLabel.pack(fill="both",side="left")
    createTimeContentLabel.pack(fill="both",side="left")

    updateTimeNameLabel = tk.Label(newRightFrameChild03_02,text="Update Time:",height=2,font="Helvetica 14",background="#FFFFFF")
    updateTimeContentLabel = tk.Label(newRightFrameChild03_02,text=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(updateTime)),height=2,font="Helvetica 12",background="#FFFFFF")
    updateTimeNameLabel.pack(fill="both",side="left")
    updateTimeContentLabel.pack(fill="both",side="left")

    text = tk.Text(newRightFrameChild04,font="Helvetica 12",height=15)
    context = "This is an empty file"
    try:
        uuidNameFile = uuid+".txt"
        # uuidNameFile = "5aea33d3-f188-4fc4-8258-30c3112821bc.txt"
        commentNameFile = os.path.join(cDir,jsonDir,uuidNameFile)
        if os.path.exists(commentNameFile):
                with open(commentNameFile,"r") as f:
                    strartMark = float(1)
                    for eline in f.readlines():
                        text.insert(tk.END,eline)
                        elineLen = eline.split(":")
                        if len(elineLen[0]) < 10:
                            endMark =strartMark + len(elineLen[0])*0.1+0.1
                            strartMark = "{:.1f}".format(strartMark)
                            endMark = "{:.1f}".format(endMark)
                        elif len(elineLen[0]) >= 10 :
                            endMark =strartMark + len(elineLen[0])*0.01+0.01
                            strartMark = "{:.2f}".format(strartMark)
                            endMark = "{:.2f}".format(endMark)
                        text.mark_set("startMark",strartMark)
                        text.mark_set("endMark",endMark)
                        strartMark = float(strartMark)+1
                        endMark = strartMark
                        # context = f.readline()
                        text.tag_add("tag1","startMark","endMark")
                        text.tag_config('tag1', foreground='black', font="Arial 16",background='lightyellow')
                    # context = f.read()
        else:
            raise FileReadExceptions("A File fail to be found")
        # text.insert(tk.END,context)

    except FileExistsError:
        print("FileExistsError")
    except FileReadExceptions as e:
        print("---error:",e.msg)
        sys.exit(-1)
    text.pack(fill="both",expand=True)

    # insert a new comment
    insertText =tk.Text(newRightFrameChild05_01,font="Helvetica 12",height=10)
    insertText.pack(fill="both",expand=True)
    insertButton = tk.Button(newRightFrameChild05_02,text="Submit",width=10,background="#FFA07A",command=lambda : insertTextCallBack(text,insertText))
    # background color
    insertButton.pack(side="top")
    insertLabel = tk.Label(newRightFrameChild05_02,text="",background="#F5F5F5")
    insertLabel.pack(fill='both',expand=True,side="top")

    # save files uuid
    saveButton = tk.Button(newRightFrameChild06,text="Save",width=6,background="yellow",command=lambda : saveTextCallBack(root,newRightFrameChild05,text,uuid))

    saveButton.pack(side="right",expand=True)

    cFrame.destroy()
    newRightFrame.pack(fill="both",expand=True,side="left")
    setNewChangeFrame(newRightFrame)
    return newRightFrame

def firstChangeFrame(croot,cFrame):
    if cFrame != None:
        cFrame.destroy()
    rightFrame = tk.Frame(croot,background="#FFFFFF")
    rightTopTitle = tk.Label(rightFrame,text="File lists",height=3,bd=5,font="Helvetica 14",bg='yellow')
    rightTopTitle.pack(fill="both",side="top")

    columns = ("Number","fileName","createTime","updateTime")

    rightTree = ttk.Treeview(rightFrame, show = "headings", columns = columns, selectmode = tk.BROWSE,style='mystyle.Treeview')
    # Treeview background color
    testStandard={"id":"15484","fileNmae":"test01.txt","createTime":"s54241248","updateTime":"5465454"}



    style_treeview(rightTree)
    rightTree.column("Number", anchor = "center")
    rightTree.column("fileName", anchor = "center")
    rightTree.column("createTime", anchor = "center")
    rightTree.column("updateTime", anchor = "center")

    rightTree.heading("Number", text = "Number")
    rightTree.heading("fileName", text = "File Name")
    rightTree.heading("createTime", text = "Create Time")
    rightTree.heading("updateTime", text = "Update Time")

    listFileNames = getJsonFile()
    for iSort in range(len(listFileNames)):
        listFileNames[iSort]['Number'] = iSort+1
        listFileNames[iSort]['createTime'] = time.strftime("%Y-%m-%d", time.localtime(listFileNames[iSort]['createTime']))
        listFileNames[iSort]['updateTime'] = time.strftime("%Y-%m-%d", time.localtime(listFileNames[iSort]['updateTime']))

    # listFileNames = [{"Number": "0", "FileName": "test01.txt", "createTime": "154878", "updateTime": "154878"},{"Number": "1", "FileName": "test02.txt", "createTime": "154878", "updateTime": "154878"}]
    for i in range(len(listFileNames)):
        flagTags = 2
        tagsStr = ""
        if i%flagTags == 0:
            tagsStr = "evenrow"
        else:
            tagsStr = "oddrow"
        rightTree.insert("",i,values=(listFileNames[i].get('Number'),listFileNames[i].get('fileName'),listFileNames[i].get('createTime'),listFileNames[i].get('updateTime')),tags=(str(tagsStr),))


    rightTree.pack(expand = True, fill = tk.BOTH,side="left")
    rightFrame.pack(fill="both",expand=True,side="left")

    firstChangeFrameButton(croot,rightFrame,listFileNames)
    return rightFrame

def getButtonCallBack(croot,cFrame,uuid):
    # print("getButtonCallBack:",uuid)
    generalChangeFrame(croot,cFrame,uuid)
    # msgBox.showinfo( "Hello Python", str(uuid))


def firstChangeFrameButton(croot,cFrame,listFileNames):

    for i in range(len(listFileNames)):
        if i == 0:
            rightLable = tk.Label(cFrame,text="",background="#FFFFFF")
            rightLable.pack(side="top")
        # rightButton = tk.Button(cFrame,text="Edit",height=1,width=8,padx=0)
        # Binding parameters between buttons and callback functions and variable parameters.
        rightButton = tk.Button(cFrame,text="Edit",width=8,padx=0,pady=0,command=lambda tempIdName = listFileNames[i]["id"] : getButtonCallBack(croot,cFrame,tempIdName))

        rightButton.pack(side="top")

    cFrame.pack(fill="both",expand=True,side="right",ipadx=0)



def createGUI(croot):

    saveJons={}
    '''
    pahtJson = str(os.path.join(cDir,jsonFileName))
    with open(pahtJson,'r') as f:
        saveJons = json.load(f)
        print("Test GUI",saveJons)
    '''
    pahtJson = getJsonFile()
    center_window(croot,width=winWidth,height=winHeight)
    leftFrame = tk.Frame(croot)

    # rightFrame = tk.Frame(croot)
    rightFrame = None
    croot.title("Test comment")
    text01 = tk.Text(leftFrame, height=2, width=15)
    # text01.grid(row=0,column=0)


    # leftFrame.pack(fill='both',expand=True,side="left")
    leftFrame.pack(fill='both',side="left",expand=True)
    tree = ttk.Treeview(leftFrame, show = "tree")
    myid=tree.insert("",0,"oneItem",text="File Menus",values=("1"))  # ""表示父节点是根

    '''
    for i in range(len(listOnlyFiles)):
        myidx1=tree.insert(myid,i,str(listOnlyFiles[i]),text=str(listOnlyFiles[i]),values=(str(i+2)))
    '''
    for i in range(len(getJsonFile())):
        myidx1=tree.insert(myid,i,str(getJsonFile()[i]['id']),text=str(getJsonFile()[i]['fileName']),values=(str(i+2)))
    # myidx1=tree.insert(myid,0,"广东",text="中国广东",values=("2"))  # text表示显示出的文本，values是隐藏的值
    # myidx2=tree.insert(myid,1,"江苏",text="中国江苏",values=("3"))
    # myidy=tree.insert("",1,"美国",text="美国USA",values=("4"))
    # myidy1=tree.insert(myidy,0,"加州",text="美国加州",values=("5") )

    # 获取所有顶级项
    # items = [item for item in tree.get_children('') if tree['item'] == '']

    listTrees = tree.get_children()
    for i in listTrees:
        tree.item(i,open=True)
        print(tree.item(i,"values"))
    # tree.grid(row=0,column=0)
    tree.pack(fill=tk.BOTH,side="left",expand=True)
    # 选中行
    rightFrame = firstChangeFrame(croot,None)
    setNewChangeFrame(rightFrame)

    tree.bind('<<TreeviewSelect>>', lambda event: selectTree(tree,root,getNewChangeFrame()))

    croot.mainloop()


'''
    rightTopTitle = tk.Label(rightFrame,text="File lists",height=3,bd=5,font="Helvetica 14",bg='yellow')
    rightTopTitle.pack(fill="both",side="top")

    columns = ("Number","FileName","createTime","updateTime")

    rightTree = ttk.Treeview(rightFrame, show = "headings", columns = columns, selectmode = tk.BROWSE,style='mystyle.Treeview')
    # Treeview background color
    style_treeview(rightTree)
    rightTree.column("Number", anchor = "center")
    rightTree.column("FileName", anchor = "center")
    rightTree.column("createTime", anchor = "center")
    rightTree.column("updateTime", anchor = "center")

    rightTree.heading("Number", text = "Number")
    rightTree.heading("FileName", text = "File Name")
    rightTree.heading("createTime", text = "Create Time")
    rightTree.heading("updateTime", text = "Update Time")

    listFileNames = [{"Number": "0", "FileName": "test01.txt", "createTime": "154878", "updateTime": "154878"},{"Number": "1", "FileName": "test02.txt", "createTime": "154878", "updateTime": "154878"}]
    for i in range(len(listFileNames)):
        flagTags = 2
        tagsStr = ""
        if i/flagTags == 0:
            tagsStr = "evenrow"
        else:
            tagsStr = "oddrow"
        rightTree.insert("",i,values=(listFileNames[i].get('Number'),listFileNames[i].get('FileName'),listFileNames[i].get('createTime'),listFileNames[i].get('updateTime')),tags=(tagsStr,))


    rightTree.pack(expand = True, fill = tk.BOTH,side="left")

    text02 = tk.Text(rightFrame, height=2, width=15)
    # text02.pack()


    rightFrame.pack(fill="both",expand=True,side="left",ipadx=0)
    '''
    # croot.mainloop()

def createTempJsonFile():
    saveLists = []
    # dateTime = time.localtime(time.time())
    dateTime = time.time()
    for itemFileName in listOnlyFiles:
        saveJons ={}
        uuidObj = getUIDD()
        saveJons["id"] = uuidObj
        saveJons["fileName"] = itemFileName
        saveJons["createTime"] = dateTime
        saveJons["updateTime"] = dateTime
        saveLists.append(saveJons)
    pahtJson = str(os.path.join(cDir,jsonFileName))
    with open(pahtJson, 'w') as f:
        json.dump(saveLists, f)
    print(saveLists)
    return saveLists
def show(text):
    print('INSERT  ：', text.index(tk.INSERT))
    print('CURRENT ：', text.index(tk.CURRENT))
    print('END     ：', text.index(tk.END))
    print(type(text.index(tk.END)))

def TestMark():
    uuidNameFile = "0b759ad0-96e7-43a8-8546-9bd0a336f5c7.txt"
    commentNameFile = os.path.join(cDir,jsonDir,uuidNameFile)
    text = tk.Text(root,font="Courier 14")
    button = tk.Button(root, text="Print", command=lambda :show(text))
    button.pack(pady=3)

    if os.path.exists(commentNameFile):
        with open(commentNameFile,"r") as f:
            strartMark = float(1)
            for eline in f.readlines():
                text.insert(tk.END,eline)
                elineLen = eline.split(":")
                if len(elineLen[0]) < 10:
                    endMark =strartMark + len(elineLen[0])*0.1+0.1
                    strartMark = "{:.1f}".format(strartMark)
                    endMark = "{:.1f}".format(endMark)
                elif len(elineLen[0]) >= 10 :
                    endMark =strartMark + len(elineLen[0])*0.01+0.01
                    strartMark = "{:.2f}".format(strartMark)
                    endMark = "{:.2f}".format(endMark)
                text.mark_set("startMark",strartMark)
                text.mark_set("endMark",endMark)
                strartMark = float(strartMark)+1
                endMark = strartMark
                # context = f.readline()
                text.tag_add("tag1","startMark","endMark")
                text.tag_config('tag1', foreground='black', font="Arial 16",background='lightyellow')
        # Number format
        num = 123.4567
        formatted_num = "{:.2f}".format(num)
        print(type(formatted_num))
        ttool.printMsg(text.get("startMark","endMark"))
        text.pack(fill=tk.BOTH,expand=True)


        root.mainloop()


    else:
        raise FileReadExceptions("A File fail to be found")


if __name__=="__main__":
    getDirs()
    # TestMark()
    # '''
    try:
        res = checkFiles()
    except FileNotFoundError:
        print("---warning:a file do not exist")
    except FileRUpdateExceptions as e:
        print("---warning:",e.msg)
    else:
        createJsonFile(res)
    # '''
    # createJsonFile()
    createGUI(getRoot())
    # print(getAnalyseJsonFile())
    # createJsonFile()




