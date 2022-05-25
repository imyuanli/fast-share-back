#!/usr/bin/python3
import datetime
import random
import string
import traceback

import dataset
import pymysql
import requests
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseSettings

pymysql.install_as_MySQLdb()

VERSION = '2.2'


# -------------静态变量-------------
class Settings(BaseSettings):
    env: str = "dev"


settings = Settings()
DB_URL = 'rm-uf6b2d8720b76742wno.mysql.rds.aliyuncs.com'
if settings.env and (settings.env == 'production' or settings.env == 'test'):
    DB_URL = 'rm-uf6b2d8720b76742w.mysql.rds.aliyuncs.com'

BASE_FRONT_URL = "https://jztest.jzmbti.com"
if settings.env and settings.env == 'production':
    BASE_FRONT_URL = "https://jzmbti.com"

SECRET_KEY_ENTERPRISE = "getbusylivingorgetbusydyingenterprise"
ALGORITHM = "HS256"

# -------------数据库-------------

db_enterprise = dataset.connect(
    f'mysql://root:X5G57diLH8uVYvub@{DB_URL}:3306/enterprise?charset=utf8&autocommit=true',
    engine_kwargs={'pool_recycle': 280, 'pool_pre_ping': True}
)  # type:dataset.Database
db_mbti = dataset.connect(
    f'mysql://root:X5G57diLH8uVYvub@{DB_URL}:3306/mbti?charset=utf8&autocommit=true',
    engine_kwargs={'pool_recycle': 280, 'pool_pre_ping': True}
)  # type:dataset.Database
table_enterprise_user = db_enterprise.get_table('enterprise_user')  # type: dataset.Table
table_enterprise_sn = db_enterprise.get_table('enterprise_sn')  # type: dataset.Table
table_department = db_enterprise.get_table('department')  # type: dataset.Table
table_employee = db_enterprise.get_table('employee')  # type: dataset.Table
table_enterprise = db_enterprise.get_table('enterprise')  # type: dataset.Table
table_employee_department_relation = db_enterprise.get_table('employee_department_relation')  # type: dataset.Table
table_recruit = db_enterprise.get_table('recruit')  # type: dataset.Table
table_recruit_position_category = db_enterprise.get_table('recruit_position_category')  # type: dataset.Table

table_article = db_enterprise.get_table('home_article')  # type: dataset.Table
table_section = db_enterprise.get_table('home_section')  # type: dataset.Table
table_author = db_enterprise.get_table('home_author')  # type: dataset.Table
# -------------安全设置-------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/login/weixin")


async def get_current_enterprise_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = UnLoginException
    try:
        payload = jwt.decode(token, SECRET_KEY_ENTERPRISE, algorithms=[ALGORITHM])
        uid: str = payload.get("uid")
        expires = payload.get("exp")
        version = payload.get("version")
        if uid is None:
            raise credentials_exception
        if expires is None or datetime.datetime.utcnow() > datetime.datetime.utcfromtimestamp(expires):
            raise credentials_exception
        if version is None or version != VERSION:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    user = table_enterprise_user.find_one(id=uid, del_flag=0)
    if user is None:
        raise credentials_exception
    return user


def get_ip_address(ip):
    table_ip_address = db_mbti.get_table('ip_address', primary_id='id',
                                         primary_type=db_mbti.types.integer)  # type: dataset.Table
    ip_address = table_ip_address.find_one(ip=ip)
    if not ip_address:
        r = requests.get('http://apis.juhe.cn/ip/ipNewV3',
                         params={'ip': ip, 'key': '2afeb58a849ab6f50032242f6124f3b1'})
        ip_address = {}
        try:
            result_ip_address = r.json()['result']
            if result_ip_address:
                ip_address['ip'] = ip
                ip_address['country'] = result_ip_address['Country']
                ip_address['province'] = result_ip_address['Province']
                ip_address['city'] = result_ip_address['City']
                ip_address['county'] = result_ip_address['District']
                ip_address['isp'] = result_ip_address['Isp']
                table_ip_address.insert(ip_address)
        except:
            print(r.content)
    return ip_address


# -------------error msg-------------

def sent_error_msg_to_ding_talk(content):
    if settings.env == 'dev':
        print(content)
    else:
        requests.post(
            "https://oapi.dingtalk.com/robot/send?" +
            "access_token=67b575c773e36d0dcf264e58bb4c5afd2bb3483f23e182ebe48f2276c43bff67",
            json={
                "msgtype": "text",
                "text": {"content": content}}
        )


def get_request_msg(request: Request):
    ip = request.headers.get('X-Forwarded-For')
    ip_address = get_ip_address(ip)
    ip_place = f"{ip_address.get('country')}," + \
               f"{ip_address.get('province')}," + \
               f"{ip_address.get('city')}," + \
               f"{ip_address.get('county')}," + \
               f"{ip_address.get('isp')}"
    url = request.url
    params = request.query_params
    # body = await request.body()
    msg = f"IP: {ip} {ip_place} \n URL:{url}\n HEADER:{request.headers} \n PARAM:{params}\n "
    return msg


def send_request_ding_talk(request, is_traceback=True):
    content = get_request_msg(request)
    if is_traceback:
        content += f" \n {traceback.format_exc()}"
    sent_error_msg_to_ding_talk(content)


# -------------response-------------

def ok(data):
    return {
        "data": data,
        "errno": 0,
        "errmsg": "成功",
    }


def fail(errno, errmsg):
    return {
        "errno": errno,
        "errmsg": errmsg,
    }




def bad_argument():
    return fail(401, "接口参数不对，如有问题可联系客服")


def un_login():
    return fail(501, "请登录")


def default_error():
    return fail(502, "系统内部错误，如有问题可联系客服")


def no_permission():
    return fail(506, "只能看您自己的内容哦")


class UnLoginException(Exception):
    pass


class NoPermissionException(Exception):
    pass


class BadArgumentException(Exception):
    pass
