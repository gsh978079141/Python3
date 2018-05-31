'''
Created on 2017年11月14日

@author: gdd
'''
from urllib import request  
from  bs4 import BeautifulSoup  
import re  
import time  
  
url = "https://www.zhihu.com/question/22918070" 
#url="http://china.nba.com/" 
html = request.urlopen(url).read().decode('utf-8', 'ignore')
soup = BeautifulSoup(html,'html.parser')  
#print(soup.prettify())  
  
#用Beautiful Soup结合正则表达式来提取包含所有图片链接（img标签中，class=**，以.jpg结尾的链接）的语句  
#links = soup.find_all('img') 
links = soup.find_all('img', "origin_image zh-lightbox-thumb",src=re.compile(r'.jpg$')) 
#print(links)  
# 设置保存图片的路径，否则会保存到程序当前路径  
path = r'/Volumes/GSH/Python/test/images/'                            #路径前的r是保持字符串原始值的意思，就是说不对其中的符号进行转义  
for link in links:  
    #print(link.attrs['src'])  
    #if(link.attrs['src'].startswith('http://')):
        #src=link.compile('.jpg$')
        #保存链接并命名，time.time()返回当前时间戳防止命名冲突  
        request.urlretrieve(link.attrs['src'],path+'\%s.jpg' % time.time())  #使用request.urlretrieve直接将所有远程链接数据下载到本地
        print("图片下载成功")
    #else:
        #print("链接有误")  