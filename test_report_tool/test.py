# -*- coding: utf-8 -*-
# @Time : 2023/2/9 9:31
# @Author : weiliu
# @File : test.py.py
# @Software: PyCharm

# from config_ini import ConfigIni
import testlink
import pandas as pd
import requests
import urllib3
import shutil
import urllib
from redminelib import Redmine





'''
testlink_url = "http://172.16.10.108/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
api_token = '4a0bc007e7cf8d0cce57a11a5056d275'

# 连接 testlink,定义实体类
tlc = testlink.TestlinkAPIClient(testlink_url, api_token)
exec_project = "公共测试用例库"
exec_plan = "医共体测试"
test_plan_response = tlc.getTestPlanByName(exec_project, exec_plan)
print(test_plan_response[0]['id'])
test_plan_id = '64700'
# 获取接口数据
res = tlc.getTotalsForTestPlan(test_plan_id)
# result = tlc.getAllExecutionsResults(test_plan_id)
# 测试计划中总共有多少个用例
print(res['total'][0]['qty'])
# 获取测试用例
res_case = tlc.getTestCasesForTestPlan(test_plan_id)
print(res_case)

#获取测试用例集
res_case_suit = tlc.getTestSuitesForTestPlan(test_plan_id)
print(res_case_suit)
'''

# redmin_url = 'http://172.16.10.93:3000'
# redmine = Redmine(redmin_url, username='liuwei', password='ynby@123456')
# print(redmine)
# # 查询待验证task  query_id=718
# # 查询待验证 bug  query_id=719
# issue = redmine.issue.filter(query_id=718)
# print(len(issue))
# print(issue)
# print('=================分割线==========================')
# 获取project
# p1 = redmine.project.get('qianmo')
# print(p1.fixed_version)
#
# print(p1.issues[1].fixed_version)
# 根据版本进行筛选，筛选bug


print('=================分割线==========================')
'''
status_id: 状态 1:new 2:in progress 3:resolved  4:feedback  5:close 7:reopen
tracker_id：跟踪，缺陷 1:bug, 3:dev_task
fixed_version_id='阡陌3.2.6'   版本
priority_id：优先级 1-4(low,normal,high,urgent)
category_id：模块
cf_3:错误类型： string '代码错误'
'''



# issues_1 = redmine.issue.filter(project_id='qianmo', status_id='*', fixed_version_id=620, offset=0, limit=100)
# issues_1 = redmine.issue.filter(project_id='qianmo', status_id='*', tracker_id=1, fixed_version_id=620)
# print(issues_1[0].fixed_version)
# print(len(issues_1))

# issues_2 = issues_1.filter(tracker='bug', fixed_version='阡陌3.2.6')
# print(issues_2)
# # 可以判断多少个
# print(len(issues_1))
# # 遍历bug单
# for issue in issues_1:
#     # print(issue.id)
#     # print(issue.subject)
#     # print(issue.fixed_version)
#     print(issue.priority)
#     print(issue.author)
#     # 错误类型
#     print(issue.custom_fields._resources)
#     print(issue.custom_fields._resources[1]['value'])

# 如果fixed_verison = XXX 就纳入统计，统计数量

'''
def list_decorator(func):
    def wrapper(*args , **kwargs):
        data = func(*args , **kwargs)
        result = {}
        for i in set(data):
            result[i] = data.count(i)
        return result
    return wrapper

@list_decorator
def fuc():
    list_url = [1,2,2,1,4,5,5,5,5]
    return list_url
print(fuc())
'''

# P2 = redmine.project.all()
# print(P2)

'''
设计思路

1、新建一个类，登录信息
2、根据项目（project_id）来获取项目的一些issue 
3、根据筛选条件，筛选获取的时间值 
每个版本的：dev_task数据
发现缺陷数据：
status：
每个版本执行用例：数据
测试用例通过率：
'''
dic_1 = {'New': 1, 'Closed': 8, 'Resolved': 3}
dic_2 = {'Closed': 30, 'reopen': 1}
list_dic = [
        {'New': 1, 'Closed': 8, 'Resolved': 3},
        {'Closed': 30},
        {'New': 1, 'Closed': 8, 'Resolved': 3}
]

list_dic_2 = [
        {'New': 1, 'Closed': 8, 'Resolved': 3},
        {'Closed': 30},
        {'New': 1, 'Closed': 8, 'Resolved': 3}
]
all_list = []
all_list.append(list_dic)
all_list.append(list_dic_2)
print(all_list)
# # print(len(list_dic))
# for i in range(len(list_dic) - 1):
#     dic = list_dic[i+1]
#     dic_0 = list_dic[0]
#     for key, value in dic.items():
#         if key in list_dic[0]:
#             dic_0[key] += value
#         else:
#             dic_0[key] = value
# print(list_dic[0])