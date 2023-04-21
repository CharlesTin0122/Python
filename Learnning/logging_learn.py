# -*- coding: utf-8 -*-
# @FileName :  logging_learn.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/4/23 16:38
# @Software : PyCharm
# Description:logging标准库学习

import logging


"""------------------------------------------------基础-----------------------------------------------------------"""
"""
默认日志级别是warning
使用baseConfig()来指定日志存储和日志输出级别,filemode参数中‘a’是追加模式（日志会向后追加），‘W’是写入模式（日志会被重写）。
"""
# logging.basicConfig(filename="demo.log", filemode="w", level=logging.INFO)
#
# logging.debug("this is a debug log")
# logging.info("this is an info log")
# logging.warning("this is a warning log")
# logging.error("this is an error log")
# logging.critical("this is a critical log")

# print("this is print log")

"""
输出格式和添加公共信息
%(asctime)s:显示log时间，%(levelname)-8s：显示log级别，-8：占8个字符，'-'为左对齐，
%(filename)s:显示文件名，%(lineno)s:显示行数，%(message)s:显示log信息，中间用|区隔
"""
# logging.basicConfig(format="%(asctime)s|%(levelname)-8s|%(filename)s:%(lineno)s|%(message)s", level=logging.DEBUG)
#
# logging.debug("this is a debug log")
# logging.warning("this is a warning log")


"""----------------------------------------------进阶------------------------------------------------------------"""
# 记录器 Logger，用于创建日志
logger = logging.getLogger("ccc.applog")  # 记录器，默认是‘root’
logger.setLevel(logging.DEBUG)  # 设置记录器log级别为debug
# 处理器 Handler，用于输出日志
consoleHandler = logging.StreamHandler()  # 流处理器handler
consoleHandler.setLevel(logging.DEBUG)  # 流处理器log级别为debug

fileHandler = logging.FileHandler(filename="addDemo.log")  # 文件处理器，没有指定日志级别，使用记录器的日志级别
fileHandler.setLevel(logging.INFO)  # 文件处理器log级别为info

"""记录器log级别设为最低，处理器分别设置log级别"""

# 格式 Formatter，用于输出的格式
formater = logging.Formatter("%(asctime)s|%(levelname)-8s|%(filename)s:%(lineno)s|%(message)s")  # 日志格式

# 给处理器设置格式
consoleHandler.setFormatter(formater)
fileHandler.setFormatter(formater)

# 给记录器设置处理器
logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)

# 过滤器 Filter
flt = logging.Filter("ccc")  # 定义过滤器为名称空间‘ccc’
logger.addFilter(flt)  # 记录器关联过滤器
fileHandler.addFilter(flt)  # 处理器关联过滤器

# 打印日志的代码
logger.debug("this is a debug log")
logger.info("this is a info log")
logger.warning("this is a warning log")
logger.error("this is a error log")
logger.critical("this is a critical log")
