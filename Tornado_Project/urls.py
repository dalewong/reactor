# coding:utf-8

import os

from handlers import Passport, VerifyCode, IndexHandler
from handlers.BaseHandler import StaticFileHandler


handlers = [
    (r"/api/imagecode", VerifyCode.ImageCodeHandler),
    (r"/api/smscode", VerifyCode.SMSCodeHandler),
    (r"/api/register", VerifyCode.RegisterHandler),
    (r"/api/smsverify", VerifyCode.SMSVerifyHandler),
    (r"/api/login", VerifyCode.LoginHandler),
    (r"/api/index", IndexHandler.UserLogin),
    (r'/api/local', IndexHandler.LocalHandler),
    (r'/api/profile/avatar', IndexHandler.AvatarHandler),
    (r'/api/namemodify', IndexHandler.NameModifyHandler),
    (r'/api/auth', IndexHandler.AuthHandler),
    (r'/api/myhouse', IndexHandler.HouseHandler),
    (r'/api/newhouse', IndexHandler.NewhouseHandler),
    (r'/api/house/image', IndexHandler.UsrPicHandler),
    # (r'/api/search', IndexHandler.SearchHandler),
    ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
    (r"/(.*)", StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html"))
]