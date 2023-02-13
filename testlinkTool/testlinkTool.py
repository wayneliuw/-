# -*- coding: utf-8 -*-
# @Time : 2022/7/05 18:17
# @Author : weiliu
# @File : testlinkTool.py
# @Software: PyCharm
import traceback

import xlrd3 as xlrd
import tkinter as tk
from testlink import *
from dataclasses import dataclass
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showwarning, showinfo
from os.path import exists
from os import walk

ACTIVE = 1
PUBLIC = 1
VERSION = 1
OPEN = 1
win = tk.Tk()

# plan_id = tk.StringVar()      # 测试计划ID
case_list = []    # 测试用例ID集

@dataclass
class ClientTestLink:
    """
    http://47.104.12.106:8080/testlink/lib/api/xmlrpc/v1/xmlrpc.php
    """
    user_api_pwd: str
    client_url: str = "http://172.16.10.108/testlink/lib/api/xmlrpc/v1/xmlrpc.php"

    def __post_init__(self):
        # 获取域名和地址
        self.tlc = TestlinkAPIClient(self.client_url, self.user_api_pwd)

    def get_projects(self):
        """获取testLink内所有项目"""
        project_list = []
        for project in self.tlc.getProjects():
            project_list.append([project.get("id"), project.get("name")])
        return project_list

    def get_project_id_by_name(self, project_name):
        """获取项目id根据项目名称"""
        return self.tlc.getProjectIDByName(project_name)

    def get_test_suites(self, project_id):
        """获取指定项目里(需要项目id)的测试用例集"""
        test_suite_list = []
        test_suites = self.tlc.getFirstLevelTestSuitesForTestProject(project_id)
        for test_suite in test_suites:
            test_suite_list.append([test_suite.get("id"), test_suite.get("name")])
        return test_suite_list

    def get_test_suite_id(self, project_id, test_suite_name):
        """查询一级目录"""
        all_suites = self.get_test_suites(project_id)
        for i in all_suites:
            if i[1] == test_suite_name:
                return i[0]
            else:
                pass
        return False

    def get_test_suite_for_test_suite(self, test_suite_id):
        """查询用例集下是否含有某用例集"""
        try:
            test_suite_id = self.tlc.getTestSuitesForTestSuite(test_suite_id)
            return test_suite_id
        except Exception:
            return False

    def create_test_suite(self, project_id: int, test_suite_name: str, parent_id: int = None):
        """判断是否拥有测试用例集，如果没有就创建测试用例集"""
        suite_data = self.tlc.createTestSuite(project_id, test_suite_name, test_suite_name, parentid=parent_id)
        cheak_bool = isinstance(suite_data, list)  # 是否存在数据,存在就返回testsuitid
        if cheak_bool:
            return suite_data[0].get("id")       # 如果存在就返回获取的id
        else:
            if parent_id is None:
                return self.get_test_suite_id(project_id=project_id, test_suite_name=test_suite_name)
            else:
                for k, v in self.get_test_suite_for_test_suite(parent_id).items():
                    if isinstance(v, dict):
                        if v.get("name") == test_suite_name:
                            return v.get("id")
                        else:
                            pass
                    else:
                        return self.get_test_suite_for_test_suite(parent_id).get("id")

    def create_test_case(self, project_id: int, test_suite_id: int, test_case_name, summary,  preconditions,
                         step, result, importance,  author_login):
        """创建测试用例"""
        self.tlc.initStep(step, result, 1)
        return self.tlc.createTestCase(testprojectid=project_id,
                                       testsuiteid=test_suite_id,
                                       testcasename=test_case_name,
                                       summary=summary,
                                       preconditions=preconditions,
                                       importance=importance,    # 重要性
                                       authorlogin=author_login
                                       )

    def update_project_keywords(self, project_id, test_case_id, keyword_value):
        """加关键字"""
        test_case = self.tlc.getTestCase(testcaseid=test_case_id)[0]
        args = {
            'testprojectid': project_id,
            'testcaseexternalid': test_case['full_tc_external_id'],
            'version': int(test_case['version'])
        }
        keyword = self.tlc.addTestCaseKeywords({args['testcaseexternalid']: [keyword_value]})
        keyword = None if not keyword_value else keyword
        print(f"上传的关键字为:{keyword}")
        return keyword

    # 创建测试计划
    def create_test_plan(self, project_name, test_plan_name, active, public):
        try:
            test_plan = self.tlc.createTestPlan(testprojectname=project_name, testplanname=test_plan_name, active=active, public=public)
            test_plan_id = test_plan[0]['id']
            return test_plan_id
        except Exception:
            return False

    # 将测试用例加入测试计划
    def add_test_case_to_test_plan(self, project_id, test_plan_id, test_case_id, version):
        if test_case_id:
            add_case = self.tlc.addTestCaseToTestPlan(testprojectid=project_id, testplanid=test_plan_id, testcaseexternalid=test_case_id, version=version)
            feature_id = add_case['feature_id']
            return feature_id
        else:
            print("暂无测试用例")


