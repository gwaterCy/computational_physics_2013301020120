# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 08:31:04 2016
#武大教务系统的爬虫程序
@author: yi cao
"""
import urllib2
import cookielib
from PIL import Image
import cStringIO
import urllib
import re
import getpass

class Spider:
    
    def __int__(self):
        self.LoginUrl ="http://210.42.121.134/servlet/Login"
        self.CaptchaUrl = "http://210.42.121.134/servlet/GenImg"
        self.CreditUrl = "http://210.42.121.134//servlet/Svlt_QueryStuScore?"
        self.username = raw_input('student ID : ')
        self.password = getpass.getpass('Password: ')
        self.cookie = cookielib.CookieJar()
        self.handler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.handler)
        # 将cookies绑定到一个opener cookie由cookielib自动管理
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            }
        self.credit_table={
            'none':'',
            'pr':'%B9%AB%B9%B2%B1%D8%D0%DE', #公必
            'pe':'%B9%AB%B9%B2%D1%A1%D0%DE', #公选
            'mr':'%D7%A8%D2%B5%B1%D8%D0%DE' ,#专必
            'me':'%D7%A8%D2%B5%D1%A1%D0%DE' ,#专选
            'last':'%C9%CF',
            'next':'%CF%C2'
        }
        # 根据抓包信息 构造headers
                           
    def login(self):
        captcha = self.show_captcha(self.CaptchaUrl)
        postData = {
            'id': self.username,
            'pwd': self.password,
            'xdvfb': captcha
            }
        data = urllib.urlencode(postData)   # 生成post数据 ?key1=value1&key2=value2的形式
        result = self.getPage(self.LoginUrl, data)
        pattern = re.compile(r'<font color="red" style="font-size: 12px;">')   #用于判断是否验证码出错
        if  re.search(pattern,result):
            print "验证码错误或密码错误!".decode('utf-8')
            self.login()
        else:
            print '登录成功！'.decode('utf-8')
    
    def getUrCource(self,year='0',term='none',_type='none',flag='0'):
        #usage:term = 'last','next'; _type = 'pr','pe','mr','me' flag = 0,1#为1时只显示有成绩的课程
        url = self.CreditUrl+'year='+year+'&term='+self.credit_table[term]+'&learnType='+self.credit_table[_type]+'&scoreFlag='+flag
        result = self.getPage(url,'')
        pattern = re.compile('<tr (null>|null class>|null class="alt">).*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>',re.S)
        #用于获取成绩信息[课头号，课名，类型，学分，教师，开课学院，备注，年份，学期，分数]
        if  not re.search(pattern,result):
            print "无该类型课程".decode('utf-8')
        else:
            item = re.findall(pattern,result)
            return item       #item 是一个list,其每一项又是一个包含单个课程信息的list
    
    def getUrCredit(self,cource_item):
        #usage : 将getUrCource 中得到的item填入参数列表即可，也可以将几项item合并
        gpa_all ,credit_all =0.0,0.0
        item = cource_item
        for i in item:
            if  not i[10].encode('utf-8') == '':    #避免有没有成绩的课程干扰计算
                gpa_all = self.gpaConvert(i[4].encode('utf-8'),i[10].encode('utf-8')) + gpa_all
                #print gpa_all
                credit_all = credit_all + float(i[4].encode('utf-8')) 
                #print credit_all
        return  '%.5f'% (gpa_all/credit_all)
            
    def gpaConvert(self,credit,score):
        gpa_table=[0.0,1.0,1.5,2.0,2.3,2.7,3.0,3.3,3.7,4.0]
        score_table =[range(0,60),range(60,64),range(64,68),range(68,72),range(72,75)
            ,range(75,78),range(78,82),range(82,85),range(85,90),range(90,101)]
        score = float(score)
        credit = float(credit)
        for i in range(10):
            if score in score_table[i]:
                return gpa_table[i]*credit
           
    def getPage(self,url,data):
        request = urllib2.Request(url, data, self.headers)    # 构造request请求
        try:
            response = self.opener.open(request)
            result = response.read().decode('gb2312')
            return result
        except urllib2.HTTPError, e:
            print e.code  
            
            
    def show_captcha(self,url):
        picture = self.opener.open(url).read()
        # 用openr访问验证码地址,获取cookie
        file = cStringIO.StringIO(picture)
        Image.open(file).show()   #使用open可以直接打开图片，不用到本地区查看
        captcha = raw_input("please input the captcha: ")
        return captcha
        
    

spider = Spider()
spider.__int__()
spider.login()
item =  spider.getUrCource(flag='1')
for i in item:
    print i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]
a = spider.getUrCredit(item)
print 'credit ：'+a
        
        
    
        