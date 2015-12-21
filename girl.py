import os, sys, requests, uuid, time
import urllib.request
from bs4 import BeautifulSoup
import socket
import threading
socket.setdefaulttimeout(5.0)
p_jclock = threading.Condition() #进程锁调用
p_newPath = [] #最新解析的url链接表
p_stanPath = [] #等待爬取的url链接表
p_existPath = [] #已经爬取过的url链接表
p_errorPath = [] #下载失败的url链接表
p_downNum = 0 #已经下载过的连接数
p_threadNum = 10


def headers(url):
    headers2 = {"Host": "www.mzitu.com","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Accept": "image/png,image/*;q=0.8,*/*;q=0.5","Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3","Accept-Encoding": "gzip, deflate","Referer":url,"Cookie": "BAIDUID=E7640F5E0492BC620C23C0A8B7012A1C:FG=1; HMACCOUNT=5DA7BAB08C224046; BIDUPSID=E7640F5E0492BC620C23C0A8B7012A1C; PSTM=1450504738; H_PS_PSSID=17747_1420_18240_12824_18501_17001_17073_15742_12089","Connection": "keep-alive"}
    return headers2
class SuperUrl:
    def __init__(self,url):
        self.url = url
        self.headers = headers(url)
        self.img_threadpool = [] #图片进程池
        self.url_threadpool = [] #url爬取进程池
        self.url_ThreadNum = 5

    def urlscan(self):
        global p_stanPath
        global p_allPath
        p_stanPath.append(self.url)
        while (len(p_stanPath)!=0):
            j =0
            while j<self.url_ThreadNum and j < len(p_stanPath):
                urlobj = requests.get(p_stanPath[j],data=None,headers=headers(p_stanPath[j]))
                html = BeautifulSoup(urlobj.text, "html.parser")
                ListUrl = html.find_all("a")
                for my_ListUrl in ListUrl:
                    new_url = my_ListUrl.get("href")
                    pd_url = new_url[:7]
                    if pd_url =="http://":
                        p_newPath.append(new_url)
                urlThread = DownAllImg()
                self.url_threadpool.append(urlThread)
                urlThread.start()
                p_existPath.append(p_stanPath[j])
                j+=1

            for urlThread2 in self.url_threadpool:
                urlThread2.join(30)
            self.url_threadpool = []
            self.getUrl()

    def getUrl(self):
            global p_newPath
            global p_stanPath
            global p_existPath
            p_stanPath = list(set(p_newPath)-set(p_existPath))
            p_newPath = []