def get_all_case_num(excel_file_name):
    """统计有多少条用例"""
    datacases = xlrd.open_workbook(excel_file_name)
    sheets = datacases.sheet_names()
    total_num = 0
    for sheet in sheets:   # sheet中有多少条用例
        sheet_1 = datacases.sheet_by_name(sheet)
        row_num = sheet_1.nrows
        total_num += row_num - 1
    return total_num


def run_root(excel_file_name, project_id, username, api_token):
    """
    创建用例
    """
    global case_list      # 获取所有testcaseID
    case_num = get_all_case_num(excel_file_name)     # 总共多少条用例
    win2 = tk.Tk()
    # 设置标题
    win2.title("导入任务")
    # 设置大小和位置
    win2.geometry("220x100")
    win.iconbitmap(r"img/ynby.ico")
    # 禁止改变窗口大小
    win2.resizable(0, 0)
    # 进度条
    mpb = ttk.Progressbar(win2, orient="horizontal", length=150, mode="determinate")
    mpb.place(x="10", y="10")
    mpb["maximum"] = case_num
    mpb["value"] = 0
    upload_label = tk.Label(win2, text='正在导入用例...(切勿关闭)', fg='red')
    upload_label.place(x="10", y="40")
    upload_label_text = tk.Label(win2, text='', fg='red')
    upload_label_text.place(x="160", y="40")
    upload_per_label = tk.Label(win2, text='', fg='red')
    upload_per_label.place(x="160", y="10")
    # 读取excel，获取数据
    datacases = xlrd.open_workbook(excel_file_name)

    sheets = datacases.sheet_names()

    for sheet in sheets:
        sheet_1 = datacases.sheet_by_name(sheet)

        # ====================测试用例功能模块==============================

        row_num = sheet_1.nrows
        for i in range(1, row_num):
            # 定义默认步骤编号第一步
            catalog_1 = sheet_1.cell_value(i, 0)  # 一级目录
            catalog_2 = sheet_1.cell_value(i, 1)  # 二级目录
            catalog_3 = sheet_1.cell_value(i, 2)  # 三级目录，三级目录可以不用
            test_case_name = sheet_1.cell_value(i, 3)  # 用例名称
            summary = sheet_1.cell_value(i, 4)  # 摘要
            key_words = sheet_1.cell_value(i, 5)  # 关键字，可以不用
            test_case_level = sheet_1.cell_value(i, 6)  # 用例级别
            preconditions = sheet_1.cell_value(i, 7)  # 预置条件
            preconditions_list = []
            for i_preconditions in preconditions.split('\n'):
                preconditions_list.append("<p>" + i_preconditions + "</p>")
            preconditions = ''.join(preconditions_list)

            step = sheet_1.cell_value(i, 8)  # 操作步骤
            step_list = []
            # importance = ''
            # 处理换行，换行符号分割
            for i_step in step.split('\n'):
                step_list.append("<p>" + i_step + "</p>")
            step = ''.join(step_list)
            expected_results = sheet_1.cell_value(i, 9)  # 预期结果
            expected_results_list = []
            # 处理换行
            for i_expected_results in expected_results.split('\n'):
                expected_results_list.append("<p>" + i_expected_results + "</p>")
            expected_results = ''.join(expected_results_list)
            # 将优先级转换为字典
            if (test_case_level == "" or test_case_level == None):
                print(u"格式错误, 第%s行, \"优先级\"列, 不能为空!" % row_num)
                return None
            else:
                importance_value = test_case_level.strip()
                importance_value = importance_value.capitalize()  # 首字母大写
                if (importance_value == "Medium" or importance_value == "M"):
                    importance = "2"
                elif (importance_value == "High" or importance_value == "H"):
                    importance = "3"
                elif (importance_value == "Low" or importance_value == "L"):
                    importance = "1"
            # 结束转换
            try:
                # 创建一级目录
                test_suite_id = ClientTestLink(api_token).create_test_suite(project_id=project_id,
                                                                            test_suite_name=catalog_1)
                # 创建二级目录
                if catalog_2:
                    test_suite_id = ClientTestLink(api_token).create_test_suite(project_id=project_id,
                                                                                test_suite_name=catalog_2,
                                                                                parent_id=test_suite_id)
                    # 创建三级目录
                    if catalog_3:
                        test_suite_id = ClientTestLink(api_token).create_test_suite(project_id=project_id,
                                                                                    test_suite_name=catalog_3,
                                                                                    parent_id=test_suite_id)

                result = ClientTestLink(api_token).create_test_case(
                    project_id=project_id,
                    test_suite_id=test_suite_id,
                    test_case_name=test_case_name,
                    summary=summary,
                    preconditions=preconditions,
                    importance=importance,
                    step=step,
                    result=expected_results,
                    author_login=username)

                # 获取用例ID
                test_case_id = result[0].get("id")

                # 添加关键字，如果不在关键词
                if not key_words:
                    key_words = "功能测试"
                ClientTestLink(api_token).update_project_keywords(project_id=project_id,
                                                                  test_case_id=test_case_id,
                                                                  keyword_value=key_words)

                print(f"上传的关键字为{key_words}")
                mpb["value"] = i
                # 更新进度
                upload_label_text.config(text=f"<{i}/{case_num}>")
                upload_per_label.config(text=f"{((i / case_num) * 100):.2f}%")
                win.update()
                case_list.append(test_case_id)
                print(f"{test_case_id}-上传用例成功")
            except Exception as e:
                with open('log.txt', 'a+', encoding='utf-8') as fp:
                    fp.write(traceback.format_exc())
                raise Exception(e)

    try:
        win2.destroy()
    except:
        pass



