# coding:utf-8

import logging
import constants
import random
import re
import hashlib

from .BaseHandler import BaseHandler
from utils.captcha.captcha import captcha
from utils.response_code import RET
from utils.session import Session
from libs.yuntongxun.CCP import ccp

class ImageCodeHandler(BaseHandler):
    
    """"""
    def get(self):
        code_id = self.get_argument("codeid")
        pre_code_id = self.get_argument("pcodeid")
        if pre_code_id:
            try:
                self.redis.delete("image_code_%s" % pre_code_id)
            except Exception as e:
                logging.error(e)
        # name 图片验证码名称
        # text 图片验证码文本
        # image 图片验证码二进制数据
        name, text, image = captcha.generate_captcha()
        try:
            self.redis.setex("image_code_%s" % code_id, constants.IMAGE_CODE_EXPIRES_SECONDS, text)
        except Exception as e:
            logging.error(e)
            self.write("")
        else:
            self.set_header("Content-Type", "image/jpg")
            self.write(image)


class SMSCodeHandler(BaseHandler):
    """"""
    def post(self):
        # 获取参数
        mobile = self.json_args.get("mobile") 
        image_code_id = self.json_args.get("image_code_id") 
        image_code_text = self.json_args.get("image_code_text") 
        if not all((mobile, image_code_id, image_code_text)):
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数不完整")) 
        if not re.match(r"1\d{10}", mobile):
            return self.write(dict(errno=RET.PARAMERR, errmsg="手机号错误")) 
        # 判断图片验证码
        try:
            real_image_code_text = self.redis.get("image_code_%s" % image_code_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="查询出错"))
        if not real_image_code_text:
            return self.write(dict(errno=RET.NODATA, errmsg="验证码已过期！"))
        if real_image_code_text.lower() != image_code_text.lower():
            return self.write(dict(errno=RET.DATAERR, errmsg="验证码错误！"))
        # 若成功：
        # 生成随机验证码
        sms_code = "%04d" % random.randint(0, 9999)
        try:
            self.redis.setex("sms_code_%s" % mobile, constants.SMS_CODE_EXPIRES_SECONDS, sms_code)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="生成短信验证码错误"))
        # 发送短信
        try:
            ccp.sendTemplateSMS(mobile, [sms_code, constants.SMS_CODE_EXPIRES_SECONDS/60], 1)
            # 需要判断返回值，待实现
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.THIRDERR, errmsg="发送失败！"))
        self.write(dict(errno=RET.OK, errmsg="OK"))


class RegisterHandler(BaseHandler):

    def post(self):
        mobile = self.json_args.get('mobile')
        phonecode = self.json_args.get('phonecode')
        passwd1 = self.json_args.get('passwd1')
        passwd2 = self.json_args.get('passwd2')


        if (passwd1 and passwd2 and passwd1 == passwd2):
            # if re.match(r'\S{5, 10}', passwd1):
            pattern = re.compile(r'^\S{5,10}$')
            if pattern.match(passwd1):
                
                secure_passwd = hashlib.md5(passwd1 + constants.SALT).hexdigest()
                try:
                    self.db.execute('insert into ih_user_profile(up_name, up_mobile, up_passwd, up_admin) values(%s, %s, %s, %s)', mobile, mobile, secure_passwd, 0)

                except Exception as e:
                    logging.error(e)
                    return self.write(dict(erron = RET.DBERR, errmsg = '数据库写入错误'))

                session = Session(self)

                session.data['uname'] = mobileewq

                session.save()                
                
                return self.write(dict(erron=RET.OK,errmsg='/index.html'))
          
            return self.write(dict(erron=RET.DATAERR, errmsg ='密码格式不正确'))
        
        self.write(dict(erron=RET.DATAERR, errmsg ='密码不能为空且两次输入密码需一致'))

        
class SMSVerifyHandler(BaseHandler):
    def post(self):
        phonenum = self.json_args.get('phonenum')
        print(phonenum)
        if phonenum:            
            name = self.db.get('select up_name from ih_user_profile where up_mobile = %s', phonenum)

            if name:               
                return self.write(dict(erron=RET.PARAMERR, errmsg= '手机号重复'))

            return self.write(dict(erron=RET.OK, errmsg='手机号验证通过'))

        self.write(dict(RET.DATAERR, errmsg = '手机号不能为空'))


class LoginHandler(BaseHandler):
    def post(self):
        mobile = self.json_args.get('mobile')
        password = self.json_args.get('passwd')
        secure_passwd = hashlib.md5(password + constants.SALT).hexdigest()

        try:
            uname = self.db.get('select up_name, up_mobile, up_avatar from ih_user_profile where up_mobile = %s and up_passwd = %s', mobile, secure_passwd)
            print(uname)
        except Exception as e:
            logging.error(e)
            return self.write(dict(erron = RET.DBERR, errmsg = '数据库查询错误'))
        
        if uname:
            session = Session(self)
            session.data['uname'] = uname.get(u'up_name')
            session.data['umobile'] = uname.get(u'up_mobile')
            session.data['uavatar'] = uname.get(u'up_avatar')
            session.save()
            print(session.data['uname'],session.data['umobile'])

            return self.write(dict(erron = RET.OK, errmsg = '登陆成功'))
        
        self.write(dict(erron = RET.PARAMERR, errmsg = '用户名或者密码错误'))







        