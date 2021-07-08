import configparser
import logging as log
import os
import shutil
import sys

import nacos
import yaml

from com.gsh.freqx.utils.nacos import const

# s nacos 常量配置
const.DATA_ID = "data_id"
const.GROUP = "group"
const.WATCHER_FUN = "watcher_fun"
const.CONTENT = "content"
# 默认组别
const.DEFAULT_GROUP_NAME = "DEFAULT_GROUP"
# 默认命名空间
const.DEFAULT_NAMESPACE = ""
# 默认集群名称
const.DEFAULT_CLUSTER_NAME = "DEFAULT"

# e nacos 常量配置

class NacosClient(object):

    def __init__(self, server_addresses, namespace, username, password) -> None:
        log.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'), level=log.INFO)
        self.server_addresses = server_addresses
        self.namespace = namespace
        self.username = username
        self.password = password
        # no auth mode
        # client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE)
        # auth mode
        client = nacos.NacosClient(server_addresses, namespace=namespace, username=username, password=password)
        # 调试模式
        # client.set_debugging()
        # 监听回调函数线程数
        client.set_options(callback_thread_num=1)
        self.client = client
        sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
        sys.path.append("..")

    def get_client(self):
        """
        获取nacosClient实例
        :return:
        """
        return self.client

    def add_service2nacos(self, service_name, ip, port, cluster_name=const.DEFAULT_CLUSTER_NAME, weight=1.0, metadata=None,
                          enable=True, healthy=True, ephemeral=True, group_name=const.DEFAULT_GROUP_NAME):
        """
        注册服务至nacos
        :param service_name:
        :param ip:
        :param port:
        :param cluster_name:
        :param weight:
        :param metadata:
        :param enable:
        :param healthy:
        :param ephemeral:
        :param group_name:
        :return:
        """
        self.client.add_naming_instance(service_name, ip, port, cluster_name, weight, metadata, enable, healthy,
                                        ephemeral, group_name)

    def send_heartbeat(self, service_name, ip, port, cluster_name=const.DEFAULT_CLUSTER_NAME, weight=1.0, metadata=None, ephemeral=True,
                       group_name=const.DEFAULT_GROUP_NAME):
        """
        发送服务心跳
        :param service_name:
        :param ip:
        :param port:
        :param cluster_name:
        :param weight:
        :param metadata:
        :param ephemeral:
        :param group_name:
        :return:
        """
        self.client.send_heartbeat(service_name, ip, port, cluster_name, weight, metadata, ephemeral, group_name)

    def get_nacos_original_config(self, data_id, group):
        """
        获取原始配置
        :param data_id: 连接信息
        :param group: 用户数据
        :return:
        """
        nacos_config = self.client.get_config(data_id, group)
        print("get_nacos_original_config :%s" % nacos_config)
        return nacos_config

    def add_watchers(self, watchers):
        """
        添加观察者/配置文件修改监听器
        :param watchers: 观察者信息列表
        :return:
        """
        for watcher in watchers:
            self.client.add_config_watchers(watcher.get(const.DATA_ID), watcher.get(const.GROUP),
                                            [watcher.get(const.WATCHER_FUN)])


class NacosFormatConvert:
    """
    配置文件格式转化类
    """

    @staticmethod
    def config2yaml(nacos_original_config):
        """
        yaml文件格式转化
        :param nacos_original_config: nacos返回的原始数据
        :return: 返回字典类型,conf['key']
        """
        conf = yaml.load(nacos_original_config, Loader=yaml.FullLoader)
        print("config2yaml : %s" % conf)
        return conf

    @staticmethod
    def config2ini(nacos_original_config):
        """
        ini文件格式转化
        文件格式：
        [common]
        url = www.gshyun.com
        :param nacos_original_config: nacos返回的原始数据
        :return: 读取属性-conf.get("common","url") -> www.gshyun.com
        """
        conf = configparser.ConfigParser()
        conf.read_string(nacos_original_config)
        print("config2ini : %s" % conf)
        return conf

    @staticmethod
    def default_config_format_converter(nacos_original_config):
        """
        未知格式，默认透传
        :param nacos_original_config: nacos返回的原始数据
        :return:
        """
        return nacos_original_config

    @staticmethod
    def config_format_converter(data):
        """
        文件格式转化入口
        :param data:
        :return:
        """
        # 文件后缀
        file_suffix = data[const.DATA_ID].split(".")[1]
        switch = {'yaml': NacosFormatConvert.config2yaml,  # 注意此处不要加括号
                  'ini': NacosFormatConvert.config2ini}
        return switch.get(file_suffix, NacosFormatConvert.default_config_format_converter)(data[const.CONTENT])

    def print_cm(self, status, data_id, group, namespace):
        """
        将snapsho file复制到本地的文件路径
        :param status:
        :param data_id:
        :param group:
        :param namespace:
        :return:
        """
        snapshot_file = "{0}+{1}+{2}".format(status[data_id], status[group], namespace)
        for p in self.cf['configs']:
            if status[data_id] == p['id'] and status[group] == p[group]:
                shutil.copy("nacos-data/snapshot/{}".format(snapshot_file), p['path'])  #
        return True
