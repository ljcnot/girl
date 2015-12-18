# -*- coding: utf-8 -*-
import os
from win32com.client import Dispatch
import win32com.client
import win32com



xlApp = None
def get_data(path):
    #获取excel数据源

    filePath = os.getcwd()+"\\"+path+".xls" #input(u"请将excel的文件路径粘贴进来")
    is_valid = False
    try:
        if os.path.isfile(filePath):
            filename = os.path.basename(filePath)
            if filename.split('.')[1] == 'xls':
                is_valid = True
        data = None
        if is_valid:
            xlApp = win32com.client.Dispatch('Excel.Application')
            data = xlApp.Workbooks.Open(filePath)
    except Exception as e:
        print("错误%s"%e)
        return None
    return data

def formTime(gTime): #切割初始时间跟结束时间
    timeList = gTime.split('-')
    fTime=time(timeList[0], timeList[1])
    return fTime

def breakTime(fTime):#分割小时，分钟
    kTime= fTime.split(":")
    mTime=timeHours(int(kTime[0]),int(kTime[1]))
    return mTime

def countTime(kTime,oTime): #计算工时
    if oTime.hours < kTime.hours:
        oTime.hours += 24
    workHours = oTime.hours - kTime.hours
    workMinutes = int(((workHours*60)+oTime.minutes-kTime.minutes)/60)
    yMinutes = ((workHours*60)+oTime.minutes-kTime.minutes)%60
    if yMinutes >= 30:
        workTime = float(workMinutes)+0.5
    else:
        workTime = int(workMinutes)
    return workTime

class timeHours(object):
    def __init__(self, hours, minutes):
        self.hours = hours
        self.minutes = minutes

class time(object):
    def __init__(self, starTime, overTime):
        self.starTime = starTime
        self.overTime = overTime

def read_excel(data):
    sheet2 = list(range(1,data.Worksheets.Count))
    for x in sheet2:
        print("%s号副表为：%s"%(x,data.Sheets(x).Name))
    sheet = input("请输入需要计算工时的副表名：\n")
    xValue = data.Worksheets(sheet)
    cNum = 7
    gNum = 6
    rNum = 3

    #mValue =  xValue.Cells(2,7).Value
    MaxRow = xValue.UsedRange.Rows.Count
    num = list(range(rNum,MaxRow+1))
    for c in num:
        uValue = xValue.Cells(c, cNum).Value
        pValue = formTime(uValue)
        myValue = countTime(breakTime(pValue.starTime), breakTime(pValue.overTime))
        xValue.Cells(c, gNum).Value = myValue
        print("正在修改第%d行工时为%d"%(c,myValue))
    data.Close(SaveChanges=1)
    return True



    # for num in list(range(2,len(cols))):
    #    print (cols[num])


# gTime = "17:30-21:00"
# l=formTime(gTime)
# k = countTime(breakTime(l.starTime),breakTime(l.overTime))
# print (k)
j = input("输入excel名称：\n")
l = get_data(j)
m= read_excel(l)
if m:
    print("操作完成")

