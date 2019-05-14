# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 21:25:45 2019
@author: Administrator
"""

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import random
import weather
import baidu_ai
import threading

# 标题
title = ""
# 内容
content = ""


# 爬取每页的超链接
def getHTMLText(url, headers):
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # print(r.text)
        return r.text
    except:
        return "爬取失败"


# 获取页面url
def parsehtml(namelist, urllist, html):
    url = 'http://www.tom61.com'
    soup = BeautifulSoup(html, 'html.parser')
    t = soup.find('dl', attrs={'class': 'txt_box'})
    # print(t)
    i = t.find_all('a')
    # print(i)
    for link in i:
        href = link.get('href')
        if url in href:
            urllist.append(link.get('href'))
        else:
            urllist.append(url + link.get('href'))
        # namelist.append(link.get('title'))


# 解析故事页面标签获取故事内容
def parsehtml2(html):
    global title
    text = []
    soup = BeautifulSoup(html, 'html.parser')
    # 正文
    t = soup.find('div', class_='t_news_txt')
    # 标题
    t2 = soup.find('div', class_='t_news')
    for i in t2.findAll('h1'):
        title = i.text
    for i in t.findAll('p'):
        text.append(i.text)
    return "\n".join(text)


# 解析页面 获取故事分类与url键值对
def parseHtmlGetClassify(html):
    storyClassify = {}
    soup = BeautifulSoup(html, 'html.parser')
    # 故事分类
    t = soup.find('ul', class_='t_dh_tab')
    for i in t.findAll('a'):
        storyClassify[i.text] = i['href']
    return storyClassify


# 发送邮件
def sendEmail(url, headers):
    msg_from = '978079141@qq.com'  # 发送方邮箱
    passwd = 'yydmmxoxizuabdbb'  # 填入发送方邮箱的授权码
    receivers = ['978079141@qq.com,978079141@qq.com']  # 收件人邮箱

    subject = '今日份的睡前小故事'  # 主题
    html = getHTMLText(url, headers)
    content = parsehtml2(html)  # 正文

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = ','.join(receivers)
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
        s.login(msg_from, passwd)
        print(msg.as_string())
        s.sendmail(msg_from, msg['To'].split(','), msg.as_string())
        print("发送成功")
    except:
        print("发送失败")
    finally:
        s.quit()


# 获取故事与标题
def getStory(url, headers):
    subject = '王二狗的睡前小故事'  # 主题
    html = getHTMLText(url, headers)
    content = parsehtml2(html)  # 正文
    # msg = MIMEText(content)
    return content


# 原主函数
def main_story():
    headers = {
        # 请求头
        'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    }
    urllist = []
    namelist = []
    BROADCAST_MP3 = "story.mp3"
    for i in range(1, 11):
        if i == 1:
            url = 'http://www.tom61.com/ertongwenxue/tonghuagushi/index.html'
        else:
            url = 'http://www.tom61.com/ertongwenxue/tonghuagushi/index_' + str(i) + '.html'
        # print("正在爬取第%s页的故事链接：" % (i))
        # print(url + '\n')
        html = getHTMLText(url, headers)
        parsehtml(namelist, urllist, html)
    # print("爬取链接完成")
    '''
    for i in urllist:
        html=getHTMLText(i,headers)
        parsehtml2(html)
    '''
    # sendemail(random.choice(urllist), headers)
    content = getStory(random.choice(urllist), headers)
    print(title + '\n' + content)
    # 百度 文字合成语音
    baidu_ai.text_to_audio(content, BROADCAST_MP3)
    # 百度 播放语音
    baidu_ai.voice_broadcast(BROADCAST_MP3)


# 修改后主函数
def test_main_story():
    headers = {
        # 请求头
        'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    }
    # 故事网址url
    base_story_url = "http://www.tom61.com/ertongwenxue/"
    # 随机 当前故事分类下第几页
    page = random.randint(1, 5)
    # url前缀
    prefix = "http:"
    if page == 1:
        suffix = '/index.html'
    else:
        suffix = '/index_%s.html' % page

    fen_lei_html = getHTMLText(base_story_url, headers)
    # 故事分类dirct（'故事类别',"url"）
    story_url_dict = parseHtmlGetClassify(fen_lei_html)
    url_list = list(story_url_dict.values())
    # 故事分类+第几页
    classify_page_url = prefix + random.choice(url_list) + suffix
    class_page_html = getHTMLText(classify_page_url, headers)
    # 当前页故事url list
    story_url_list = []
    parsehtml([], story_url_list, class_page_html)
    # 获得故事内容
    content = getStory(random.choice(story_url_list), headers)
    print(title + '\n' + content)
    # 百度语音合成后的MP3文件
    broadcast_mp3 = "story.mp3"
    # 百度 文字合成语音
    baidu_ai.text_to_audio("故事名：" + title + content, broadcast_mp3)
    # 百度 播放语音
    baidu_ai.voice_broadcast(broadcast_mp3)


# 原main函数
# if __name__ == '__main__':
#     # main()
#     story = "故事"
#     storyList = ["童话故事",""]
#     weather = "天气"
#     while(1):
#         result = baidu_ai.audio_to_text()
#         if story in result:
#             get_story()
#         elif weather in result:
#             weatherApi.start()

# 分支转换
def delivery(result):
    switch = {1: test_main_story, 2: weather.start}
    t = threading.Thread(target=switch[result], name=switch[result])
    t.setDaemon(True)
    t.start()


def main():
    story = ["故事", "固始", "孤石", "故世"]
    weather = ["天气", "天启", "田七", "天琪", "预报", "天气预报"]
    # main_story()
    # 语音识别结果
    # while (1):
    #     try:
    #         result = baidu_ai.audio_to_text()
    #         delivery(result)
    #     except (Exception, AttributeError, TypeError):
    #         test_main_story()
    while (1):
        try:
            result = baidu_ai.audio_to_text()
            print(baidu_ai.word_lexer(result))
            if "故事" in result:
                delivery(1)
            elif "天气" in result:
                delivery(2)
        except (Exception, TypeError):
            result = baidu_ai.audio_to_text()
            print(baidu_ai.word_lexer(result))
# print('thread %s ended.' % threading.current_thread().name)if __name__ == '__main__':
if __name__ == '__main__':
    main()