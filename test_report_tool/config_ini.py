# -*- coding: utf-8 -*-
# @Time : 2023/2/7 9:32
# @Author : weiliu
# @File : config_ini.py.py
# @Software: PyCharm

import configparser
import os

class ConfigIni:
    '''
    获取配置文件

     BASE_PATH: 获得当前项目的绝对路径
    config_file_path:获取当前配置文件的路径，相当于根路径
    '''

   # BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    # 获取当前目录
    BASE_PATH = os.getcwd()
    # 获取当前配置文件的路径，相当于根路径,读取config.ini配置文件
    config_file_path = os.path.join(BASE_PATH, "config.ini")

    def __init__(self, file_path=config_file_path):
        '''
        定义一个配置文件的对象，默认一个文件路径，可自己补充其他路径
        :param file_path: 配置文件的绝对路径
        '''
        # 定义对象
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path,encoding="utf-8-sig")

    def get_key(self, section, option):
        '''
        获取配置文件的value值
        :param section: 配置文件中section的值
        :param option: 配置文件中option的值
        :return:
        '''
        value = self.cf.get(section, option)
        return value

    def set_value(self, section, option, value):
        '''
        修改value的值
        :param section:
        :param option:
        :param value:
        :return:
        '''
        self.cf.set(section, option, value)
        with open(self.config_file_path, 'w+') as f:
            self.cf.write(f)

cf = ConfigIni()

if __name__ == '__main__':
    value = cf.get_key('redmine', 'fixed_version_id')
    value = value.split(",")
    print(value)
    print(type(value))