# -*- coding: utf-8 -*-
import os
import xlwt
import xlrd
from openpyxl import workbook,load_workbook

import copy

def get_data(path):
    #获取excel数据源
    filePath = path #input(u"请将excel的文件路径粘贴进来")
    is_valid = False
    try:
        if os.path.isfile(filePath):
            filename = os.path.basename(filePath)
            if filename.split('.')[1] == 'xls':
                is_valid = True
        data = None
        if is_valid:
            data = load_workbook(filename = filePath)
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
    r =  data.get_sheet_names()
    for s in r:
        print (s)

    sname = input("输入想要的更改的表")
    sheet2 = data[sname]
    print(sheet2['D18'].value)


    # for num in list(range(2,len(cols))):
    #    print (cols[num])


# gTime = "17:30-21:00"
# l=formTime(gTime)
# k = countTime(breakTime(l.starTime),breakTime(l.overTime))
# print (k)
l =get_data("E:\games\库备份\文档\全保科加点申报.xls")
m= read_excel(l)

