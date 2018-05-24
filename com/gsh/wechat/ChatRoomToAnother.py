#coding=UTF-8
# 一个群中的人邀请加入另一个群
import itchat
itchat.login()
# itchat.auto_login(hotReload=True)
#search得到一个list下标0第一个
Aroom=itchat.search_chatrooms(name='测试A群')
Broom=itchat.search_chatrooms(name='哈哈哈')

friends=itchat.get_friends()
print(friends)
# 自动更行memList
memberList =itchat.update_chatroom(Aroom[0].UserName).MemberList
for mem in memberList:
    try:
        print(mem.UserName)
        itchat.add_friend(userName=mem.UserName,status=2)
    except:
        print("添加好友失败")
    print("添加好友成功")
try:
#     添加好友到群memList为一个字典dict(类似java中的map)
    itchat.add_member_into_chatroom(Broom.UserName,memberList)  
except:
    print('转移群聊失败')