#  导入测试用例时弹出的窗口
def run_case(case_list, project_id, test_plan, api_token):
    """
    创建用例
    """
    case_id = case_list
    print(case_id)
    case_plan_num = len(case_id)     # 总共多少条用例
    print(case_plan_num)
    win2 = tk.Tk()
    # 设置标题
    win2.title("导入测试用例到测试计划")
    # 设置大小和位置
    win2.geometry("220x100")
    win.iconbitmap(r"img/ynby.ico")
    # 禁止改变窗口大小
    win2.resizable(0, 0)
    # 进度条
    mpb = ttk.Progressbar(win2, orient="horizontal", length=150, mode="determinate")
    mpb.place(x="10", y="10")
    mpb["maximum"] = case_plan_num
    mpb["value"] = 0
    upload_label = tk.Label(win2, text='正在导入用例到测试计划...(切勿关闭)', fg='red')
    upload_label.place(x="10", y="40")
    upload_label_text = tk.Label(win2, text='', fg='red')
    upload_label_text.place(x="160", y="40")
    upload_per_label = tk.Label(win2, text='', fg='red')
    upload_per_label.place(x="160", y="10")
    project_id = ClientTestLink(api_token).tlc.getProjectIDByName(projectName=project_id)
    # case_id中的数据，需要获得case的testcaseexternalid，获取数据
    try:
        for i in range(case_plan_num):
            test_case = ClientTestLink(api_token).tlc.getTestCase(testcaseid=case_id[i])[0]    # 获取测试用例信息
            test_case_external_id = test_case['full_tc_external_id']             # 获取测试用例externalid
            print(test_case_external_id)
            case_feature_id = ClientTestLink(api_token).add_test_case_to_test_plan(project_id=project_id, test_plan_id=test_plan, test_case_id=test_case_external_id, version=VERSION)
            mpb["value"] = i
            # 更新进度
            upload_label_text.config(text=f"<{i}/{case_plan_num}>")
            upload_per_label.config(text=f"{((i / case_plan_num) * 100):.2f}%")
            win.update()
            print("添加用例到测试计划成功,feature_id为{}".format(case_feature_id))
    except Exception as e:
        with open('log.txt', 'a+', encoding='utf-8') as fp:
            fp.write(traceback.format_exc())
        raise Exception(e)

    try:
        win2.destroy()
    except:
        pass


