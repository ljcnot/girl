# coding: utf-8

from collections import deque
from threading import Thread
import logging

url_list = deque()
download_list = deque()
running = False


class LoopThread(Thread):
    def __init__(self, target, args, **kwargs):
        self.running = False
        self.target = target
        self.args = args
        super(LoopThread, self).__init__(**kwargs)

    def run(self):
        self.running = True
        while self.running:
            self.target(*self.args)

    def stop(self):
        self.running = False


class ThreadPool(object):
    def __init__(self, pool):
        self.pool = pool

    def append(self, *args):
        for p in args:
            self.pool.append(p)

    def start(self):
        for p in self.pool:
            p.start()

    def stop(self):
        for p in self.pool:
            p.stop()

    def join(self):
        for p in self.pool:
            p.join()


def analyzer(url_list, down_list):
    try:
        url = url_list.popleft()
    except IndexError:
        pass
    else:
        # 页面分析
        logging.info('Analyse %s', url)
        img_url = url + '/bitch'
        page_id = url.split('/')[-1]
        if page_id == '':
            page_id = 1
        else:
            page_id = int(page_id)
        next_page = '/'.join(url.split('/')[:-1] + [str(page_id + 1)])
        down_list.append((img_url, 'shit'))
        url_list.append(next_page)


def downloader(down_list):
    try:
        url, title = down_list.popleft()
    except IndexError:
        pass
    else:
        # 下载
        logging.info('Download %s with title %s', url, title)


if __name__ == '__main__':
    ana_pool = ThreadPool([
        LoopThread(target=analyzer,
                   args=(url_list, download_list)) for _ in xrange(4)
    ])
    down_pool = ThreadPool([
        LoopThread(target=downloader,
                   args=(download_list, )) for _ in xrange(4)
    ])

    logging.basicConfig(level=logging.INFO)
    url_list.append('http://www.fuck.com/')
    ana_pool.start()
    down_pool.start()
    from time import sleep
    sleep(3)  # 其实可以在thread中去调用stop，这里只是举个例子所以就强行等三秒stop了
    ana_pool.stop()
    down_pool.stop()
    ana_pool.join()
    down_pool.join()
