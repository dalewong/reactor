#coding:utf-8

import logging
import constants

from .BaseHandler import BaseHandler
from utils.response_code import RET
from utils.session import Session
from utils.user_login import user_login
from libs.qiniucloud import avatarSave
import config
import json

class UserLogin(BaseHandler):
    def post(self):
        usession = Session(self)
        # session_area = usession.data.get("area")
        session_area = self.redis.get('area')
        if session_area:
            usr = usession.data.get("uname") 
            session_areas = json.loads(session_area)
            return self.write(dict(erron = RET.OK, errmsg = usr, areaList = session_areas))

        area = self.db.query('select ai_area_id, ai_name from ih_area_info')
        print area
        areas = []
        for a in area:
            print(a)
            are = {}
            are["ai_area_id"] = a[u"ai_area_id"]
            are["ai_name"] = a[u"ai_name"]
            areas.append(are)

        areas = json.dumps(areas)
        self.redis.setex("area", config.areaTime ,areas)
        print(areas)
        
        if usession.data:
            usr = usession.data.get("uname")              

            return self.write(dict(erron = RET.OK, errmsg = usr, areaList = areas))

        self.write(dict(erron = RET.SESSIONERR, errmsg = '未登陆', areaList = areas))


class LocalHandler(BaseHandler):

    @user_login
    def post(self, usrsession):
        
        uavar = usrsession.data.get(u"uavatar")
        if uavar:
            usrsession.data[u"uavatar"] = config.cloud + uavar

        self.write(dict(erron = RET.OK, errmsg= usrsession.data))


        # self.db.get("select up_avatar from ih_user_profile where up_mobile = %s", )


class AvatarHandler(BaseHandler):

    @user_login
    def post(self, usrsession):
        guest_files = self.request.files
        guest_file = guest_files["avatar"][0]['body']

        try:
            avatar_name = avatarSave(guest_file)
        except Exception as e:
            logging.error(e)
            return self.write(dict(erron = RET.IOERR, errmsg = "远端服务器保存错误"))
        try:

            self.db.execute('update ih_user_profile set up_avatar = %s where up_name = %s', avatar_name, usrsession.data.get(u"uname"))   
        
        except Exception as e:
            logging.error(e)
            return self.write(dict(erron = RET.DBERR, errmsg = "数据库插入错误"))

        usrsession.data[u"uavatar"] = avatar_name
        usrsession.save()

        self.write(dict(erron = RET.OK, errmsg = config.cloud + avatar_name ))


class NameModifyHandler(BaseHandler):

    @user_login
    def post(self, usrsession):

        usrname = self.json_args.get("usrname")
        print(usrname)

        if usrname:
            try:
                self.db.execute("update ih_user_profile set up_name = %s where up_name = %s", usrname, usrsession.data.get(u"uname"))
            
            except Exception  as e:
                logging.error(e)
                return self.write(dict(erron = RET.DBERR, errmsg = "数据库查询出错"))

            
            usrsession.data[u"uname"] = usrname
            usrsession.save()

            self.write(dict(erron = RET.OK, errmsg = "更新成功"))

        self.write(dict(erron = RET.PARAMERR, errmsg = '参数不能为空'))


class AuthHandler(BaseHandler):

    @user_login
    def post(self, usrsession):

        realName = self.json_args.get("realName")
        idCard = self.json_args.get("idCard")

        if realName and idCard:
            uname = usrsession.data[u"uname"]
            try:
                self.db.execute("update ih_user_profile set up_real_name = %s, up_id_card = %s where up_name = %s", realName, idCard,  uname)
            except Exception as e:
                logging.error(e)
                return self.write(dict(erron = RET.DBERR, errmsg = "数据库查询错误"))

            return self.write(dict(erron = RET.OK, errmsg = "认证已提交，待审核"))


