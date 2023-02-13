# -*- coding: utf-8 -*-
# @Time : 2023/1/17 14:39
# @Author : weiliu
# @File : write_data.py.py
# @Software: PyCharm

import pandas as pd
import os
import datetime
import winreg
import json
import locale
# 解决datetime.strftime，格式中文存在encoding error的问题
locale.setlocale(locale.LC_CTYPE, 'chinese')

'''
todolist:
1、生成一个表格，表头包括
项目，模块，模块接口数， 模块已导入soso的接口数， 未导入soso接口数
2、每个项目生成一个单独的文件夹，文件夹包括处理好的json和最后的统计表
3、尝试使用多线程来构造
'''

class ExcelData:
    '''
    1、excel 表头公共类，定义各个excel的表头信息
    2、将excel在桌面生成的公共方法
    '''
    def __init__(self, project_name):

        self.pd = pd
        self.project_name = project_name


    # 统计数据列表页面
    def excel_statistics(self):
        df_statistics = self.pd.DataFrame(columns=['项目', '模块', '模块接口数', ' 模块已导入soso的接口数', '未导入soso接口数', '已导入的接口比例'])
        return df_statistics

    # 创建文件夹
    def create_file(self):
        '''
        创建桌面文件夹
        :return:
        '''
        # 获取所有文件列表
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        # 选择桌面文件
        desktop = winreg.QueryValueEx(key, "Desktop")[0]
        path = desktop + '\接口未导入soso文件夹'
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        date = str(datetime.datetime.now().strftime('%Y-%m-%d %H时%M分%S秒'))
        # 创建项目文件夹
        path_poject = path + f'\{self.project_name}项目'
        if os.path.exists(path_poject):
            pass
        else:
            os.mkdir(path_poject)
        return path_poject



    def write_json(self, res_module):
        '''
        写入json数据
        :param res_module:
        :return:
        '''
        path_poject = self.create_file()
        try:
            module_name = res_module['info']['title']
            with open(path_poject + f'\{module_name}'+'.json', mode='w') as f:
                json.dump(res_module, f)
            print(f'获取{self.project_name}的{module_name}模块json文件成功！')
        except Exception as e:
            print(e)

    def write_excel(self, statistics):
        '''
        写入数据
        :param data:
        :return:
        '''
        path_poject = self.create_file()
        df_statistics = self.excel_statistics()
        for i in range(len(statistics)):
            df_statistics.loc[len(df_statistics)] = statistics[i]
        try:
            with pd.ExcelWriter(path_poject+f'\{self.project_name}导入soso接口率统计表--' + '.xlsx', mode='w') as writer:
                # 将数据写入excel中
                df_statistics.to_excel(writer, sheet_name=self.project_name, index=False)
            print(df_statistics)
            print('统计数据获取成功，请在桌面文件夹查看')
        except Exception as e:
            print(e)




# if __name__ == '__main__':
#     data = ExcelData('qianmo')
#     test = 1
#     statistics = data.write_excel(test)
#     print(statistics)