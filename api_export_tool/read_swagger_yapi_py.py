# -*- coding: utf-8 -*-
# @Time : 2023/2/3 11:21
# @Author : weiliu
# @File : read_swagger_yapi_py.py
# @Software: PyCharm


from write_data import ExcelData
import requests
import re
from get_soso_data import GetSosoData
from pandas.api.types import CategoricalDtype

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                         '/107.0.0.0 Safari/537.36',
               'Content-Type': 'application/json'}

RE_PATTERN = re.compile(r'/\d+$|/$|/true|/false|/:[a-zA-Z]+|/{.+}|/[a-zA-Z0-9]+-[a-zA-Z0-9-]+-[a-zA-Z0-9]+[a-zA-Z0-9]$')


class ReadSwaggerApiDocs:
    '''
    获取swagger接口信息，与soso接口信息进行比较
    将比较结果写入excel中
    '''

    def __init__(self, url, project_name, login_data=0):
        '''

        :param url: 项目url
        :param project_name: 项目名字
        :param login_data: 登录信息，默认为空可以不填写
        '''
        #  http://192.168.32.85:9600/swagger-resources传入资源地址获取链接
        self.url = url
        self.resource_url = self.url + '/swagger-resources'
        self.project_name = project_name
        self.login_data = login_data


    def get_api_resource(self, url):
        '''
        获取接口的返回信息，调用接口返回response
        :param url: 接口地址
        :return:
        '''
        res = requests.get(url, headers=HEADERS)
        if res.status_code == 200:
            return res.json()
        else:
            print(res.text)
            return "获取接口文档失败"

    def get_soso_case_data(self, soso_data):
        '''
        获取soso中已经加入case的列表
        :param soso_data: 已经加入soso的接口
        :return: 返回已经加入soso的列表
        '''
        # 获取soso中的数据接口
        soso_data = soso_data
        soso_url_list = soso_data['url'].to_list()
        # 处理url中的替换数字及参数，只保留纯接口
        soso_url_list_change = []
        for url in range(len(soso_url_list)):
            soso_url_list_change.append(RE_PATTERN.sub('', soso_url_list[url]))
        return soso_url_list_change


    def get_swagger_modules(self):
        '''
        获取swagger中的接口模块
        :return:
        '''
        url = self.resource_url
        try:
            # res = ReadSwaggerApiDocs(self.url, self.project_name).get_api_resource(url)
            res = self.get_api_resource(url)
            modules_list = []
            # 循环获取模块信息
            for i in range(len(res)):
                modules_list.append(res[i]['url'])
            return modules_list
        except Exception as error:
            print(f'{error}')

    def get_single_module_res(self, module):
        '''
        获取单个模块的swagger.json文件
        1、在这里做判断，如果是阡陌和b2b就直接调用self.url + module
        2、如果是b2b和口腔，就调用下载接口
        :param module: 传入模块名称或者id
        :return:
        '''
        if self.project_name == '阡陌' or self.project_name == '中医体质':
            module_url = self.url + module
            try:
                # 获取单个模块的接口swaggerjson文档信息
                res_module = self.get_api_resource(module_url)
                return res_module
            except Exception as e:
                print(f"获取接口文档失败，失败原因：{e}")
        else:
            # module_url = self.url + '/api/plugin/exportSwagger?type=OpenAPIV2&pid=52&status=all&isWiki=false'
            # 拼接下载路径
            # module_url = self.url + '/api/plugin/exportSwagger?type=OpenAPIV2&pid=' + module + '&status=all&isWiki=false'
            try:
                # 获取单个模块的接口swaggerjson文档信息
                res_module = self.get_api_resource(module_url)
                return res_module
            except Exception as e:
                print(f"获取接口文档失败，失败原因：{e}")






    def get_yapi_modules(self):
        '''
        1、获取yapi中的模块和对应的token信息
        2、获取项目的project_id
        3、通过导出接口获取swagger 文件

        :return: 模块和token对应的字典值
        '''
        # 登录地址
        login_url = self.url + '/api/user/login'
        # 登录获取cookie信息
        try:
            login_response = requests.post(url=login_url, json=self.login_data, headers=HEADERS, allow_redirects=False)

            # 获取登录后的请求头，正则提取_yapi_token和 _yapi_uid
            res_head = login_response.headers['Set-Cookie']
            _yapi_token = re.findall("_yapi_token=(.+?);", res_head)
            _yapi_uid = re.findall("_yapi_uid=(.+?);", res_head)
            # 组装登录的信息头
            login_headers = {
                'content-type': 'application/json;charset=UTF-8' ,
                'Cookie': '_yapi_token=' + _yapi_token[0] + ';_yapi_uid=' + _yapi_uid[0]
            }
            # 调用group/list接口获取接口所在的组，这里group_id是一个组的ID，整个项目所在的组
            group_list_url = self.url + '/api/group/list'
            response_id = requests.get(url=group_list_url, headers=login_headers, allow_redirects=False)
            group_id = response_id.json()['data'][1]['_id']
            # 组装api_project_url
            api_project_url = self.url + '/api/project/list?group_id=' + str(group_id) + '&page=1&limit=10'
            response_list = requests.get(url=api_project_url, headers=login_headers, allow_redirects=False)
            res = response_list.json()['data']['list']
            # 获取project_name 和对应的 uid值
            list_module_name = []           # 模块名称
            list_module_id = []             # 模块对应的ID
            for i in range(len(res)):
                list_module_name.append(res[i]['name'])
                list_module_id.append(res[i]['_id'])
                # return dic_api, login_headers
            return list_module_id, list_module_name
        except Exception as e:
            raise e

            # export_url = self.project_name + '/api/plugin/export?type=json&pid=' + list_module_id[i] + '&status=all&isWiki=false'
            # 导出文件，文件格式为swagger_json格式
            export_url = self.url + '/api/plugin/exportSwagger?type=OpenAPIV2&pid=52&status=all&isWiki=false'
            response_export = requests.get(url=export_url, headers=login_headers, allow_redirects=False)
            print(response_export.status_code)
            print(response_export.json())


    def get_pure_swagger_url(self, res_module):
        '''
        判断path字段有没有，如果没有就不保留，有就就行处理逻辑
        :param res_module: 单个模块的swagger_json
        :param soso_data: soso中的url信息
        :return: 返回一个swaggerjson文件，该文件只包括soso中不存在的接口信息
        '''
        if 'paths' in res_module:
            # 如果是阡陌的话项目还有/test/qianmo这个头
            module_url_list_qianmo = []
            # 取模块的名字
            module_name = res_module['basePath']
            # 获取模块的列表字典
            module_url_dic = res_module['paths']
            # 获取接口列表
            module_url_list = list(module_url_dic)
            # 拼接接口和处理接口留下纯接口
            if self.project_name == "阡陌":
                for i in range(len(module_url_list)):
                    # 将模块与url拼接
                    module_url_list[i] = module_name + module_url_list[i]
                    # 去除多余参数的影响
                    module_url_list[i] = RE_PATTERN.sub('', module_url_list[i])
                    # 生成加了/test/qianmo这个头的列表
                    module_url_list_qianmo.append('/test/qianmo'+ module_url_list[i])
            else:
                for i in range(len(module_url_list)):
                    # 将模块与url拼接
                    module_url_list[i] = module_name + module_url_list[i]
                    # 去除多余参数的影响
                    module_url_list[i] = RE_PATTERN.sub('', module_url_list[i])
            sum_swagger = len(module_url_list)
            return module_url_list, sum_swagger, module_url_list_qianmo
        else:
            module_name = res_module['basePath']
            module_url_list = []
            sum_swagger = len(module_url_list)
            print(f'{module_name}模块接口数为{sum_swagger}')
            return module_url_list, sum_swagger


        '''
        对比的逻辑
        1、首先将swagger接口，过滤，留下纯接口
        2、然后与soso中的列表对比
        3、对比中了记录其下标，然后通过下标找到swagger接口未过滤的值
        4、然后在字典中将对应的key值取消
        '''

    def compare_data_and_rewrite(self, module, soso_data):
        '''
        1、首先将swagger接口，过滤，留下纯接口
        2、然后与soso中的列表对比
        3、对比中了记录其下标，然后通过下标找到swagger接口未过滤的值
        4、然后在字典中将对应的key值取消
        :param url_lsit:
        :param soso_data:
        :return:
        '''
        sum_in_soso = 0
        sum_swagger = 0
        # 过滤后的soso_data
        soso_data = self.get_soso_case_data(soso_data)
        # 获取swagger模块的json值
        res_module = self.get_single_module_res(module)
        # 防止接口文档获取失败导致的异常
        module_name_change = ''
        if res_module != '获取接口文档失败':
            # 修改swagger接口中的相关属性
            module_name_change = res_module['basePath'].replace('/' , '_')
            # 如果存在路径就获取，进行下面的流程
            if 'paths' in res_module:
                # # 获取模块的列表字典
                module_url_dic = res_module['paths']
                # 获取纯正的swagger接口列表
                module_url_list_pure = list(module_url_dic)
                # 获取过滤后的module_url_list
                module_url = self.get_pure_swagger_url(res_module)
                # 获取module_url_list和接口中总数
                module_url_list = module_url[0]
                sum_swagger = module_url[1]
                module_url_list_qianmo = module_url[2]
                if self.project_name == '阡陌':
                    # 进行对比过程
                    for i in range(sum_swagger):
                        # 判断swagger中的url是否在soso中
                        if module_url_list[i] in soso_data or module_url_list_qianmo[i] in soso_data :
                            # 如果存在就从原来的字典中删除
                            del module_url_dic[module_url_list_pure[i]]
                            sum_in_soso += 1
                        else:
                            continue
                else:
                    for i in range(sum_swagger):
                        # 判断swagger中的url是否在soso中
                        if module_url_list[i] in soso_data:
                            # 如果存在就从原来的字典中删除
                            del module_url_dic[module_url_list_pure[i]]
                            sum_in_soso += 1
                        else:
                            continue
                # 替换swaggerJson的title为项目+模块名字
                res_module['info']['title'] = self.project_name + module_name_change
                # 重新拼接路径的字典值
                res_module['paths'] = module_url_dic
            else:
                pass
        # global SUM_SWAGGER, SUM_IN_SOSO, SUM_OUT_SOSO
        # SUM_SWAGGER = sum_swagger
        # SUM_IN_SOSO = sum_in_soso
        # SUM_OUT_SOSO = sum_swagger - sum_in_soso

        # 生成统计数据
        sum_out_soso = sum_swagger - sum_in_soso
        list_statistics = []
        # 插入项目名称
        list_statistics.append(self.project_name)
        # 模块名称
        list_statistics.append(module_name_change)
        # 用例总数
        list_statistics.append(sum_swagger)
        # 在soso用例数
        list_statistics.append(sum_in_soso)
        # 任务总数
        list_statistics.append(sum_out_soso)
        # 执行比例
        if sum_swagger != 0:
            list_statistics.append(str(round(sum_in_soso / sum_swagger, 4) * 100) + '%')
        else:
            list_statistics.append(0)
        return res_module, list_statistics



