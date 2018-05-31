import itchat

@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing'])
def text_reply(msg):
    itchat.send('%s: %s'%(msg['Type'], msg['Text']), msg['FromUserName'])

@itchat.msg_register('Friends')
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.get_contact()
    itchat.send_msg(msg['RecommendInfo']['UserName'], 'Nice to meet you!')


itchat.auto_login()
itchat.run()
