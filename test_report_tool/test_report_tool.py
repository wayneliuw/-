# -*- coding: utf-8 -*-
# @Time : 2023/2/7 9:30
# @Author : weiliu
# @File : test_report_tool.py.py
# @Software: PyCharm


from config_ini import ConfigIni
# import testlink
# import pandas as pd
# import requests
# import urllib3
# import shutil
# import urllib
from redminelib import Redmine
import time

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
'''
status_id: 状态 1:new 2:in progress 3:resolved  4:feedback  5:close 7:reopen
tracker_id：跟踪，缺陷 1:bug, 4:dev_task
fixed_version_id='阡陌3.2.6'   版本
priority_id：优先级 1-4(low,normal,high,urgent)
category_id：模块
cf_3:错误类型： string '代码错误'
'''


class RedmineReportGet:

    def __init__(self):
        '''
        初始化redmine
        '''
        cf = ConfigIni()
        self.username = cf.get_key('redmine', 'username')
        self.password = cf.get_key('redmine', 'password')
        self.url = cf.get_key('redmine', 'url')
        try:
            self.redmine = Redmine(self.url, username=self.username, password=self.password)
        except Exception as e:
            raise RuntimeError(f'无法连接到Redmine，请检查网络！{e}')

    def list_decorator(func):
        '''
        写个装饰器，就是将函数的返回结果按照每个类别列出来
        获取list中对应元素出现的的次数
        :return:
        '''
        def wrapper(*args , **kwargs):
            data = func(*args, **kwargs)
            result = {}
            for i in set(data):
                result[i] = data.count(i)
            return result
        return wrapper

    def get_issue_bug(self , project, fixed_version_id):
        '''
        根据项目和版本获取bug情况
        :param project:
        :param fixed_version_id:
        :return:
        '''
        tracker_id = 1
        project = project
        fixed_version_id = fixed_version_id
        isssu_bug = self.redmine.issue.filter(project_id=project,
                                              tracker_id=tracker_id,
                                              status_id='*',
                                              fixed_version_id=fixed_version_id)
        bug_num = len(isssu_bug)
        fixed_version_id_name = isssu_bug[0].fixed_version
        return isssu_bug, bug_num,  fixed_version_id_name

    def get_issue_task(self , project , fixed_version_id):
        '''
        获取task数据
        :param project:
        :param fixed_version_id:
        :return:
        '''
        tracker_id = 4
        project = project
        fixed_version_id = fixed_version_id
        isssu_task = self.redmine.issue.filter(project_id=project,
                                              tracker_id=tracker_id,
                                               status_id='*',
                                              fixed_version_id=fixed_version_id)
        task_num = len(isssu_task)
        return task_num

    @list_decorator
    def get_issue_priority(self, project, fixed_version_id):
        '''
        获取缺陷的优先级
        :return:
        '''
        res = self.get_issue_bug(project=project , fixed_version_id=fixed_version_id)
        bug_issue = res[0]
        # 定义缺陷优先级的list
        priority_list = []
        for issue in bug_issue:
            priority = issue.priority.name
            priority_list.append(priority)
        return priority_list

    @list_decorator
    def get_issue_category(self, project, fixed_version_id):
        '''
        获取缺陷属于哪个模块的
        :param project:
        :param fixed_version_id:
        :return:
        '''
        res = self.get_issue_bug(project=project, fixed_version_id=fixed_version_id)
        bug_issue = res[0]
        # 定义缺陷属于哪个模块的list
        category_list = []
        for issue in bug_issue:
            category = issue.category.name
            category_list.append(category)
        return category_list

    @list_decorator
    def get_issue_wrong_type(self, project, fixed_version_id):
        '''
        获取缺陷类型
        :param project:
        :param fixed_version_id:
        :return:
        '''
        res = self.get_issue_bug(project=project, fixed_version_id=fixed_version_id)
        bug_issue = res[0]
        # 定义缺陷属于哪个类型的list
        wrong_type_list = []
        for issue in bug_issue:
            wrong_type = issue.custom_fields._resources[1]['value']
            wrong_type_list.append(wrong_type)
        return wrong_type_list

    @list_decorator
    def get_issue_status(self, project, fixed_version_id):
        '''
        获取缺陷状态
        :param project:
        :param fixed_version_id:
        :return:
        '''
        res = self.get_issue_bug(project=project, fixed_version_id=fixed_version_id)
        bug_issue = res[0]
        # 定义缺陷属于哪个类型的list
        status_list = []
        for issue in bug_issue:
            status = issue.status.name
            status_list.append(status)
        return status_list

    def get_all_bug(self):
        project = ConfigIni().get_key('redmine', 'project')
        fixed_version_id = ConfigIni().get_key('redmine' , 'fixed_version_id')
        fixed_version_id = fixed_version_id.split(',')
        bug_priority_list = []
        bug_wrong_type_list = []
        bug_category_list = []
        # 获取各个模块的数据
        for i in range(len(fixed_version_id)):
            bug_num = self.get_issue_bug(project=project, fixed_version_id=fixed_version_id[i])
            print(f'=========版本:{bug_num[2]},版本id:{fixed_version_id[i]}:分割线===============')
            print(f'{bug_num[2]}版本缺陷数据:{bug_num[1]}')
            task_num = self.get_issue_task(project=project, fixed_version_id=fixed_version_id[i])
            print(f'{bug_num[2]}版本dev_task数据:{task_num}')
            bug_priority = self.get_issue_priority(project=project, fixed_version_id=fixed_version_id[i])
            print(f'{bug_num[2]}版本缺陷优先级数据:{bug_priority}')
            bug_priority_list.append(bug_priority)
            bug_wrong_type = self.get_issue_wrong_type(project=project, fixed_version_id=fixed_version_id[i])
            print(f'{bug_num[2]}版本缺陷错误类型数据:{bug_wrong_type}')
            bug_wrong_type_list.append(bug_wrong_type)
            bug_category = self.get_issue_category(project=project, fixed_version_id=fixed_version_id[i])
            print(f'{bug_num[2]}版本缺陷错误类型数据:{bug_category}')
            bug_category_list.append(bug_category)
            bug_status = self.get_issue_status(project=project, fixed_version_id=fixed_version_id[i])
            print(f'{bug_num[2]}版本缺陷错误类型数据:{bug_status}')
        # 获取总数据
        print("\n当前月度版本的总缺陷数据为：")
        bug_all_list = []
        bug_all_list.append(bug_priority_list)
        bug_all_list.append(bug_wrong_type_list)
        bug_all_list.append(bug_category_list)
        for i in range(len(bug_all_list)):
            for j in range(len(bug_all_list[i]) - 1):
                dic_0 = bug_all_list[i][0]
                dic_1 = bug_all_list[i][j+1]
                for key, value in dic_1.items():
                    if key in dic_0:
                        dic_0[key] += value
                    else:
                        dic_0[key] = value
            print(f'数据为：{bug_all_list[i][0]}')


if __name__ == '__main__':
    redmine = RedmineReportGet()
    print("开始获取项目数据=============")
    res = redmine.get_all_bug()
    while True:
        print('0.结束程序')
        number = int(input())
        if number == 0:
            exit()








