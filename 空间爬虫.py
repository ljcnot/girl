import os, sys, requests, uuid, time
import urllib.request
from bs4 import BeautifulSoup
import socket
socket.setdefaulttimeout(5.0)



targetDir =os.getcwd()
papap=targetDir+"\\"

def generateFileName(name):
    return str(uuid.uuid3(uuid.NAMESPACE_URL,name))
  
      
# 根据文件名创建文件
def createFileWithFileName(localPathParam,fileName):  
    totalPath=localPathParam+'\\'+fileName  
    if not os.path.exists(totalPath):  
        file=open(totalPath,'a+')  
        file.close()  
        return totalPath

url2 = "http://www.meizitu.com/a/sifang_5_1.html"
data=None
headers = {
    'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    }
false = False
def meiziImg(url):
    s = requests.get(url,data=data,headers=headers)
    bs = BeautifulSoup(s.text,"html.parser")
    girl=bs.find_all('div',class_="postContent")
    for child in girl:
        for j in child.find_all('img'):
            l = j.get('src')
            #print("慢点慢点")
            #time.sleep(1)
            fileName=generateFileName(l)+'.jpg'
            try:
                if os.path.exists(papap+fileName):
                    print("这个妹子已经扒过了")
                    continue
                else:
                    urllib.request.urlretrieve(l,createFileWithFileName(targetDir,fileName))
            except:
                print("此图下载失败")
                continue
            print(l)
    return false

def qzurl(url):
    s = requests.get(url,data=data,headers=headers)
    bs = BeautifulSoup(s.text,"html.parser")
    t="http://www.meizitu.com/a/sifang_5_1.html"
    g = bs.find_all('li', class_="wp-item")
    for child in g:
        for m in child.find_all(target="_blank"):
            l=m.get("href")
            if t!=l:
                print(l)
                j=meiziImg(l)
                t=l
                if j:
                    continue
    return false
def fanye(url):
    g = r"http://www.meizitu.com/a/"
    s = requests.get(url, data=data, headers=headers)
    gs = BeautifulSoup(s.text,"html.parser")
    i = gs.find_all(id = "wp_page_numbers")
    for c in i:
        for d in c.find_all("a"):
            b = d.get("href")
            u = g+b
            print("正在爬"+u)
            j = qzurl(u)
            if j:
               continue
    return false
def mulu(url):
    s= requests.get(url, data=data, headers=headers)
    gs= BeautifulSoup(s.text, "html.parser")
    i = gs.find_all("span")
    for c in i:
        for d in c.find_all("a"):
            b = d.get("href")
            print("正在爬%s"%b)
            j = fanye(b)
            if j:
                continue


mulu(url2)
#meiziImg("http://www.meizitu.com/a/5240.html")

#print(bs.prettify())
#print(bs.select('img[class="s-news-img"]'))
#for child in bs.descendants:
#    print(child.class_="s-news-img")




