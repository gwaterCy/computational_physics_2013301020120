# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 16:13 2016
解决了抓取链接时会一并抓取其fork信息的问题！
@author: yi cao

程序设计思路：
1.从老师的主页开始，分别爬取follow，star，watch三个页面的所有同学的git主页链接
2.然后进入每个人的主页，爬取他们的软件池的链接，共计要打开280次页面。所以网速决定了爬取速度
3.由于耗时较长所以，避免中间网络不稳定中断了，需要重新爬取。所以要设计断点续爬。用文本文档存储断点信息，下次启动时直接载入
"""

import urllib
import re
import xlr_tools

url_table = ["https://github.com/caihao/followers"
    ,"https://github.com/caihao/followers?page=2"
    ,"https://github.com/caihao/computational_physics_whu/watchers"
    ,"https://github.com/caihao/computational_physics_whu/watchers?page=2"
    ,"https://github.com/caihao/computational_physics_whu/stargazers"
    ,"https://github.com/caihao/computational_physics_whu/stargazers?page=2"]

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getInf(html):
    reg = r'<img alt="@(.*?)" class="gravatar"'
    imgre = re.compile(reg)
    item = re.findall(imgre,html)
    for i in range(len(item)):
        item[i] =  'https://github.com/'+item[i]
    return item
    
def getRes(html,url):
    reg = r'<li class="public source.*?">\n.*?<a href="/.*(/c.*?)" class="'
    imgre = re.compile(reg)
    if re.search(imgre,html):
        item = re.findall(imgre,html)
        return url+item[0]
    else:
        print '\n'+url+'      have no repositeries'
        text2.write(url+'      have no repositeries\n')
        return 'no'
        
def convertUrl(url):
    pattern = re.compile(r'https.*?.com/(.*?)/.*?(201.*)')
    if re.search(pattern,url):
        item = re.findall(pattern,url)
        inf = '>-'+item[0][1]+'[*github*:'+item[0][0]+']'
        content = inf +'\n('+git_url+')\n'
        return content
    else:
        return 'no'
        
def saveInterrupt():
        text1=open('restart.txt','w')
        text1.write(str(page_out)+'\n')
        text1.write(str(url_out))
        text1.close()
        text.close()
        text2.close()
        print '在第'+str(page_out+1)+'页第'+str(url_out+1)+'个链接处中断'
    
if __name__ == '__main__':
    ############初始化##############
    text = open('roster.txt','a')
    text1=open('restart.txt','a')
    text2 = open('debug.txt','a')
    #打开并创建三个文件，用于记录所爬取数据。roster/存储结果，debug/存储错误信息
    #restart/用于记录上次爬取断点，进而续传
    NUM = 0
    ERROR_NUM = 0
    #初始化NUM和ERROR_NUM
    text1=open('restart.txt','r')
    #打开restart 进行断点续传
    a = text1.readline()#读restart的第一行，取出当前页码
    if a == '':
        a='0'
    PAGE_IN = int(a)
    
    a = text1.readline()#读取第二行，取出当前页面的第a个链接
    if a == '':
        a='0'
    URL_IN = int(a)
    text1.close()    
    ################################
    print "开工咯，开始爬取大家的git链接！！！！！！"+'上次结束页码:'+str(PAGE_IN+1)+';第'+str(URL_IN+1)+'个'
    print '每个我看着喜欢的链接，我就会用 # 标记^_^'
    for page in range(len(url_table)-PAGE_IN):#总长度减去已经爬取的就是剩下要爬的
        page_out = page+PAGE_IN #用于存储当前爬取的页码   
        try:
            html = getHtml(url_table[page+PAGE_IN])
            url = getInf(html)
        except:
            saveInterrupt()
            exit()
        #print url
        for i in range(len(url)-URL_IN):
            url_out = i + URL_IN
            try:
                html = getHtml(url[i+URL_IN])#获取个人的repositories页面
                git_url = getRes(html,url[i+URL_IN])
            except:
                saveInterrupt()
                exit()
            if  git_url == 'no': 
                ERROR_NUM = ERROR_NUM + 1
            else:
                #print git_url
                content = convertUrl(str(git_url))
                #print inf
                if not content == 'no':                            
                    text.write(content)
                    NUM = NUM+1
                    print '#',
                else:
                    text2.write('\n No StudentID\n'+git_url)
                    print '\n No StudentID\n'+git_url
                    ERROR_NUM = ERROR_NUM+1
                    
                if NUM %10==0:
                    print '\n已经抓取了'+str(NUM)+'个git的链接啦！逝者如吾乎，不舍昼夜'
                elif NUM %35 ==0:
                    print '\n如果你网速快点的话，我不就不会这么累了'
                #break            
        URL_IN = 0
        url_out = 0
    print '\n总共有'+str(NUM)+'个git链接'
    print '\n其外还有'+str(ERROR_NUM)+'个同学没有建软件池，或者他的软件池名字太难看！哼！'
    text.close()
    text2.close()
#解决断点续传！！！！！(解决)用文本存下上次结束的时的信息，再启动时重载
#解决爬虫效率问题！！！！
#解决重复爬取的问题！！！策略：(采用唯一名单表筛选信息即可)
#优化代码结构！！！（final）
#优化交互模式与体验！！！（基本解决）
#解决fork的问题(解决)再解决stared
#匹配tools操作方式
    
    