def file_name(file_path, excel_dir):
    for root, dirs, files in walk(excel_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files)  # 当前路径下所有非目录子文件
        files_list = []
        for file in enumerate(files):   # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标
            hz = file[1].split('.')[-1]    # 文件名字
            if hz == "xlsx" or hz == "xls":
                files_list.append(file_path + file[1])
            else:
                pass
        return files_list


def select_excel_file_path():
    path_file = askopenfilename()
    excel_file_str.set(path_file)
    return path_file


def export_excel():
    # pattern = r.get()
    excel_file_path = excel_file_str.get()
    project_name = com.get()
    api = api_str.get()
    username = username_str.get()
    if excel_file_path == "":
        showwarning("警告", "请传入excel文件路径")
        return False
    else:
        if exists(excel_file_path):
            if project_name in get_project_list():
                pass
            else:
                showwarning("错误", "项目名不存在,请检查")
                return False
        else:
            showwarning("错误", "导入的excel的目录或文件不存在！")
            return False
    # 尝试导入
    try:
        run_root(excel_file_name=excel_file_path,
                 project_id=ClientTestLink(api).get_project_id_by_name(project_name),
                 api_token=api,
                 username=username)
        showinfo("成功", "导入成功！")
    except Exception as e:
        print(e)
        showwarning("失败", "导入失败！请联系管理员")
        return False

#  新建测试计划
def create_plan():
    # global test_plan
    api = api_str.get()
    project_name = com.get()
    plan_name = plan_str.get()

    if plan_name == "":
        showwarning("警告", "请输入测试计划名称")
        return False
    else:
        try:
            test_plan_id = ClientTestLink(api).create_test_plan(
                project_name=project_name,
                test_plan_name=plan_name,
                active=ACTIVE, public=PUBLIC)
            if test_plan_id:
                showinfo("成功", "新建成功，测试计划ID为：{}".format(test_plan_id))
            else:
                showinfo("失败", "测试计划ID重复")
            plan_id.set(test_plan_id)
            return True
        except Exception:
            showinfo("警告", "新建测试计划失败")



# 新建测试build
def create_build():
    # global test_plan
    api = api_str.get()
    # project_name = com.get()
    test_plan = test_plan_text.get()
    build_name = build_str.get()

    if build_name == "":
        showwarning("警告", "请输入测试build名称")
        return False
    else:
        try:
            test_build_id = ClientTestLink(api).tlc.createBuild(
                testplanid=test_plan,
                buildname=build_name,
                active=ACTIVE,
                open=OPEN
            )
            if test_build_id[0]['status']:
                showinfo("成功", "新建成功，buildID为:{}".format(test_build_id[0]['id']))
            else:
                showinfo("失败", "新建失败，message为:{}".format(test_build_id[0]['message']))
            return True
        except Exception:
            showinfo("警告", "新建测试build失败")


