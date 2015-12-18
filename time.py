# -*- coding: utf-8 -*-
import os
import string
import xlrd


def get_data():
    #获取excel数据源
    filePath = input(u"请将excel的文件路径粘贴进来")
    is_valid = False
    try:
        if os.path.isfile(filePath):
            filename = os.path.basename(filePath)
            if filename.split('.')[1] == 'xls':
                is_valid = True
        data = None
        if is_valid:
            data = xlrd.open_workbook(filePath)
    except Exception as e:
        print("错误%s"%e)
        return None
    return data
gTime = "17:30-20:30"
def formTime(gTime): #切割初始时间跟结束时间
    timeList = gTime.split('-')
    fTime=time(timeList[0], timeList[1])
    return fTime

class time(object):
    def __init__(self,starTime,overTime):
        self.starTime = starTime
        self.overTime = overTime

l=formTime(gTime)