if __name__ == '__main__':
    project_name = '阡陌'
    data = GetSosoData()
    # # soso中所有接口
    soso_data = data.get_qianmo_cases()
    # # print(task_data)
    # url_qianmo = 'http://192.168.32.85:9600'
    url_tcm = 'http://10.11.201.106:9700'
    #
    api_doc = ReadSwaggerApiDocs(url_tcm, project_name=project_name)
    # url_resources = 'http://10.11.201.106:9700/swagger-resources'
    modules = api_doc.get_swagger_modules()
    print(modules)
    # # module = '/trade/v2/api-docs'
    # module_1 = '/uaa/v2/api-docs'
    # module_2 = '/system/v2/api-docs'
    # res_module = api_doc.get_single_module_res(module_1)
    # print(res_module)
    # res_url_list = api_doc.compare_data_and_rewrite(module=module_2, soso_data=soso_data)
    # print(res_url_list[0], '\n', res_url_list[1])
    # list_statistics = res_url_list[1]
    # res_module = res_url_list[0]
    # result = ExcelData(project_name=project_name).write_excel(list_statistics=list_statistics, res_module=res_module)
    list_statistics_all = []
    for i in range(len(modules)):
        res_url_list = api_doc.compare_data_and_rewrite(module=modules[i], soso_data=soso_data)
        list_statistics = res_url_list[1]
        res_module = res_url_list[0]
        # 将静态文件写入列表中
        list_statistics_all.append(list_statistics)
        result = ExcelData(project_name=project_name).write_json(res_module=res_module)
    statistics = ExcelData(project_name=project_name).write_excel(statistics=list_statistics_all)





    # result = ExcelData(project_name=project_name).write_excel(
    #     df_statistics=df_statistics,
    #     df_api_detail=df_api_detail,
    #     df_api_diff=df_api_diff,
    #     df_task_diff=df_task_diff,
    #     df_api_soso=soso_data)
    #








