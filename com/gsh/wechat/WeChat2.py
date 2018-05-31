import itchat
itchat.auto_login(hotReload=True)
chatrooms=itchat.get_chatrooms()
# for chatroom in chatrooms:
#     print(chatroom)
#     chatName=itchat.get_friends()
#     chatName=itchat.search_friends(chatroom.UserName)
chatroom=chatrooms[0]      
memList=itchat.update_chatroom(chatroom.UserName).MemberList
# for i in list:
#     print ("序号：%s   值：%s" % (list.index(i) + 1, i))
for mem in memList:
#     itchat.add_friend(mem.UserName,status=2)
#     itchat.send('hello',toUserName=mem.UserName)
    print(mem)
# 创建群聊，topic键值为群聊名
# 删除群聊内的用户
# itchat.delete_member_from_chatroom('测试B群', memList)
# 增加用户进入群聊
itchat.add_member_into_chatroom('测试B群', memList)
# itchat.add_friend(userName='@d6f7438280745a4d7513eddfe9a753dd60f4548705c22d4cd8c483f467bc4f21',status=2)
# for mem in memList:
#     print(mem.ChatroomMember)
# for mem in memList:
#     print(mem.MemberList)
#     itchat.add_friend
# fri=itchat.search_friends(userName='@d6f7438280745a4d7513eddfe9a753dd60f4548705c22d4cd8c483f467bc4f21')
# print(fri)
