# -*- coding: utf-8 -*-
# @Time : 2023/2/2 13:16
# @Author : weiliu
# @File : test.py.py
# @Software: PyCharm

import requests
import json
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                         '/107.0.0.0 Safari/537.36',
               'Content-Type': 'application/json'}
login_url = 'http://192.168.32.30:3000/api/user/login'
login_data = {"email":"hehuiling@ynby.cn", "password":"123456"}
login_response = requests.post(url=login_url, json=login_data , headers=headers , allow_redirects=False)

res_head = login_response.headers['Set-Cookie']
_yapi_token = re.findall("_yapi_token=(.+?);" , res_head)
_yapi_uid = re.findall("_yapi_uid=(.+?);" , res_head)
HEADERS = {
    'content-type': 'application/json;charset=UTF-8' ,
    'Cookie': '_yapi_token=' + _yapi_token[0] + ';_yapi_uid=' + _yapi_uid[0]
}

url = 'http://10.11.201.106:9700/tcm-order/v2/api-docs'
url_1 = 'http://192.168.32.85:9600/trade/v2/api-docs'
url_2 = 'http://192.168.32.30:3000/api/plugin/exportSwagger?type=OpenAPIV2&pid=36&status=all&isWiki=false'
token = '464c943064ec8d3a974307b6ea06622728d99c18c7023f5a6272d7662bce0fe7'
url_3 = 'http://192.168.32.30:3000/api/interface/list?page=1&limit=999999&token=' + token
res = requests.get(url=url, headers=HEADERS)
res_2 = requests.get(url=url_2, headers=HEADERS)
print('----fengexian----','\n')
res2_url_dic = res_2.json()['paths']
print(res2_url_dic)

# 获取key值
swagger_url_list = list(res2_url_dic.keys())

'''
在这里需要写一个方法来处理

1、接口名字是一样的，但是可能存在两个方式，就是
   post 和 put 这可能就是两个接口
   但是swagger中可能是一个接口
   
2、如果存在就剔除了，两个都会加入

'''
request_method = ['post','get','head','option','put','move']
son_dic_key_list = []
for i in range(len(swagger_url_list)):
    print(swagger_url_list[i])
    dic_son = res2_url_dic[swagger_url_list[i]]
    print(len(list(dic_son.keys())))
    print(dic_son)
    # son_dic_key_list = list(res2_url_dic[swagger_url_list[i]].keys())
    # print(son_dic_key_list)

    # # 查看子字典，如果子字典中有超过两个key就加上
    #     son_dic = res2_url_dic[swagger_url_list[i]].keys(
print('----fengexian----','\n')
# swagger_url_list = list(res2_url_dic.keys())
'''
'/nursingPlanDevice': {
			'post': {
				'tags': ['方案管理-方案设备'],
				'summary': '保存方案设备',
				'description': '保存方案设备',
				'consumes': ['application/json'],
				'parameters': [{
					'name': 'root',
					'in': 'body',
					'schema': {
						'type': 'object',
						'properties': {
							'sysDictDeviceId': {
								'type': 'integer',
								'description': '数据字典中设备类型的id'
							},
							'picUrl': {
								'type': 'string',
								'description': '设备图片地址'
							},
							'status': {
								'type': 'integer',
								'description': '状态(0:禁止,1:正常)'
							}
						},
						'required': ['sysDictDeviceId', 'picUrl', 'status'],
						'$schema': 'http://json-schema.org/draft-04/schema#'
					}
				}],
				'responses': {
					'200': {
						'description': 'successful operation',
						'schema': {
							'type': 'object',
							'properties': {
								'code': {
									'type': 'integer',
									'description': '响应码'
								},
								'msg': {
									'type': 'string',
									'description': '提示信息'
								},
								'data': {
									'type': 'object',
									'properties': {},
									'description': '响应的消息体'
								}
							},
							'$schema': 'http://json-schema.org/draft-04/schema#',
							'description': ''
						}
					}
				}
			},
			'put': {
				'tags': ['方案管理-方案设备'],
				'summary': '修改设备方案',
				'description': '修改设备方案',
				'consumes': ['application/json'],
				'parameters': [{
					'name': 'root',
					'in': 'body',
					'schema': {
						'type': 'object',
						'properties': {
							'id': {
								'type': 'integer',
								'description': '主键id'
							},
							'sysDictDeviceId': {
								'type': 'integer',
								'description': '数据字典中设备类型的id'
							},
							'picUrl': {
								'type': 'string',
								'description': '设备图片地址'
							},
							'status': {
								'type': 'integer',
								'description': '状态(0:禁止,1:正常)'
							}
						},
						'required': ['id', 'sysDictDeviceId', 'picUrl', 'status'],
						'$schema': 'http://json-schema.org/draft-04/schema#'
					}
				}],
				'responses': {
					'200': {
						'description': 'successful operation',
						'schema': {
							'type': 'object',
							'properties': {
								'code': {
									'type': 'integer',
									'description': '响应码'
								},
								'msg': {
									'type': 'string',
									'description': '提示信息'
								},
								'data': {
									'type': 'object',
									'properties': {},
									'description': '响应的消息体'
								}
							},
							'$schema': 'http://json-schema.org/draft-04/schema#',
							'description': ''
						}
					}
				}
			}
		},
'''






# print(type(res.text))
# print('----fengexian----','\n')
# res = res.json()
# print(res)
#
# print('----fengexian----','\n')
# url_dic = res['paths']
#
# basepath = res['basePath']
# basepath = basepath.replace('/','_')
# print(basepath)
# res['info']['title'] = 'trade模块'
# # print(res)
# # print(url_dic)
#
# print('----fengexian----','\n')
# # 返回字典中的list
# url_swagger_list = url_dic.keys()
# print(list(url_swagger_list))
# print('----fengexian----','\n')
# list_soso = ['/pay/micropay/{communityHospitalId}','/pay/query/{communityHospitalCode}']
# for i in range(len(list_soso)):
#     if list_soso[i] in url_swagger_list:
#         # 删除字典该条目
#         del url_dic[list_soso[i]]
# print(url_dic)
# print('----fengexian----','\n')
# res['path'] = url_dic
# print(res)
# # 将文件存为json文件
# with open('trade.json', 'w') as f:
#
#     json.dump(res, f)

