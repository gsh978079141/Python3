'''
Created on 2017年12月26日

@author: gdd
'''
import socket
import time
import datetime
import requests
from bs4 import BeautifulSoup
import multiprocessing


client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host=socket.gethostbyname("openbarrage.douyutv.com")
port=8601
client.connect((host,port))
import re
path=re.compile(b'txt@=(.+?)/cid@')
uid_path=re.compile(b'nn@=(.+?)/txt@')
level_path=re.compile(b'level@=([1-9][0-9]?)/egtt@')

def sendmsg(msgstr):
    msg = msgstr.encode('utf-8')
    data_length = len(msg) + 8
    code = 689
    msgHead = int.to_bytes(data_length, 4, 'little') \
              + int.to_bytes(data_length, 4, 'little') + int.to_bytes(code, 4, 'little')
    client.send(msgHead)
    sent = 0
    while sent < len(msg):
        tn = client.send(msg[sent:])
        sent = sent + tn

def get_name(roomid):
    r = requests.get("http://www.douyu.com/"+roomid)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.find('a', {'class', 'zb-name'}).string



def keeplive():
    while True:
        msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\x00'
        print('keep live')
        sendmsg(msg)
        time.sleep(15)



def start(roomid):
        msg='type@=loginreq/username@=/password@=/roomid@={}/\x00'.format(roomid)
        sendmsg(msg)
        msg_more='type@=joingroup/rid@={}/gid@=-9999/\x00'.format(roomid)
        sendmsg(msg_more)
        
        f=open('danmudata.txt','a')
        print('连接到{}的直播间'.format(get_name(roomid)))
        while True:
            data=client.recv(1024)
            data_more=path.findall(data)
            uid_more=uid_path.findall(data)
            level_more=level_path.findall(data)
            if not data:
                print("break")
                break
            else:
                for i in range(0,len(data_more)):
                    try:    
                        print("{"+uid_more[i].decode('utf-8')+"}"+"{"+data_more[i].decode("utf-8")+"}"+'\n')
                        file_path = 'data/{}.txt'.format(datetime.date.today())
#                              弹幕写入文件
                        with open(file_path, mode='a', encoding='utf-8', errors='ignore') as f:
                            nowtime=time.strftime("%H:%M:%S")  
                            f.write("{"+nowtime+"}"+"{"+uid_more[i].decode('utf-8')+"}"+"{"+data_more[i].decode("utf-8")+"}"+'\n')
#                         conn.commit()
#                     except KeyboardInterrupt:
#                         conn.close()
# 78561   2267291
                    except:
                        continue

if __name__=='__main__':
        room_id=input("plz enter the room id")
        p1=multiprocessing.Process(target=start,args=(room_id,))
        p2=multiprocessing.Process(target=keeplive)
        p1.start()
        p2.start()