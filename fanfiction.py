__author__ = 'CQC'
# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import tool
import os
from bs4 import BeautifulSoup
class Fanfiction:
    def __init__(self):
        self.baseurl = "http://www.fanfiction.net"
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : self.user_agent }
        self.topicurl = None
        self.nameurl = None
        self.maindir = os.getenv('HOME') + os.sep + 'fanfiction'
        self.topicdir = None
        self.namedir = None
        self.pageNumber = None
     	self.tool = tool.Tool()
    def getPage(self, url):
        request = urllib2.Request(url, headers = self.headers)
        response = urllib2.urlopen(request)
        return response.read().decode('utf-8')
    def selectTopic(self):
        page = self.getPage(self.baseurl)
        pattern = re.compile('<table.*?gui_table1i(.*?)</table>', re.S)
#       pattern = re.compile(r'<table.*?id="gui_table1i".*?<tbody>(.*?)</tbody>', re.S)
        items = re.findall(pattern, page)
        print items
        pattern =re.compile("<a.*?href='(.*?)'>(.*?)</a>", re.S)
        topics = re.findall(pattern, items[0])
        print topics
        menu = dict()
        print 'Please select one of the following topics:'
        for topic in topics:
            menu[topic[1]] = topic[0]
            print topic[1]
        topic = raw_input('> ')
        self.topicdir = self.maindir + os.sep + topic.replace('/', '-')
        if not os.path.exists(self.topicdir):
            os.makedirs(self.topicdir)
        self.topicurl = self.baseurl + menu[topic]
        page = self.getPage(self.topicurl)
        pattern = re.compile('<div><a.*?href="(.*?)".*?title="(.*?)"', re.S)
        names = re.findall(pattern, page)
        menu = dict()
        print 'Please select one of the following name:'
        for name in names:
            menu[name[1]] = name[0]
            print name[1]
        name = raw_input('> ')
        self.namedir = self.topicdir + os.sep + name.replace(' ', '-')
        if not os.path.exists(self.namedir):
            os.makedirs(self.namedir)
        self.nameurl = self.baseurl + menu[name]
    def getPageNumber(self):
        page = self.getPage(self.nameurl)
        pattern = re.compile("<center.*?Page.*?\.\..*?&p=(.*?)'>Last", re.S)
        items = re.findall(pattern, page)
        self.pageNumber = int(items[0])
    def main(self):
        if not os.path.exists(self.maindir):
            os.makedirs(self.maindir)
        self.selectTopic()
        self.getPageNumber()
        namedir_unicode = (self.namedir + os.sep).decode('ascii')
        #for num in range(1, self.pageNumber + 1):
        for num in range(70, self.pageNumber + 1):
            print 'Page Number is %d' % num
            page = self.getPage(self.nameurl + '?&srt=1&r=103&p=' + str(num))
            pattern = re.compile("<div class='z-list.*?'.*?>" + '<a.*?href="(.*?)">' +
            "<img.*?>(.*?)</a>", re.S)
            threads = re.findall(pattern, page)
            #pattern = re.compile("<div.*?class='z-padtop2 xgray.*?>(.*?)<span", re.S)
            pattern = re.compile("<div.*?class='z-padtop2 xgray.*?>.*?Chapter.*?(\d+).*?<span", re.S)

            chapterNumbers = re.findall(pattern, page)
            for thread, chapterNumber in zip(threads, chapterNumbers):
                token = thread[0].split('/')
                filename = open(namedir_unicode + token[4], 'w')
                try:
                    for chapter in range(1, int(chapterNumber) + 1):
                        filename.write((u"\n\nChapter %s\n" % unicode(chapter)).encode('utf-8'))
                        threadurl = self.baseurl.decode('ascii') + u'/s/' +     token[2] + u'/' + unicode(chapter) + u'/' + token[4]
                        print threadurl
                        page = self.getPage(threadurl)
                        pattern = re.compile('<p>(.*?)</p>', re.S)
                        paragraphs = re.findall(pattern, page)
                        for paragraph in paragraphs:
                            content = self.tool.replace(paragraph)
                            filename.write((content + u'\n').encode('utf-8'))
                except urllib2.HTTPError:
                    log.write((threadurl + u'\t' + u'Chapter ' + chapterNumber).encode('utf-8'))			
                except urllib2.URLError:
                    log.write((threadurl + u'\t' + u'Chapter ' + chapterNumber).encode('utf-8'))			
		except:
                    log.write((threadurl + u'\t' + u'Chapter ' + chapterNumber).encode('utf-8'))			
                finally:
		    filename.close()
fanfiction = Fanfiction()
log = open(os.getenv('HOME') + os.sep + 'log', 'a')
fanfiction.main()
log.close()
                   
