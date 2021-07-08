import logging as log
import os
import sys
import threading
import time
import paho.mqtt.client as mqtt


class MqttClient(object):

    def __init__(self, ip, topic, username, password) -> None:
        log.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'), level=log.INFO)
        self.ip = ip
        self.username = username
        self.password = password
        sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
        sys.path.append("..")
        client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        client = mqtt.Client(client_id, transport='tcp')
        self.client = client
        self.topic = topic
        t = threading.Thread(target=self.server_conenet, args=(self.client,), daemon=True)
        t.start()
        time.sleep(1)
        # self.server_conenet(client=self.client)

    # 订阅回调函数
    def on_connect(self, client, userdata, flags, rc):
        log.info('connected to mqtt with resurt code ', rc)
        client.subscribe(self.topic)  # 订阅主题

    # 使用静态方法 因为参数是固定的
    @staticmethod
    def on_message(client, userdata, msg):
        """
        接收客户端发送的消息
        :param client: 连接信息
        :param userdata: 用户数据
        :param msg: 客户端返回的消息
        :return:
        """
        # payload = json.loads(msg.payload.decode('utf-8'))
        payload = msg.payload.decode('utf-8')
        # if payload['type'] == 'pic':
        #     data = base64.b64decode(payload['msg'])
        #     image_url = os.path.join('D://%s.jpg' % int(time.time()))
        #     with open(image_url, 'wb') as f:
        #         f.write(data)
        log.info("receive msg : ", payload)
        print("receive msg : ", payload)

    # 服务监听
    def server_conenet(self, client):
        client.on_connect = self.on_connect  # 启用订阅模式
        client.on_message = self.on_message  # 接收消息
        client.username_pw_set(self.username, self.password)
        client.connect(self.ip, 1883, 60)  # 链接
        client.loop_start()  # 以start方式运行，需要启动一个守护线程，让服务端运行，否则会随主线程死亡
        # client.loop_forever()  # 以forever方式阻塞运行。

    # 服务停止
    def server_stop(client):
        client.loop_stop()  # 停止服务端
        sys.exit(0)

    # 发布消息
    def publish_message(self, topic, msg):
        self.client.publish(topic, msg)
