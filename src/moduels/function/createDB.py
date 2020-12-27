# -*- coding: UTF-8 -*-

from moduels.component.NormalValue import 常量

def createDB():

    数据库连接 = 常量.数据库连接
    偏好设置表单名 = 常量.偏好设置表单名
    语音引擎表单名 = 常量.语音引擎表单名
    # 模板表单名 = 常量.数据库模板表单名
    # 皮肤表单名 = 常量.数据库皮肤表单名
    cursor = 数据库连接.cursor()

    result = cursor.execute(f'select * from sqlite_master where name = "{偏好设置表单名}";')
    if result.fetchone() == None:
        cursor.execute(f'''create table {偏好设置表单名} (
                                            id integer primary key autoincrement,
                                            item text,
                                            value text
                                            )''')
    else:
        # print('偏好设置表单已存在')
        pass
    result = cursor.execute(f'select * from sqlite_master where name = "{语音引擎表单名}";')
    if result.fetchone() == None:
        cursor.execute(f'''create table {语音引擎表单名} (
                                    id integer primary key autoincrement,
                                    引擎名称 text,
                                    服务商 text,
                                    AppKey text,
                                    语言 text,
                                    AccessKeyId text,
                                    AccessKeySecret text
                                    )''')
    else:
        # print('语音引擎表单名已存在')
        pass
    #
    # result = cursor.execute(f'select * from sqlite_master where name = "{皮肤表单名}";')
    # if result.fetchone() == None:
    #     cursor.execute(f'''create table {皮肤表单名} (
    #                                 id integer primary key autoincrement,
    #                                 skinName text,
    #                                 outputFileName text,
    #                                 sourceFilePath text,
    #                                 supportDarkMode BOOLEAN)''')
    # else:
    #     print('皮肤表单已存在')
    #
    数据库连接.commit() # 最后要提交更改
