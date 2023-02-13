# -*- coding: utf-8 -*-
# @Time : 2023/1/30 15:17
# @Author : weiliu
# @File : api_export_tool.py.py
# @Software: PyCharm

from get_soso_data import GetSosoData
from write_data import ExcelData
from read_swagger_api import ReadSwaggerApiDocs
from read_yapi_api import ReadYapiApiDocs

class GetData:
    def __init__(self, project_name):
        self.project_name = project_name

    def get_swagger_data(self, url,  soso_data):
        '''
        获取swagger的数据
        :param url:
        :param soso_data:
        :return:
        '''
        api_doc = ReadSwaggerApiDocs(url, project_name=self.project_name)
        modules = api_doc.get_swagger_modules()
        # 所有用例的接口
        list_statistics_all = []
        for i in range(len(modules)):
            res_url_list = api_doc.compare_data_and_rewrite(module=modules[i] , soso_data=soso_data)
            list_statistics = res_url_list[1]
            res_module = res_url_list[0]
            # 将静态文件写入列表中
            list_statistics_all.append(list_statistics)
            result = ExcelData(project_name=self.project_name).write_json(res_module=res_module)
        statistics = ExcelData(project_name=self.project_name).write_excel(statistics=list_statistics_all)

    def get_yapi_data(self, url, soso_data, login_data):
        '''
        获取swagger的数据
        :param url:
        :param soso_data:
        :return:
        '''
        api_doc = ReadYapiApiDocs(url, project_name=self.project_name, login_data=login_data)
        modules = api_doc.get_yapi_modules()
        modules = modules[0]
        # 所有用例的接口
        list_statistics_all = []
        for i in range(len(modules)):
            res_url_list = api_doc.compare_data_and_rewrite(module=modules[i] , soso_data=soso_data)
            list_statistics = res_url_list[1]
            res_module = res_url_list[0]
            # 将静态文件写入列表中
            list_statistics_all.append(list_statistics)
            result = ExcelData(project_name=self.project_name).write_json(res_module=res_module)
        statistics = ExcelData(project_name=self.project_name).write_excel(statistics=list_statistics_all)

    def get_qianmo_data(self):
        '''
        获取阡陌的测试数据
        :return:
        '''
        print(f'开始获取{self.project_name}导入soso的接口数据.....')
        data = GetSosoData()
        # soso中所有接口
        soso_data = data.get_qianmo_cases()
        url = 'http://192.168.32.85:9600'

        result = GetData(self.project_name).get_swagger_data(url=url, soso_data=soso_data)
        print(f'{self.project_name}接口接口数据统计获取完成.....')

    def get_tcm_data(self):
        '''
        获取中医体质的测试数据
        :return:
        '''
        print(f'开始获取{self.project_name}导入soso的接口数据.....')
        data = GetSosoData()
        # soso中所有接口
        soso_data = data.get_tcm_cases()
        # # print(task_data)
        url = 'http://10.11.201.106:9700'
        result = GetData(self.project_name).get_swagger_data(url=url, soso_data=soso_data)
        print(f'{self.project_name}接口接口数据统计获取完成.....')

    def get_b2b_data(self):
        print(f'开始获取{self.project_name}接口自动化覆盖率.....')
        project_name = 'b2b'
        data = GetSosoData()
        # 获取soso中的所有接口
        soso_data = data.get_b2b_cases()

        # b2b中yapi的接口信息
        url = 'http://192.168.32.66:3000'
        login_data = {"email": "hehuiling@ynby.cn" , "password": "ynby@123456"}
        result = GetData(self.project_name).get_yapi_data(url=url, soso_data=soso_data, login_data=login_data)
        print(f'{self.project_name}接口接口数据统计获取完成.....')

    def get_oral_data(self):
        print(f'开始获取{self.project_name}接口自动化覆盖率.....')
        project_name = 'oral'
        data = GetSosoData()
        # 获取soso中的所有接口oral
        soso_data = data.get_oral_cases()

        # 口腔中yapi的接口信息
        url = 'http://192.168.32.30:3000'
        login_data = {"email": "hehuiling@ynby.cn", "password": "123456"}
        result = GetData(self.project_name).get_yapi_data(url=url, soso_data=soso_data, login_data=login_data)
        print(f'{self.project_name}接口接口数据统计获取完成.....')

if __name__ == '__main__':
    print('#################---打印数据仅供参考---#################')
    print('''\'/sys/dict/device' 和  /sys/dict/device/{id} 在过滤参数后都会变为'/sys/dict/device'
这样与soso中相比较，上面两个接口都会被认为在soso中存在而被过滤，导致数据不准确
    ''')
    while True:
        print('业务线列表如下:', '\n'
              '0.结束程序', '\n'
              '1.阡陌', '\n'
              '2.中医体质', '\n'
              '3.b2b', '\n'
              '4.口腔')
        print('请选择需要获取接口覆盖率统计信息的业务线：')
        number = int(input())
        if number == 1:
            qianmo_data = GetData('阡陌').get_qianmo_data()
            print('----------华丽的分割线----------')
        elif number == 2:
            tcm_data = GetData('中医体质').get_tcm_data()
            print('----------华丽的分割线----------')
        elif number == 3:
            b2b_data = GetData('b2b').get_b2b_data()
            print('----------华丽的分割线----------')
        elif number == 4:
            oral_data = GetData('oral').get_oral_data()
            print('----------华丽的分割线----------')
        elif number == 0:
            print('结束程序')
            exit()
        else:
            print('输入的业务线ID错误或不存在！')


