# coding:utf-8

import os

# Application配置参数
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "template"),
    "cookie_secret":"kb8LwR4MSASQzT+HWLqy4YWnN1DJcEKJrjblnr77uSw=",
    "xsrf_cookies":True,
    "debug":True,
}

# mysql
mysql_options = dict(
    host="127.0.0.1",
    database="ihome",
    user="root",
    password="wQ5198871"
)

# redis
redis_options = dict(
    host="127.0.0.1",
    port=6379 
)

log_file = os.path.join(os.path.dirname(__file__), "logs/log")
log_level = "debug"

session_expires = 86400 # session数据有效期，秒

cloud = 'http://oh7i0d9jl.bkt.clouddn.com/'

areaTime = 86400