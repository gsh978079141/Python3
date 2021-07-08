import socket
import time
from com.gsh.freqx.utils.mqtt.MqttUtils import MqttClient
from com.gsh.freqx.utils.nacos import const
from com.gsh.freqx.utils.nacos.NacosUtil import NacosClient, NacosFormatConvert


# mqtt测试
def mqtt_test():
    # 启动监听
    topic = "/test/gsh"
    ip = "192.168.0.107"
    username = "admin"
    password = "public"
    mqtt_client = MqttClient(ip=ip, topic=topic, username=username, password=password)
    while True:
        pass


def nacos_test():
    data_id_yaml = "config.yaml"
    group_yaml = "DEFAULT_GROUP"
    data_id_ini = "init.ini"
    group_ini = "DEFAULT_GROUP"
    # s nacos基础信息配置
    server_addresses = "192.168.0.107:8848"
    namespace = "python-test"
    username = "nacos"
    password = "nacos"
    # e nacos基础信息配置
    nacos_client = NacosClient(server_addresses=server_addresses, namespace=namespace, username=username,
                               password=password)
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)


    # 模拟处理nacos配置更新(yaml)
    def exec_config_yaml(data):
        final_data = NacosFormatConvert.config_format_converter(data=data)
        print("exec_config_yaml : %s" % final_data)

    # 模拟处理nacos配置更新(ini)
    def exec_init_ini(data):
        final_data = NacosFormatConvert.config_format_converter(data=data)
        print("exec_init_ini : %s" % final_data)

    # 新增配置更新监视器
    def nacos_add_watchers():
        watchers = []
        watchers.append({const.DATA_ID: data_id_yaml, const.GROUP: group_yaml,
                         const.WATCHER_FUN: exec_config_yaml})
        watchers.append({const.DATA_ID: data_id_ini, const.GROUP: group_ini,
                         const.WATCHER_FUN: exec_init_ini})
        nacos_client.add_watchers(watchers)

    # 新增服务实例至nacos
    def add_service2nacos():
        nacos_client.add_service2nacos(service_name="python-service-1", ip=ip, port="8081", ephemeral=True)

    # 新增配置更新监视器
    nacos_add_watchers()

    add_service2nacos()

    while True:
        time.sleep(2)
        nacos_client.send_heartbeat(service_name="python-service-1", ip=ip, port="8081", ephemeral=True)
    # nacos_config = get_nacos_original_config(DATA_ID, GROUP)
    # config2yaml = NacosFormatConvert.config2yaml(nacos_config)
    # 获取具体属性值: config2yaml['configs']['name']
    # print("main config2yaml : %s ", config2yaml)


if __name__ == '__main__':
    nacos_test()

