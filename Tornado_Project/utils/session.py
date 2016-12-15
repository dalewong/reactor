# coding:utf-8

# session = Session(request_handler,)
# session.sid
# session.data
# RequestHandler.get_secure_cookie()
# set_secure_cookie
# redis
import uuid
import logging
import json
import config

# session = Session(request_handler=self)
# session.session_id = 'abcdesfsdfs'

# # 第一次访问或者出错 {}

# session.data = {}
# session.data["user_id"] = 123
# session.data["user_mobile"] = 1186232

# session.save()


class Session(object):
    """"""
    def __init__(self, request_handler):
        self.request_handler = request_handler
        self.session_id = self.request_handler.get_secure_cookie("session_id")
        if not self.session_id:
            # 用户第一次访问
            # 生成一个session_id, 全局唯一
            self.session_id = uuid.uuid4().get_hex()
            self.data = {}
        else:
            # 拿到了session_id,去redis中取数据
            try:
                data = self.request_handler.redis.get("sess_%s" % self.session_id)
            except Exception as e:
                logging.error(e)
                self.data = {}
            if not data:
                self.data = {}
            else:
                self.data = json.loads(data)

    def save(self):

        json_data = json.dumps(self.data)
        print(json_data)
        try:
            self.request_handler.redis.setex("sess_%s" % self.session_id, config.session_expires, json_data)
        except Exception as e:
            logging.error(e)
            raise Exception("save session failed")
        else:
            self.request_handler.set_secure_cookie("session_id", self.session_id)

    def clear(self):
        self.request_handler.clear_cookie("session_id")
        try:
            self.redis.delete("sess_%s" % self.session_id)
        except Exception as e:
            logging.error(e)

    