class HouseHandler(BaseHandler):

    @user_login
    def get(self, usrsession):
        """ """
        umobile = usrsession.data.get(u'umobile')
        print(umobile)
        usr_certify = usrsession.data.get(u"certify")
        #如果实名
        if usr_certify:
            try:
                user_datas = self.db.query('select ih_house_info.hi_house_id, ih_house_info.hi_title, ih_house_info.hi_area_id, ih_house_info.hi_price, ih_house_info.hi_utime from ih_house_info join ih_user_profile on ih_user_profile.up_user_id = ih_house_info.hi_user_id where ih_user_profile.up_mobile = %s', umobile)
            except Exception as e:
                logging.error(e)
                return self.write(dict(erron = RET.DBERR, errmsg = "数据库查询出错"))

            usrList = []
            for data in user_datas:
                usrDict = {}
                usrDict["hi_house_id"] = data["hi_house_id"]
                usrDict["hi_title"] = data["hi_title"]
                usrDict["hi_area_id"] = data["hi_area_id"]
                usrDict["hi_price"] = data["hi_price"]
                usrDict["hi_utime"] = data["hi_utime"].strftime('%Y-%m-%d') 
                usrList.append(usrDict)           
            
            return self.write(dict(erron = RET.OK, errmsg = usrList))
        try:
            usr_cer = self.db.get('select up_real_name from ih_user_profile where up_mobile = %s', umobile)
        
        except Exception as e:
            logging.error(e)
            return self.write(dict(erron = RET.DBERR, errmsg = "数据库查询出错"))
        #如果登陆
        if usr_cer:
            usrsession.data["certify"] = 'YES'
            usrsession.save()
            try:
                user_datas = self.db.query('select ih_house_info.hi_house_id, ih_house_info.hi_title, ih_house_info.hi_area_id, ih_house_info.hi_price, ih_house_info.hi_utime from ih_area_info inner join ih_user_profile on ih_user_profile.up_user_id = ih_house_info.hi_user_id where ih_user_profile.up_mobile = %s', umobile)
            except Exception as e:
                logging.error(e)
                return self.write(dict(erron = RET.DBERR, errmsg = "数据库查询出错"))
            usrList = []
            for data in user_datas:
                usrDict = {}
                usrDict["hi_house_id"] = data["hi_house_id"]
                usrDict["hi_title"] = data["hi_title"]
                usrDict["hi_area_id"] = data["hi_area_id"]
                usrDict["hi_price"] = data["hi_price"]
                usrDict["hi_utime"] = data["hi_utime"].strftime('%Y-%m-%d') 
                usrList.append(usrDict)    
            
            return self.write(dict(erron = RET.OK, errmsg = usrList))
        self.write(dict(erron = RET.USERERR, errmsg = "还未实名认证，请实名认证"))


class NewhouseHandler(BaseHandler):

    @user_login
    def get(self, usrsession):

        session_area = self.redis.get('area')
        if session_area:
            session_areas = json.loads(session_area)
            return self.write(dict(erron = RET.OK, areaList = session_areas))

        try:
            area = self.db.query('select ai_area_id, ai_name from ih_area_info')
        except Exception as e:
            logging.error(e)
            self.write(dict(erron = RET.DBERR, areaList = []))
        areas = []
        for a in area:           
            are = {}
            are["ai_area_id"] = a[u"ai_area_id"]
            are["ai_name"] = a[u"ai_name"]
            areas.append(are)

        areas = json.dumps(areas)
        try:
            self.redis.setex("area", config.areaTime ,areas)
        except Exception as e:
            logging.error(e)
            return self.write(dict(erron= RET.DBERR, areaList = areas))
        self.write(dict(erron = RET.OK, areaList = areas))


    @user_login
    def post(self, usrsession):
        
        data = self.json_args
        logging.debug(data)
        area_id  = data["area_id"]
        capacity = data["capacity"]
        title    = data["title"]
        price    = data["price"]
        facility = data["facility"]
        acreage  = data["acreage"]
        beds     = data["beds"]
        room_count = data["room_count"]
        max_days   = data["max_days"]
        deposit    = data["deposit"]
        address    = data["address"]
        min_days   = data["min_days"]
        unit       = data["unit"]
        umobile    = usrsession.data[u"umobile"]

        try:
            price = int(price) * 100
            deposit = int(deposit) * 100
        except Exception:
            return self.write(dict(erron = RET.PARAMERR, errmsg = "参数错误"))

        if all([area_id, capacity, title, price, facility, acreage, beds, room_count, max_days, deposit, address, min_days, unit]):
            try:
                usrId = self.db.get("select up_user_id from ih_user_profile where up_mobile = %s",umobile)
            except Exception as e:
                logging.error(e)
                self.write(dict(erron = DBERR, errmsg = "数据库查询出错1"))
            uid  = usrId["up_user_id"]
            logging.debug(uid)            
            sql = "insert into ih_house_info(hi_user_id, hi_title, hi_price, hi_area_id, hi_address, hi_room_count, hi_acreage, hi_house_unit, hi_capacity, hi_beds, hi_min_days, hi_max_days) values(%(user_id)s, %(title)s, %(price)s, %(area_id)s, %(address)s, %(room_count)s, %(acreage)s, %(house_unit)s, %(capacity)s, %(beds)s, %(min_days)s, %(max_days)s)"
            try:
                HouseId = self.db.execute(sql, user_id = uid , title = title, price = price, area_id = area_id, address = address, room_count = room_count, acreage= acreage, house_unit = unit, capacity = capacity, beds = beds, min_days = min_days, max_days = max_days)
            except Exception as e:
                logging.error(e)
                return self.write(dict(erron = RET.DBERR, errmsg = "数据库查询出错2"))
            
            sql_addition = []  #sql语句加入参数            
            sqlist = []  #查询参数构建

            sql = "insert into ih_house_facility(hf_house_id,hf_facility_id) values"
            for ufacility in facility:
                sql_addition.append( "(%s,%s)" )
                sqlist.append(HouseId)
                sqlist.append(ufacility)
            sqlist = tuple(sqlist)
            sql += ",".join(sql_addition)#完成查询语句拼装过程
            logging.debug(sql)
            logging.debug(sqlist)                

            try:
                self.db.execute(sql, *sqlist)
            except Exception as e:
                logging.error(e)
                try:
                    self.db.execute("delete from ih_house_info where hi_house_id = %s", HouseId)
                except Exception as e:
                    logging.error(e)
                    return self.write(dict(erron = RET.DBERR, errmsg = "数据库出错，需要手动删除3"))

                return self.write(dict(erron = RET.DBERR, errmsg = "数据库出错,请重新填写信息4"))

            return self.write(dict(erron = RET.OK, errmsg = "上传数据成功, 请上传图片"))

        self.write(dict(erron=RET.PARAMERR, errmsg = "缺少参数"))


