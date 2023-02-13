## test_report_tool简介
    本项目主要目的是根据项目的名称和版本号，获取对应项目的缺陷数据和dev_task数据，
    对于同一个项目的的多个数据能够多个版本的缺陷数据，并返回汇总的数据，以供大家填写阅读报告
### 使用方法
1. 获取项目的名称和版本编号登录到remine上根据下图所示去找项目对应的名称
       
    ![](https://pic.imgdb.cn/item/63e5b4d24757feff33918462.png)
2. 获取项目的版本编号
    ![](https://pic.imgdb.cn/item/63e5b6c74757feff3394301f.png)
3. 在项目config.ini中输入对应的项目和编号
    ![](https://pic.imgdb.cn/item/63e5bc074757feff339bf06d.png)
4. 设置完成后就可以运行查看结果了

### 依赖的安装包

1. pip install python-redmine -i https://pypi.tuna.tsinghua.edu.cn/simple
2. pip install configparser -i https://pypi.tuna.tsinghua.edu.cn/simple
或者
1. pip install python-redmine -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
2. pip install configparser -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com


