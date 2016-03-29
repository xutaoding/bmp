OPS 后台程序
===========================
前后端程序是分离的，对应的前端代码git@gitlab.chinascope.net:web/ops.git
后端程序是基于flask的实现,数据接口使用json格式



环境
-----------------------------------
前端代码:git@gitlab.chinascope.net:web/ops.git

依赖:
    apache(正式环境使用),
    nginx(测试环境使用)
    python-wsgi python-ldap flask-*(flask相关库) python 2.7

正式环境:
    后台:192.168.250.10/var/www/scope/bmp
    前端:192.168.250.10/app/www/ops/static
    数据库:mysql://192.168.250.10:3306/bmp
    
测试环境:
    后台:192.168.0.227/var/www/scope/bmp
    前端:192.168.0.227/app/www/ops/static
    数据库:mysql://192.168.250.10:3306/bmp_test

目录结构描述
-----------------------------------
### runserver.py 
    程序入口
    
    
### bmp/apis
    接口程序的根目录,myapp.py中的add_api_rule函数为接口的初始化
    接口定义规则:
        1.每个py文件对应一个接口,文件名与接口类名相同
            例 upload.py  对应类名 UploadApi 类名首字母大写
        2.接口类需要定义变量router(参考现有实现),route规则参见flask文档
        
### bmp/apis/asset
    资产管理相关接口
### bmp/apis/user
    用户相关接口
### bmp/apis/workflow
    流程审批相关接口 
### bmp/apis/api.txt
    接口调用的简要描述
### bmp/apis/refs.py
    一些基础字段定义
### bmp/apis/upload.py
    上传文件的接口
        
### bmp/models
    数据接口实现
    数据接口实现基于 flask-sqlalchemy库
    
### bmp/tasks
    同异步任务相关

### bmp/upload
    上传文件的存放目录（正式环境需要链接存储集群)
    
### bmp/signals
    flask信号相关任务
    
### templates
    html模版
    
### bmp/views
    未使用
### utils:
    杂项
    
### config.py
    配置文件
        使用方法:
            在runserver.py 同级目录新建.cfg结尾的空文件,文件名与config.py定义的类名相同    
        例:
            Config 类对应 config.cfg
            Test 类对应 test.cfg
        
### myapp.py
    对flask app类的封装，主要用作初始化
### create_db
    创建数据库表 并添加 refs.py定义的一些字段
### database.py
    对SQLAlchemy类的封装，主要用作SQLAlchemy的一些扩展操作
### const.py
    一些常量定义

### ops.sh
    没用