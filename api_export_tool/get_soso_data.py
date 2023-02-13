# -*- coding: utf-8 -*-
# @Time : 2023/1/16 11:48
# @Author : weiliu
# @File : get_soso_data.py.py
# @Software: PyCharm

import pandas as pd
import pymysql


import locale
locale.setlocale(locale.LC_CTYPE, 'chinese')


class GetSosoData:
    '''
    获取soso数据库中的testcase
    '''
    def __init__(self):
        try:
            self.dbconn = pymysql.connect(
                user='root' ,            # 用户名
                password='Ynby12#$',  # 密码：这里一定要注意123456是字符串形式
                host='10.11.201.98',  # 指定访问的服务器，本地服务器指定“localhost”，远程服务器指定服务器的ip地址
                database='sosotest_data',  # 数据库的名字
                port=3306,   # 指定端口号，范围在0-65535
                charset='utf8',  # 数据库的编码方式
            )
            self.cur = self.dbconn.cursor(cursor=pymysql.cursors.DictCursor)
        except Exception as error:
            print(f'数据库链接失败,失败原因：{error}')

    def get_testcases(self):
        '''
        获取soso中所有接口表头，写入pandas中
        :return:
        '''
        data_read = pd.read_sql('select * from sosotest_data.tb_http_interface', con=self.dbconn)
        data_read.drop(columns=['id', 'casedesc', 'caselevel', 'status', 'caseType', 'varsPre', 'header', 'params',
                         'bodyType', 'bodyContent',
                         'timeout', 'varsPost', 'performanceTime', 'state', 'modBy', 'addBy', 'sourceId',
                         'customUri', 'useCustomUri',
                         'urlRedirect'], inplace=True)
        return data_read

    # 获取B2b 的cases
    def get_b2b_cases(self):
        df_b2b = GetSosoData().get_testcases().query("businessLineId == 3")
        return df_b2b

    # 获取口腔 的cases
    def get_oral_cases(self):
        df_oral = GetSosoData().get_testcases().query("businessLineId == 2")
        return df_oral

    # 获取阡陌 的cases
    def get_qianmo_cases(self):
        df_qianmo = GetSosoData().get_testcases().query("businessLineId == 1")
        return df_qianmo

    # 获取tcm 的cases
    def get_tcm_cases(self):
        df_tcm = GetSosoData().get_testcases().query("businessLineId == 4")
        return df_tcm



    # def get_task_data(self, sql_task):
    #     '''
    #     获取task中的数据
    #     :param sql:
    #     :return: 所有在task中的数据
    #     '''
    #     list_url = []
    #     # 获取加入执行任务中的接口链接p
    #     sql_task = sql_task
    #     self.cur.execute(sql_task)
    #     data_task = self.cur.fetchall()
    #     # 获取接口对应的soso业务流的caseid，字符串格式
    #     data_task_flow_id = data_task[0]['taskTestcases']
    #     # 获取soso中接口的interfaceId，字符串格式
    #     data_task_api_id = data_task[0]['taskInterfaces']
    #     # 将相应字符串转换为列表
    #     list_flow = data_task_flow_id.split(',')
    #     list_interface = data_task_api_id.split(',')
    #     # 获取加入到b2b执行任务中的接口url--sql语句
    #     sql_api = "select url from tb_http_interface where interfaceId in %s"
    #     self.cur.execute(sql_api, (list_interface,))
    #     data_task_api = self.cur.fetchall()
    #     #  # 获取加入到业务流中的接口url--sql语句
    #     sql_api_flow = "select url from tb_http_testcase_step where caseId in %s"
    #     self.cur.execute(sql_api_flow, (list_flow,))
    #     data_api_flow = self.cur.fetchall()
    #     # 将业务流和接口中所有接口存入列表中
    #     for i in data_task_api:
    #         list_url.append(i['url'])
    #     for i in data_api_flow:
    #         list_url.append(i['url'])
    #     list_url = list(set(list_url))
    #     # 处理返回的
    #     print('获取soso数据成功')
    #     # 这里返回的是在task中的url经过了接口和任务流的去重
    #     return list_url


    # # 获取b2b任务接口
    # def get_task_b2b(self):
    #     sql_task = 'select taskInterfaces,taskTestcases from tb_task_execute where id = (select max(id) from tb_task_execute where taskId = "HTTP_TASK_3") group by taskId'
    #     task_b2b = GetSosoData().get_task_data(sql_task)
    #     return task_b2b
    #
    # # 获取tcm任务接口
    # def get_task_tcm(self):
    #     sql_task = 'select taskInterfaces,taskTestcases from tb_task_execute where id = (select max(id) from tb_task_execute where taskId = "HTTP_TASK_2") group by taskId'
    #     task_tcm = GetSosoData().get_task_data(sql_task)
    #     return task_tcm
    #
    # # 获取oral任务接口
    # def get_task_oral(self):
    #     # 口腔患者端
    #     sql_task_patient = 'select taskInterfaces,taskTestcases from tb_task_execute where id = (select max(id) from tb_task_execute where taskId = "HTTP_TASK_5") group by taskId'
    #     task_oral_patient = GetSosoData().get_task_data(sql_task_patient)
    #     # 口腔运营端
    #     sql_task_operation = 'select taskInterfaces,taskTestcases from tb_task_execute where id = (select max(id) from tb_task_execute where taskId = "HTTP_TASK_4") group by taskId'
    #     task_oral_operation = GetSosoData().get_task_data(sql_task_operation)
    #     # 二者接口合并
    #     task_oral = task_oral_operation + task_oral_patient
    #     task_oral = set(task_oral)
    #
    #     return task_oral
    #
    # # 获取qianmo任务接口
    # def get_task_qianmo(self):
    #     sql_task = 'select taskInterfaces,taskTestcases from tb_task_execute where id = (select max(id) from tb_task_execute where taskId = "HTTP_TASK_1") group by taskId'
    #     task_qianmo = GetSosoData().get_task_data(sql_task)
    #     return task_qianmo