# 将测试用例导入测试计划
def add_case_to_plan():
    test_plan = test_plan_text.get()
    api = api_str.get()
    print(case_list)
    project_name = com.get()
    try:
        if test_plan == '':
            showinfo("失败", "没有找到测试计划")
        elif case_list == []:
            showinfo("失败", "没有找到测试用例")
        else:
            run_case(
                case_list=case_list,
                project_id=project_name,
                test_plan=test_plan,
                api_token=api,
            )
            showinfo("成功", "导入成功！")
    except Exception as e:
        print(e)
        showwarning("失败", "导入失败！请联系管理员")




def refresh():
    api = api_str.get()
    value_list = ClientTestLink(api).get_projects()
    new_list = []
    for i in value_list:
        new_list.append(i[1])
    com["value"] = new_list
    showwarning("成功", "刷新成功")
    return new_list


def use_fuc():
    showinfo("使用说明",
             "1.工具目录下必须有api_token.txt\n"
             "2.文件里第一行填写api连接token,第二行填写登录用户名(请务必填写准确)\n"
             "3.步骤和预期结果想要换行请在excel中用回车换行即可\n"
             "4.excel用例里优先级不填写默认为高,关键字不填写默认为功能测试\n")

def about_tool():
    showinfo(
        "关于",
        "Copyright © YNBY.All Rights Reserved.\n"
        "Author: wayne liu\n"
    )


def set_id_label_stats():
    """
    设置子目录是否展示，如果是0就不展示子目录
    disabled, normal, readonly
    :return:
    """
    res = r.get()
    if res == 1:
        id_label_entry['state'] = 'normal'
    else:
        id_label_entry['state'] = 'disabled'
        id_str.set('')


def get_project_list():
    value_list = ClientTestLink(api_str.get()).get_projects()
    new_list = []
    for i in value_list:
        new_list.append(i[1])
    return new_list


