import socket
# 初始化socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 获取本地主机名
host = socket.gethostname()
# 端口号
port = 9999
# 绑定
server_socket.bind((host, port))
# 开始监听 最大连接数5个，多余的排队
server_socket.listen(5)
# 建立客户端连接
clientsocket, addr = server_socket.accept()

print("连接地址: %s" % str(addr))

msg = '欢迎访问菜鸟教程！' + "\r\n"
clientsocket.send(msg.encode('utf-8'))
clientsocket.close()
