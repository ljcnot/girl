#!/usr/bin/env python
#coding=utf-8
import threading
import urllib
import re
import time

g_mutex=threading.Condition()
g_pages=[]  #从中解析所有url链接
g_queueURL=[]  #等待爬取的url链接列表
g_existURL=[]  #已经爬取过的url链接列表
g_failedURL=[] #下载失败的url链接列表
g_totalcount=0 #下载过的页面数

class Crawler:
    def __init__(self,crawlername,url,threadnum):
        self.crawlername=crawlername
        self.url=url
        self.threadnum=threadnum
        self.threadpool=[]
        self.logfile=file("log.txt",'w')
    def craw(self):
        global g_queueURL
        g_queueURL.append(url)
        depth=0
        print self.crawlername+" 启动..."
        while(len(g_queueURL)!=0):
            depth+=1
            print 'Searching depth ',depth,'...\n\n'
            self.logfile.write("URL:"+g_queueURL[0]+"........")
            self.downloadAll()
            self.updateQueueURL()
            content='\n>>>Depth '+str(depth)+':\n'
            self.logfile.write(content)
            i=0
            while i<len(g_queueURL):
                content=str(g_totalcount+i)+'->'+g_queueURL[i]+'\n'
                self.logfile.write(content)
                i+=1
    def downloadAll(self):
        global g_queueURL
        global g_totalcount
        i=0
        while i<len(g_queueURL):
            j=0
            while j<self.threadnum and i+j < len(g_queueURL):
                g_totalcount+=1
                threadresult=self.download(g_queueURL[i+j],str(g_totalcount)+'.html',j)
                if threadresult!=None:
                    print 'Thread started:',i+j,'--File number =',g_totalcount
                j+=1
            i+=j
            for thread in self.threadpool:
                thread.join(30)
            threadpool=[]
        g_queueURL=[]
    def download(self,url,filename,tid):
        crawthread=CrawlerThread(url,filename,tid)
        self.threadpool.append(crawthread)
        crawthread.start()
    def updateQueueURL(self):
        global g_queueURL
        global g_existURL
        newUrlList=[]
        for content in g_pages:
            newUrlList+=self.getUrl(content)
            g_queueURL=list(set(newUrlList)-set(g_existURL))
    def getUrl(self,content):
        reg=r'"(http://.+?)"'
        regob=re.compile(reg,re.DOTALL)
        urllist=regob.findall(content)
        return urllist

class CrawlerThread(threading.Thread):
    def __init__(self,url,filename,tid):
        threading.Thread.__init__(self)
        self.url=url
        self.filename=filename
        self.tid=tid
    def run(self):
        global g_mutex
        global g_failedURL
        global g_queueURL
        try:
            page=urllib.urlopen(self.url)
            html=page.read()
            fout=file(self.filename,'w')
            fout.write(html)
            fout.close()
        except Exception,e:
            g_mutex.acquire()
            g_existURL.append(self.url)
            g_failedURL.append(self.url)
            g_mutex.release()
            print 'Failed downloading and saving',self.url
            print e
            return None
        g_mutex.acquire()
        g_pages.append(html)
        g_existURL.append(self.url)
        g_mutex.release()


if __name__=="__main__":
    url=raw_input("请输入url入口:\n")
    threadnum=int(raw_input("设置线程数:"))
    crawlername="小小爬虫"
    crawler=Crawler(crawlername,url,threadnum)
    crawler.craw()