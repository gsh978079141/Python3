import itchat
from itchat.content import TEXT
# 登录
itchat.auto_login(hotReload=True)#热启动微信
# 发送消息
itchat.send(u'test', 'filehelper')
# 获取好友列表
friends = itchat.get_friends(update=True)[0:]
room = itchat.search_friends(name=r'于志伟') #这里输入你好友的名字或备注。
username=room[0]['UserName']
itchat.send("哈哈哈",toUserName=username)
 

# 初始化计数器，有男有女，当然，有些人是不填的
# male = female = other = 0
# 遍历这个列表，列表里第一位是自己，所以从"自己"之后开始计算
# 1表示男性，2女性
# for i in friends[1:]:
#     sex = i["Sex"]
#     if sex == 1:
#         male += 1
#     elif sex == 2:
#         female += 1
#     else:
#         other += 1

# 总数算上，好计算比例啊～
# total = len(friends[1:])

# 好了，打印结果
# print(u"男性好友：%.2f%%",  (float(male) / total * 100)
# print( u"女性好友：%.2f%%" , (float(female) / total * 100)
# # print (u"其他：%.2f%%" , (float(other) / total * 100)
# print("男性好友:%.2f",float(male)/total*100)
# print("女性好友:%.2f",float(female)/total*100)
# print("其他性好友:%.2f",float(other)/total*100)


#  
# @itchat.msg_register
# def simple_reply(msg):
#   if msg['Type'] == TEXT:
#     return 'I received: %s' % msg['Content']
 

itchat.run()