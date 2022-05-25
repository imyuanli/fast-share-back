import hashlib
import random
import string
import time

import requests
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# Create your views here.
from dependencies import ok, fail
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives
from app_login import models


# 生成token
def generate_token(name):
    c_time = str(time.time())
    r = str(random.random())
    return hashlib.new("md5", (c_time + r + name).encode("utf-8")).hexdigest()


# 获取验证码
def get_login_code(request):
    # 获取到post参数
    postBody = request.body
    json_result = json.loads(postBody)
    email = json_result["email"]
    code_list = []
    for i in range(10):  # 0-9数字
        code_list.append(str(i))
    for i in range(65, 91):  # 对应从“A”到“Z”的ASCII码
        code_list.append(chr(i))
    for i in range(97, 123):  # 对应从“a”到“z”的ASCII码
        code_list.append(chr(i))
    myslice = random.sample(code_list, 6)  # 从list中随机获取6个元素，作为一个片断返回
    verification_code = ''.join(myslice)
    # 先判断有没有这个邮箱
    have_email = models.Login.objects.filter(email=email)
    # print("have_email",have_email)
    if have_email:
        have_email.update(login_code=verification_code)
    # # 将生成的验证码和邮箱存到数据库
    else:
        models.Login.objects.create(email=email, login_code=verification_code)

    res = send_mail('您的当前账号验证码为',
                    '验证码2分钟内有效验：' + verification_code,
                    '2865437316@qq.com',
                    [email])
    if res != 1:
        static = '验证码发送失败'
    else:
        static = '验证码发送成功'
    return JsonResponse(ok(static), safe=False)


# # 登录
def get_login(request):
    postBody = request.body
    json_result = json.loads(postBody)
    email = json_result["email"]
    login_code = json_result["login_code"]
    login_models = models.Login.objects.filter(email=email)
    for i in login_models:
        if i.login_code == login_code:
            token = generate_token(email)
            login_models.update(user_token=token)
            # 如果有这个用户 就更改而不是创建
            filter_user = models.User.objects.filter(user_email=email)
            if filter_user:
                filter_user.update(user_token=token)
            else:
                models.User.objects.create(
                    user_token=token,
                    user_email=email,
                    user_name=f"用户{stringDigits(10)}",
                    user_avatar='https://joeschmoe.io/api/v1/random'
                )
            return JsonResponse(ok({"token": token}), safe=False)
        else:
            return JsonResponse(fail(1009, "验证码错误"), safe=False)


def verify_token(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    user = models.Login.objects.filter(user_token=token)
    if not user:
        return 1


def get_info(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    user_data = {}
    if verify_token(request) == 1:
        return JsonResponse(fail(99, "您还未登录"), safe=False)
    else:
        filter_user = models.User.objects.filter(user_token=token)
        if filter_user:
            for i in filter_user:
                user_data = {
                    "user_name": i.user_name,
                    "user_avatar": i.user_avatar,
                }

        return JsonResponse(ok(user_data), safe=False)

# def update_info(request):
#     # file = request.POST.get("file")
#     # print(request.body)
#     return HttpResponse("ok")

def stringDigits(len):
    return "".join(
        [random.choice(string.ascii_letters) if random.randint(0, 1) else random.choice(string.digits) for i in
         range(len)])
