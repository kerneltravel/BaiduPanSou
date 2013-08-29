#!/usr/bin/python
#!encoding:utf-8
#!filename:Baidu_Pan_Sou.py
"""
Copyright 2013 BaiduPan_Sou
=======================================
author          = "Sam Huang"
name            = "Baidu_Pan_Sou"
version         = "0.4"
url             = "http://www.hiadmin.org"
author_email    = "sam.hxq@gmail.com"
=========================================

根据用户输入的内容去百度搜索引中搜索特定网站pan.baidu.com的内容
"""

import re
import webbrowser
import requests
from tkinter import *


def PanSou(name,site="pan.baidu.com"):
    """获取用户输入的内容、然后去百度搜索引擎中搜索此内容是否存在于pan.baidu.com网站中
    返回url和name并写入到对应的列表中
    """

    Url = r"http://www.baidu.com/s?wd=%s+site: %s" %(name,site)
    Url2 = r"http://www.baidu.com/s?wd=%s+site: %s&pn=10&ie=utf-8" %(name,site)
    RegUrl = r"(href=\")(http://www.baidu.com/link.*)(\")"
    RegUrlList = r"(<a href=\")(/s\?wd=.*=utf-8)(\"><span class=\"fk)" #判读分页是否存在
    RegName = r"(文件名:)(.*)(文件大小:)"
    global PageNameList
    global PageUrlList
    PageNameList = []
    PageUrlList = []


    r = requests.get(Url)
    if r.status_code == 200:
        text = r.text
        #获取搜索结果中的页面标题
        if re.search(RegName,text) != None:
            PageName_temp = re.findall(RegName, text)
            for i in PageName_temp:
                PageNameList.append(i[1])

        #获取搜索结果中的url地址
        if re.search(RegUrl,text) != None:
            PageUrl_temp = re.findall(RegUrl,text)
            for i in PageUrl_temp:
                PageUrlList.append(i[1])

    #判断分页是否存在、如存在就把分页地址传入进去
    if re.search(RegUrlList,text) != None:
        r2 = requests.get(Url2)
        if r2.status_code == 200:
            text2 = r2.text

            #获取搜索结果中的页面标题
            if re.search(RegName,text2) != None:
                PageName_temp = re.findall(RegName, text2)
                for i in PageName_temp:
                    PageNameList.append(i[1])

            #获取搜索结果中的url地址
            if re.search(RegUrl,text2) != None:
                PageUrl_temp = re.findall(RegUrl,text2)
                for i in PageUrl_temp:
                    PageUrlList.append(i[1])





def ConentIntegrity():
    """将PageNameList和PageUrlList列表做好对应关系
    连接2个列表中的值、吧内容插入到listbox中显示
    """
    regex = "</?em>" 
    repl = ""
    x = 0
    for i in PageNameList:
        PageName_temp = PageNameList[x]
        PageName = re.sub(regex,repl,PageName_temp) #蒋name中</em>的替换成空
        PageUrl = PageUrlList[x]
        listboxName.insert(END,PageName)
        listboxUrl.insert(END,PageUrl) #吧内容插入到listbox中展示
        x = x+1 #每次增1，知道list循环结束



if __name__ == "__main__":

    root = Tk()
    root.title("百度网盘搜索工具V0.4")
    root.iconbitmap("baidupan_32.ico")
    root.geometry("700x450")
    root.resizable(False,False) #固定窗口大小

    entry = Entry(root,width=41)
    entry.pack(side=TOP,anchor="nw")

    def callback():
        """设置button事件
        当点击button的时候、获取entry里面的输入内容
        并吧内容作为参数传递给PanSou(函数)
        """
        listboxUrl.delete(0,END)
        listboxName.delete(0,END)
        name = entry.get()
        str(name)
        PanSou(name)
        ConentIntegrity()


    button = Button(root,text="搜索",command=callback)
    button.pack(side=TOP,anchor="nw")

    def Option_list(event):
        """设置鼠标双击事件
        获取用户双击鼠标时选择的内容
        然后用webbrowser模块来调用默认浏览器打开url
        """
        url = listboxUrl.get(listboxUrl.curselection()) #获取用户双击选择的内容
        webbrowser.open_new_tab(url)#调用默认浏览器打开url


    listboxName = Listbox(root,width=35)
    listboxName.pack(side=LEFT,anchor="nw",fill=BOTH)

    listboxUrl = Listbox(root,width=70)
    listboxUrl.bind('<Double-Button-1>',Option_list)#设置鼠标事件
    listboxUrl.pack(side=LEFT,anchor="nw",fill=BOTH)

    root.mainloop()

