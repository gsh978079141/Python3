#!/usr/bin/python3
# -*-coding:utf-8 -*-
from socket import *
import time
COD = 'utf-8'
# 主机ip
HOST = '192.168.113.87'
# 软件端口号
PORT = 21566
BUFSIZ = 1024
ADDR = (HOST, PORT)
# 创建socket对象
tcpS = socket(AF_INET, SOCK_STREAM)
SIZE = 10
# 加入socket配置，重用ip和端口
tcpS.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
# 绑定ip端口号
tcpS.bind(ADDR)
# 设置最大链接数
tcpS.listen(SIZE)
while True:
    print("服务器启动，监听客户端链接")
    conn, addr = tcpS.accept() 
    print("链接的客户端", addr)
    while True:
        try:
            # 读取已链接客户的发送的消息
            data = conn.recv(BUFSIZ)
        except Exception:
            print("断开的客户端", addr)
            break
        print("客户端发送的内容:",data.decode(COD))
        if not data:
            break
        # 获取结构化事件戳
        msg = time.strftime("%Y-%m-%d %X")
        msg1 = '[%s]:%s' % (msg, data.decode(COD))
        # 发送消息给已链接客户端
        conn.send(msg1.encode(COD))
        # 关闭客户端链接
    conn.close()
tcpS.closel()