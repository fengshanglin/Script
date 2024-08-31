#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   textStyle.py
@Time    :   2024/08/31 10:36:28
@Author  :   linchen
@Version :   1.0
@Desc    :   None
'''
import sys
# from ..ToolLib import testTool as ttool
class TestStyleClass:
    root = None
    normal_tag = "normal"
    heading_tag = "heading"
    bold_tag = "bold"
    italic_tag = "italic"

    bold_tag = ("<b>","</b>")
    italic_tag = ("<i>","</i>")
    htmlTags = [{"nameTag":"boldTag","valueTag":bold_tag},{"nameTag":"italicTag","valueTag":italic_tag}]


    def __init__(self,*args,**kwargs) -> None:
        if args or kwargs:
            self.root = args
        else:
            self.args = ()
            self.kwargs = {}

    def get_item_mark(self,nameTag):

        for itemTag in self.htmlTags:
            if nameTag == itemTag['nameTag']:
                return itemTag["valueTag"]


    def set_text_style_temp(self,text):

        '''
        text.insert(tk.INSERT, "这是一个普通段落。\n", normal_tag)
        text.insert(tk.INSERT, "\n", "bold_tag")
        text.insert(tk.INSERT, "这是粗体文本。\n", bold_tag)
        text.insert(tk.INSERT, "\n", "italic_tag")
        text.insert(tk.INSERT, "这是斜体文本。\n", italic_tag)
        text.insert(tk.INSERT, "\n", "heading_tag")
        text.insert(tk.INSERT, "这是一个标题\n", heading_tag)
        '''
        text.tag_config(normal_tag, font=Font(family="Helvetica", size=12))
        text.tag_config(heading_tag, font=Font(family="Helvetica", size=14, weight="bold"))
        text.tag_config(bold_tag, font=Font(family="Helvetica", size=12, weight="bold"))
        text.tag_config(italic_tag, font=Font(family="Helvetica", size=12, slant="italic"))
    def text_print(self):
        print("********test*******")


    def text_cotent(self,content):

        return ""

    def text_bold_tag(self,content):

        return "<b>"+content+"</b>"

    def text_italic_tag(self,content):

        return "<i>"+content+"</i>"

    def parse_html_to_tag_location(self,content):
        content = f"{content}"
        stratTag = None
        endTag = None
        locationTag = {"nameTag":"","stratTag":"","endTag":"","flagLength":""}
        locationTagLists = []
        for iHtmlTag in self.htmlTags:
            stratTag=content.find(f"{iHtmlTag['valueTag'][0]}")
            if stratTag != -1:
               #Get flag strating location
               locationTag["nameTag"] = f"{iHtmlTag['nameTag']}"
               locationTag["stratTag"] = stratTag
               locationTag["endTag"] =content.find(f"{iHtmlTag['valueTag'][1]}")
               locationTag["flagLength"] = len(f"{iHtmlTag['valueTag'][0]}")
               locationTagLists.append(locationTag)
            # print(stratTag,iHtmlTag,endTag)

        # stratTag = locationTagLists[0]["stratTag"] + locationTagLists[0]["flagLength"]
        # print(locationTagLists,content[stratTag:locationTagLists[0]["endTag"]])
        return locationTagLists
    def parse_tag_to_html_location(self,text):
        lineNumber = int(float(text.index('end')))-1
        # bold_tag = ("<b>","</b>")
        # italic_tag = ("<i>","</i>")
        # htmlTags = [{"nameTag":"boldTag","valueTag":bold_tag},{"nameTag":"italicTag","valueTag":italic_tag}]
        locationMarkLists = []
        for iNum in range(1,lineNumber):
            lineContent = text.get(f"{iNum}.0",f"{iNum}.end")
            markTuple = text.mark_names()[2:-1]
            flag = None
            startMark = None
            endMark = None
            locationMark = {"nameTag":"","stratTag":"","endTag":"","lineNumber":"","flagLength":""}
            for iHtmlTag in self.htmlTags:
                flagMark = True
                iHtmlTagStr = iHtmlTag['valueTag'][0]
                for iMarkTuple in markTuple:
                   if iMarkTuple.find(iHtmlTagStr) == -1:
                       flagMark = False
                       continue
                   else:
                        flagMark = True
                        flag=iHtmlTagStr
                        break
                if flagMark:
                    tempMarkStr = flag + str(iNum)
                    startMark = text.index(tempMarkStr)
                    endMark = text.index(iHtmlTag['valueTag'][1]+str(iNum))
                    locationMark["nameTag"] = iHtmlTag["nameTag"]
                    locationMark["stratTag"] = startMark
                    locationMark["endTag"] = endMark
                    locationMark["lineNumber"] = str(iNum)
            locationMarkLists.append(locationMark)
        return locationMarkLists
    def set_text_style(self,text,content,iNumer):
        strartMarkStr = ""
        endMarkStr = ""
        newLineContent = ""
        markLists = self.parse_html_to_tag_location(content)
        if len(markLists) == 0:
            return -1
        for itemMark in markLists:
            stratTag = itemMark['stratTag']
            endTag = itemMark['endTag']
            # head
            # newLineContent = eline[0:stratTag]+newLineContent
            # middle
            stratTag = stratTag+itemMark['flagLength']
            newLineContent = newLineContent + content[stratTag:endTag]
            # tail
            endTag = itemMark['endTag'] + itemMark['flagLength']+1
            newLineContent = newLineContent + content[endTag:-1]
            itemMark['endTag'] = itemMark['endTag'] - itemMark['flagLength']
            # text.tag_names()
            text.insert("end",newLineContent+"\n")
            for itemMark in markLists:
                valueMark = self.get_item_mark(itemMark["nameTag"])
                strartMarkStr = valueMark[0]
                endMarkStr = valueMark[1]
                startMark = f"{iNumer}.{itemMark['stratTag']}"
                endMark = f"{iNumer}.{itemMark['endTag']}"
                strartMarkStr= strartMarkStr + f"{iNumer}"
                endMarkStr = endMarkStr + f"{iNumer}"
                text.mark_set(strartMarkStr,startMark)
                text.mark_set(endMarkStr,endMark)
                text.tag_add("tag1",strartMarkStr,endMarkStr)
            text.tag_config('tag1', foreground='black', font="Arial 16",
            background='lightyellow')
            iNumer = iNumer + 1
            return iNumer

if __name__ == "__main__":
    test = TestStyleClass()
    test.text_print()
    # ttool.printMsg("aa")
    sys.path.append("e:\\learning_materials\\python_pros\\packages\\ToolLib")
    print(test.parse_html_to_tag_location("dasdasdd<b>sdasdasdas</b>asdsadas"))

    print("/")
