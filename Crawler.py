import requests
from bs4 import BeautifulSoup
from urllib import parse
from urllib.robotparser import RobotFileParser

import re
import os, sys
import time
import random

from Page import Page
from FrequencyCounter import FrequencyCounter

class Crawler():
    def __init__(self, url) -> None:
        self.url = url

        self.pages = []
        self.visited_inQueue = {
            self.url
        }
        self.headers = {
            "Accept-Encoding":
            "identity",
            "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
        }

        # frontier queue
        self.linksQueue = []
        # links going out of the test data
        self.goingOutLinks = []
        
        self.brokenLinks = []
        self.nontextLinks = []
        self.duplicateLinks = []

        # contain already seen content
        self.contentSet = set()
        
        self.robotNotAllow = None
        # if use robotparser
        self.rp = RobotFileParser()

        self.frequncyCounter = FrequencyCounter()
        pass

    # Crawl the data of this link
    def getLinks(self, url):

        try:
            page = requests.get(url, headers=self.headers)
        # erroes in the Web page. Skip
        except:
            return
        if page.status_code == 404:
            self.brokenLinks.append(url)
            return
        
        result = page.content
        header = page.headers
        soup = BeautifulSoup(result, "lxml", from_encoding='utf-8')

        # get title
        title = soup.find('title').string if soup.find('title') else None
        try:
            contentLength = header['Content-Length']
        except:
            contentLength = len(page.text)

        # get date
        try:
            date = header['Last-Modified']
        except:
            date = None

        # check wheather need to index this page
        is_index = False if soup.find_all('meta', content='noindex') else True

        # get content and check duplication => index or not
        page.encoding = 'utf-8'
        data = self.filter_tags(soup.find('body').text).strip()
        dataStriped = data.strip().replace('\n', '').replace('\r', '').replace(
            ' ', '').replace('\t', '')

        if dataStriped in self.contentSet:
            is_index = False
            self.duplicateLinks.append(url)

        else:
            self.contentSet.add(dataStriped)


        self.addPage(url, date, title, contentLength, is_index, data)

        # Crawl links in this page
        newLinks = soup.find_all('a')
        self.getNewLinks(newLinks,url)
        return

    # Check all crawled new links and put them in the corresponding queue or list
    def getNewLinks(self, newLinks,baseurl):
        if len(newLinks) != 0:
            for link in newLinks:
                newurl = link['href']

                # links going out of the test data
                if newurl.startswith('http') or newurl.startswith('mailto'):
                    if newurl not in self.goingOutLinks:
                        self.goingOutLinks.append(newurl)
                # links can be added
                else:
                    newurl = parse.urljoin(baseurl,newurl)
                    # check whether is text file
                    if newurl.endswith('.txt') or newurl.endswith(
                            '.html') or newurl.endswith(
                                '.htm') or newurl.endswith('.php'):
                        # check if visited or already in frontier queue
                        if newurl not in self.visited_inQueue:
                            self.visited_inQueue.add(newurl)
                            self.linksQueue.append(newurl)
                    else:
                        if newurl not in self.nontextLinks:
                            self.nontextLinks.append(newurl)

    # Remove HTML Tags
    def filter_tags(self, htmlstr):
        # filter CDATA
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>',
                              re.I)  # matching CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',
                               re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',
                              re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # line feed
        re_h = re.compile('</?\w+[^>]*>')  # HTML Tag
        re_comment = re.compile('<!--[^>]*-->')  # HTML Comments
        s = re_cdata.sub('', htmlstr)  # remove CDATA
        s = re_script.sub('', s)  # remove SCRIPT
        s = re_style.sub('', s)  # remove style
        s = re_br.sub('\n', s)  # br -> \m
        s = re_h.sub('', s)  # remove HTML Tag
        s = re_comment.sub('', s)  # remove HTML Comments
        # remove line feed
        blank_line = re.compile('\n+')
        s = blank_line.sub('\n', s)
        s = self.replaceCharEntity(s)  # replace entity
        return s

    # Remove escapes
    def replaceCharEntity(self, htmlstr):
        CHAR_ENTITIES = {
            'nbsp': ' ',
            '160': ' ',
            'lt': '<',
            '60': '<',
            'gt': '>',
            '62': '>',
            'amp': '&',
            '38': '&',
            'quot': '"',
            '34': '"',
        }

        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            entity = sz.group()  # origional entity
            key = sz.group('name')  # remove escapes
            try:
                htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
            except KeyError:
                # Replace with empty string
                htmlstr = re_charEntity.sub('', htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
        return htmlstr

    # Create new Page object and add into list
    def addPage(self, url, date, title, content_len, is_index, data):
        self.pages.append(Page(url, date, title, content_len,data, is_index))

    # Output result to file after crawling
    def output(self):
        
        # Output all information about crawled pages
        Page.outputPages(self.pages)

        # find relative path
        mod_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        full_path = os.path.join(mod_path,'./Data','otherLists.txt')

        # Output other lists of links
        fo = open(full_path, 'w')

        fo.write("Goint out links:\n")
        for link in self.goingOutLinks:
            fo.write(link + '\n')

        fo.write("\rNon-text files links:\n")
        for link in self.nontextLinks:
            fo.write(link + '\n')

        fo.write("\rBroken links:\n")
        for link in self.brokenLinks:
            fo.write(link + '\n')

        fo.write("\rDuplicated links:\n")
        for link in self.duplicateLinks:
            fo.write(link + '\n')

        fo.close()

    # if use robotparser
    def setRobot(self, url):
        newurl = url + 'robots.txt'
        self.rp.set_url(newurl)
        self.rp.read()
        return

    # Main while loop of crawler
    def spider(self,N):
        # start with 1 beacuse we crawl the first page out of the for loop
        i = 1

        # read robots.txt
        self.setRobot(self.url)

        self.getLinks(self.url)
        while i < N and len(self.linksQueue) > 0:
            link = self.linksQueue.pop(0)
            i += 1
            # check robots.txt (use robotparser)
            userAgent = '*'
            if not self.rp.can_fetch(userAgent, link):
                continue

            time.sleep(random.random()*3)
            self.getLinks(link)

        # count term and frequency
        self.frequncyCounter.setPages(self.pages)
        self.frequncyCounter.tokenize()

        self.output()
        return self.pages
    