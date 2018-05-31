#先加一个群里面的好友，然后把群中的人邀请加入另一个群
import itchat
# 自动登录
itchat.auto_login(hotReload=True)
# 获取群聊列表
rooms=itchat.get_chatrooms()
# 用户输入要转移到的群名称：     
bRoomName = '哈哈哈'
# 声明总用户的列表
# 根据群名称得到群对象
bRoom=itchat.search_chatrooms(name=bRoomName)
# 遍历所有的群
# #     获得每个群的群成员列表
memList=itchat.update_chatroom(rooms[0]['UserName'])['MemberList']
    # #     将每个群成员加入总用户列表
    # #     遍历群成员列表
for mem in memList :
    # #         获得每个成员的用户名（此处可扩展得到签名 备注 城市 性别等信息）
    userName=mem.UserName
################正式启动 ###############################
    # 添加好友
    if itchat.add_friend(userName=userName,status=2):
        print('添加成功')
    else:
        print('添加失败')
        

#######################################################
#     拉好友进群memList为一个字典dict(类似java中的map)
# 睡眠5分钟等接收添加好友后，准备将此好友移至新群       
# time.sleep(120) 
# for allmem in allMemList :
#     try :
#         itchat.add_member_into_chatroom(bRoom.UserName,allmem) 
#     except :
#         print("转移失败！")
# print("转移成功！")