def run_main():
    global id_str, excel_file_str, r, win, id_label_entry, com, api_str, username_str, importance, plan_str, plan_id, test_plan_text, build_str



    # win = tk.Tk()
    # 设置标题
    win.title("TestLinkTool v1.0")
    # 设置大小和位置
    win.geometry("500x400+300+300")
    # 禁止改变窗口大小
    win.resizable(100,100)

    # 设置图标
    win.iconbitmap(r"img/ynby.ico")


    # 输入框变量
    # excel路径
    excel_file_str = tk.StringVar()
    id_str = tk.StringVar()
    api_str = tk.StringVar()
    plan_id = tk.StringVar()  # 测试计划ID
    username_str = tk.StringVar()
    with open('api_token.txt', 'r') as fp:
        res = fp.readlines()
    api_str.set(res[0].replace('\n', ''))
    username_str.set(res[1])
    # 绑定变量，一组单选框要绑定同一个变量，就能区分出单选框了
    r = tk.IntVar()
    r.set(1)

    # 进入消息循环，可以写控件
    # 创建一个菜单选项
    # 菜单条
    menubar = tk.Menu(win)
    win.config(menu=menubar)
    menu1 = tk.Menu(win, tearoff=False)
    # 给菜单选项添加内容
    for item in ['使用说明', '关于TeslinkTool', '退出']:
        if item == '退出':
            # 添加分割线
            menu1.add_separator()
            menu1.add_command(label=item, command=win.quit)
        elif item == '使用说明':
            menu1.add_command(label=item, command=use_fuc)
        elif item == '关于TeslinkTool':
            menu1.add_command(label=item, command=about_tool)

    # 向菜单条上添加菜单选项
    menubar.add_cascade(label='功能菜单', menu=menu1)
    # =======================================================
    to_test_link_project_label = tk.Label(win,
                                          text="导入项目选择：",
                                          font=("黑体", 12))
    to_test_link_project_label.place(x='20', y='40')

    cv = tk.StringVar()

    com = ttk.Combobox(win, textvariable=cv)

    com.place(x='20', y='70')

    # 设置下拉数据

    com["value"] = get_project_list()

    # 设置默认值
    com.current(0)

    # 绑定事件
    def func(event):
        print(com.get())

    print(cv.get())

    com.bind("<<ComboboxSelected>>", func)

    # =======================================================
    excel_file_path_label = tk.Label(win,
                                     text="导入excel文件路径：",
                                     font=("黑体", 12))
    excel_file_path_label.place(x='230', y='10')

    excel_file_entry = tk.Entry(win, textvariable=excel_file_str)
    excel_file_entry.place(x='235', y='40', width='240')

    excel_file_path_btn = tk.Button(win, text="设置", command=select_excel_file_path)
    excel_file_path_btn.place(x='445', y='5')

    # =======================================================

    api_label = tk.Label(win,
                         text="api_token：",
                         font=("黑体", 12), )
    api_label.place(x='230', y='200')

    api_label_entry = tk.Entry(win, textvariable=api_str, state="readonly")
    api_label_entry.place(x='235', y='230', width='240')

    # =======================================================

    username_label = tk.Label(win,
                              text="登录用户名：",
                              font=("黑体", 12), )
    username_label.place(x='230', y='270')

    username_label_entry = tk.Entry(win, textvariable=username_str, state="readonly")
    username_label_entry.place(x='235', y='300', width='240')

    # =======================================================
    radio1 = tk.Radiobutton(win, text="从根目录导入用例", value=1, variable=r, command=set_id_label_stats)

    radio1.place(x='20', y='10')

    # ========================================================

    export_btn = tk.Button(win, text="导入", command=export_excel)
    export_btn.place(x='20', y='110', width='80', height='40')

    # ========================================================
    export_btn = tk.Button(win, text="刷新", command=refresh)
    export_btn.place(x='120', y='110', width='80', height='40')

    # ===========================================
    # 创建测试计划
    create_plan_label = tk.Label(
        win,
        text="新建测试计划：",
        font=("黑体", 12), )
    create_plan_label.place(x='20', y='160')

    plan_text = tk.StringVar()
    plan_str = ttk.Entry(win, textvariable=plan_text)
    plan_str.place(x='20', y='180', width='120', height='30')

    create_plan_btn = tk.Button(win, text="新建", command=create_plan)
    create_plan_btn.place(x='150', y='180', width='50', height='30')

    # ===========================================
    #  新建测试build
    # ===========================================
    create_build_label = tk.Label(
        win,
        text="新建build版本号：",
        font=("黑体", 12), )
    create_build_label.place(x='20', y='220')

    build_text = tk.StringVar()
    build_str = ttk.Entry(win, textvariable=build_text)
    build_str.place(x='20', y='240', width='120', height='30')

    create_plan_btn = tk.Button(win, text="新建", command=create_build)
    create_plan_btn.place(x='150', y='240', width='50', height='30')

    # ===========================================

    # ===========================================
    # 添加测试计划到测试用例
    case_to_plan_label = tk.Label(
        win,
        text="添加测试用例到测试计划：",
        font=("黑体", 12), )
    case_to_plan_label.place(x='20', y='280')

    add_btn = tk.Button(win, text="添加", command=add_case_to_plan)
    add_btn.place(x='20', y='310', width='80', height='40')

    # ========================================================
    add_btn = tk.Button(win, text="刷新", command=refresh)
    add_btn.place(x='120', y='310', width='80', height='40')
    # ===========================================
    #  测试计划ID
    # ===========================================
    # # 添加测试计划到测试用例
    test_plan_label = tk.Label(
        win,
        text="测试计划id",
        font=("黑体", 12), )
    test_plan_label.place(x='230', y='90')
    test_plan_text = ttk.Entry(win, textvariable=plan_id, state="readonly")
    test_plan_text.place(x='230', y='110', width='50', height='20')


    win.mainloop()


if __name__ == '__main__':

    run_main()