class UsrPicHandler(BaseHandler):

    @user_login
    def post(self, usrsession):
        umobile = usrsession.data[u"umobile"]
        try:
            uhouse = self.db.query("select hi_house_id from ih_house_info left join ih_user_profile on  ih_house_info.hi_user_id = ih_user_profile.up_user_id where up_mobile = %s order by hi_house_id desc",umobile)
            print(uhouse)
        except Exception as e:
            logging.error(e)
            self.write(dict(erron = RET.DBERR, errmsg = '数据库查询错误')) 
        
        uhouseId = uhouse[0]["hi_house_id"]
        logging.debug(uhouseId)

        files = self.request.files
        file = files.get('house_image')
        if file:
            stream = file[0]['body']
            try:
                file_name = avatarSave(stream)
            except Exception as e:
                logging.error(e)
                return self.write(dict(erron = RET.THIRDERR, errmsg = "第三方传输失败)"))
            try:
                self.db.execute("update ih_house_info set hi_index_image_url = %s where hi_house_id = %s", file_name, uhouseId)
            except Exception as e:
                logging.error(e)
                return self.write(dict(erron = RET.DBERR, errmsg = "数据库保存出错"))
            return self.write(dict(erron = RET.OK, errmsg = "上传照片成功"))

        self.write(dict(erron = RET.PARAMERR, errmsg = "照片不能为空"))


class SearchHandler(BaseHandler):

    @user_login
    def post(self):
        self.write("hello")
        # area_id = self.get_argument("aid", "")
        # start_date = self.get_argument("sd", "")
        # end_date = self.get_argument("ed","")
        # order  = self.get_argument("st", "new")
        # page   = self.get_argument('p', "1")

        # sql = "select ih_house_info.hi_house_id, ih_house_info.hi_index_image_url, ih_house_info.hi_price, ih_house_info.hi_house_unit, ih_house_info.hi_address ih_user_profile.up_avatar from ih_house_info left join ih_order_info on ih_order_info.oi_house_id = ih_house_info.hi_house_id inner join ih_user_profile on ih_user_profile.up_user_id = ih_house_info.hi_user_id where "
       
        # sql_where_li = []
        # sql_params = {}

        # if area_id:
        #     sql_where_li.append("hi_area_id = %(hi_area_id)s")
        #     sql_params["hi_area_id"] = int(area_id)
        
        # if start_date and end_date:
        #     sql_where_li.append("not (oi_begin_date < %(end_date)s or oi_end_date > %(start_date)s)")
        #     sql_params["start_date"] = start_date
        #     sql_params["end_date"] = end_date

        # elif end_date:
        #     sql_where_li.append("not ()")
        #     sql_params["end_date"] = 
        # elif start:
        #     sql_where_li.appen()
        #     sql_params["start_date"] = 







             

















