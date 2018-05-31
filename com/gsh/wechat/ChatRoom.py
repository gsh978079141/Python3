#先加一个群里面的好友，然后把群中的人邀请加入另一个群
import itchat
# 自动登录
itchat.auto_login(hotReload=True)
# itchat.auto_login(hotReload=True)
# itchat.send('大扎好，我系轱天乐，我四渣嘎辉，探挽懒月，介四里没有挽过的船新版本，'
#                 '挤需体验三番钟，里造会干我一样，爱像借款游戏。'
#                 , toUserName=itchat.search_chatrooms(name=u'测试A群')[0]['UserName'])


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

@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing'])
def text_reply(msg):
    text=msg['Text']
    if text=='sb' :
        itchat.send('您的信息涉嫌违规！', msg['FromUserName'])

        itchat.send(msg['Text'],toUserName=itchat.search_chatrooms(name=u'哈哈哈')[0]['UserName'])
        itchat.send(msg['Text'],toUserName=itchat.search_chatrooms(name=u'测试B群')[0]['UserName'])
#     itchat.send('%s: %s'%(msg['Type'], msg['Text']), msg['FromUserName'])
# myUserName=@4764dc7e91a98f8ec9d8951162497c9cd5d37bb3febf7db28f8ebbbef2307e35
# 处理多媒体类消息
# 包括图片、录音、文件、视频
@itchat.msg_register(['PICTURE', 'RECORDING', 'ATTACHMENT', 'VIDEO'])
def download_files(msg):
    print('文件处理')
    # msg['Text']是一个文件下载函数
    # 传入文件名，将文件下载下来
    msg['Text'](msg['FileName'])
    # 把下载好的文件再发回给发送者
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register(itchat.content.CARD,isFriendChat = True)
def addFriend(msg):
    print(msg['Text'])
    print(msg['Content'])
    itchat.add_friend(userName = msg['Text']['UserName'])
    print(msg['RecommendInfo']['UserName'])
    
itchat.run(debug=True)

