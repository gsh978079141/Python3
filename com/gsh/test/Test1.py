'''
Created on 2017年11月14日

@author: gdd
'''
import  urllib.request
url='http://www.douban.com'
webpage=urllib.request.urlopen(url)
data=webpage.read()
data=data.decode('utf-8')
print(data)