class DownAllImg(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.p_threadpool = []
        self.p_imgPath = []#待爬取的img链表
    def run(self):
        global p_stanPath
        try:
            for Path in p_stanPath:
                imgobj = requests.get(Path,data=None, headers=headers(Path))
                html = BeautifulSoup(imgobj.text, "html.parser")
                girlImg = html.find_all('div', calss_="main-image")
                if girlImg ==[]:
                    break
                else:
                    for imgUrl in girlImg.find_all('img'):
                        url = imgUrl.get('src')
                        p_imgPath.append(url)
                        print(url)
                    if len(p_imgPath)!= 0:
                        title = html.find('title').text
                        for down in self.p_imgPath:
                            threadpool = DownThread(down, title)
                            self.p_threadpool.append(threadpool)
                            threadpool.start()
                        for thread in self.p_threadpool:
                            thread.join(30)
                        p_imgPath = []

        except Exception as e:
            print(e)


class DownThread(threading.Thread):
    def __init__(self,url,title):
        threading.Thread.__init__(self)
        self.url=url
        self.title=title
        self.nowFile = os.getcwd()
    def imgFileName(self):
        folderFile = self.nowFile+"\\"+self.title
        os.mkdir(folderFile)
        fileName = generateFileName(url)+'.jpg'
        totalPath = folderFile+"\\"+fileName
        return totalPath
    def run(self):
        try:

            urllib.request.urlretrieve(l,self.imgFileName())
        except Exception as e:
            print(e)

if __name__ == "__main__":
    url = r"http://www.mzitu.com/52562"#input("输入目标网址:\n")
    imgload = SuperUrl(url)
    imgload.urlscan()

#
#     s= requests.get(url, data=data, headers=headers_value())
#     gs= BeautifulSoup(s.text, "html.parser")
#     i = gs.find_all("span")
#     for c in i:
#         for d in c.find_all("a"):
#             b = d.get("href")
#             print("正在爬%s"%b)
#             j = fanye(b)
#             if j:
#                 continue
#
# class downImg:
#     def __init__(self):
#         self.now
#
#
#
#
# def generateFileName(name):
#     return str(uuid.uuid3(uuid.NAMESPACE_URL,name))
#
#
# # 根据文件名创建文件
# def createFileWithFileName(localPathParam,fileName):
#     totalPath=localPathParam+'\\'+fileName
#     if not os.path.exists(totalPath):
#         file=open(totalPath,'a+')
#         file.close()
#         return totalPath
#
# def meiziImg(url):
#     s = requests.get(url,data=data,headers=headers_value())
#     bs = BeautifulSoup(s.text,"html.parser")
#     girl=bs.find_all('div',class_="postContent")
#     for child in girl:
#         for j in child.find_all('img'):
#             l = j.get('src')
#             #print("慢点慢点")
#             #time.sleep(1)
#             fileName=generateFileName(l)+'.jpg'
#             try:
#                 if os.path.exists(papap+fileName):
#                     print("这个妹子已经扒过了")
#                     continue
#                 else:
#                     urllib.request.urlretrieve(l,createFileWithFileName(targetDir,fileName))
#             except:
#                 print("此图下载失败")
#                 continue
#             print(l)
#     return false
#
# def qzurl(url):
#     s = requests.get(url,data=data,headers=headers_value())
#     bs = BeautifulSoup(s.text,"html.parser")
#     t="http://www.meizitu.com/a/sifang_5_1.html"
#     g = bs.find_all('li', class_="wp-item")
#     for child in g:
#         for m in child.find_all(target="_blank"):
#             l=m.get("href")
#             if t!=l:
#                 print(l)
#                 j= threading.Thread(target = meiziImg, args=l)
#                 j.setDaemon(True)
#                 j.start()
#                 p_threadpool.append(j)
#                 t=l
#     for i in p_threadpool:
#         i.join(30)
#
#
#     return false
# myReferer = ""
# def headers_value():
# <<<<<<< HEAD
#     global myReferer
#     headers = {"Host": "www.meizitu.com","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Accept": "image/png,image/*;q=0.8,*/*;q=0.5","Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3","Accept-Encoding": "gzip, deflate","Referer":myReferer,"Cookie": "BAIDUID=E7640F5E0492BC620C23C0A8B7012A1C:FG=1; HMACCOUNT=5DA7BAB08C224046; BIDUPSID=E7640F5E0492BC620C23C0A8B7012A1C; PSTM=1450504738; H_PS_PSSID=17747_1420_18240_12824_18501_17001_17073_15742_12089","Connection": "keep-alive"}
# =======
#     headers = {"Host": "www.meizitu.com","User-Agent":"Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"
# ,"Accept": "image/png,image/*;q=0.8,*/*;q=0.5","Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3","Accept-Encoding": "gzip, deflate","Referer":myReferer,"Cookie": "BAIDUID=E7640F5E0492BC620C23C0A8B7012A1C:FG=1; HMACCOUNT=5DA7BAB08C224046; BIDUPSID=E7640F5E0492BC620C23C0A8B7012A1C; PSTM=1450504738; H_PS_PSSID=17747_1420_18240_12824_18501_17001_17073_15742_12089","Connection": "keep-alive"}
# >>>>>>> origin/master
#     return headers
# def fanye(url):
#     g = r"http://www.meizitu.com/a/"
#     global myReferer
#     myReferer= url
#     s = requests.get(url, data=data, headers=headers_value())
#     gs = BeautifulSoup(s.text,"html.parser")
#     i = gs.find_all(id = "wp_page_numbers")
#     for c in i:
#         for d in c.find_all("a"):
#             b = d.get("href")
#             u = g+b
#             print("正在爬"+u)
#             j = qzurl(u)
#             if j:
#                continue
#             p_threadpool = []
#     return false
#
#
# def mulu(url):
#     global myReferer
#     myReferer = url
#     s= requests.get(url, data=data, headers=headers_value())
#     gs= BeautifulSoup(s.text, "html.parser")
#     i = gs.find_all("span")
#     for c in i:
#         for d in c.find_all("a"):
#             b = d.get("href")
#             print("正在爬%s"%b)
#             j = fanye(b)
#             if j:
#                 continue
#
# targetDir =os.getcwd()
# papap=targetDir+"\\"
#
#
# url2 = "http://www.meizitu.com/a/sifang_5_1.html"
# data=None
#
#
#
# false = False
# try:
#
#     mulu(url2)
# except:
#     print ("Unexpected error:", sys.exc_info()) # sys.exc_info()返回出错信息
#     input('press enter key to exit') #这儿放一个等待输入是为了不让程序退出
#


