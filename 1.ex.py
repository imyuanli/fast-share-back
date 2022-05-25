import os
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yuanliback.settings")
import django

django.setup()

from app_dashboard import models as dashboard
from app_login import models as login
# list = ["python", 'c语言', 'java', 'javascript', '前端', '后端', '数据库', '其他']
# for i in list:
#     models.Sections.objects.create(
#         section_name=i
#     )


# filter_user = models.User.objects.filter(user_token="2b138c1cdec913940c68cadb65e031fd")
# # user_id = i.pk
# for i in filter_user:
#     print(i.pk)

# filter_source = dashboard.Sections.objects.all()
# section_list = []
# for section in filter_source:
#     section_list.append({
#         section.pk: section.section_name
#     })
# print(section_list)
# source_list = []
# for i in filter_source:
#     print(i.source_author)
#     author_name=""
#     author_avatar=""
#     filter_user = login.User.objects.filter(user_id=i.source_author)
#     for j in filter_user:
#         author_name = j.user_name
#         author_avatar = j.user_avatar
#     source_list.append({
#         "source_title": i.source_title,
#         "source_desc": i.source_desc,
#         "source_url": i.source_url,
#         "source_section": i.source_section,
#         "author_name": author_name,
#         "author_avatar":author_avatar
#     })

# print(source_list)
dashboard.Source.objects.create(
    source_desc= "asdadasdadasdadasdadasdadasdadasdadasdadasdadasdadasdadasdadasdadasdadasdadasdadasdadasdadasdadasdad",
    source_section= "8",
    source_title= "asdasdasd",
    source_url= "https://ant.design/components/overview-cn/",
    source_author=2,
)

# for i in range(0,5):
#         a = random.randint(0, 9)
#         print(a)
# # ret = models.File.objects.filter(file_num=17578)
# # for i in ret:
# #         print(i.file_load)
# # a = '17578'
# # ret=models.File.objects.get(file_num=a)
# # if ret:
# #         b=models.File.objects.
# # else:
# #         print(1)
# # ret = models.Song.objects.values()
#
#     # file_name = file.split('.')[0]
#     # file_n=str(file_name)+'.ico'
# # img = PythonMagick.Image('../logo.jpg')
# # img.sample('48x48')
# # img.write('logo.ico')
# #
# #
# # # 查询所有数据，queryset,对象列表
# # ret = models.Song.objects.all()
# #
# #
# # # get方法，有且唯一的数据，对象
# # ret = models.Song.objects.get(pk=1)
# #
# #
# # # filter方法，返回满足条件的列表。对象列表
# # ret = models.Song.objects.filter(song_name="迟迟")
# #
# #
# # # order_by(),排序，默认是升序。字段前加-就是降序，也可进行多字段排序
# # ret = models.Song.objects.all().order_by("-pk")
# #
# #
# # # reverse,对已经排序的列表进行翻转
# # ret = models.Song.objects.all().order_by("pk").reverse()
# #
# #
# # # values,如果不指定字段的话，获取所有字段和值，字典,QuerySet  [{},{}]
# # ret = models.Song.objects.values()
# # # values,如果指定字段的话，获取指定值，字典QuerySet  [{},{}]
# # ret = models.Song.objects.values("song_name")
# #
# #
# #
# # # values_list,如果不指定字段的话，获取所有值，元组,QuerySet  [(),()]
# # ret = models.Song.objects.values_list()
# # # values_list,如果不指定字段的话，获取所有值，元组,QuerySet  [(),()]
# # ret = models.Song.objects.values_list("song_name")
# #
# #
# # #distinct,去重
# # ret = models.Song.objects.all().distinct()
# #
# # # count,计数 对象
# # ret = models.Song.objects.all().count()
# #
# #
# # # first,获取到对象列表的第一条数据 对象
# # ret = models.Song.objects.all().first()
# #
# #
# # # last,获取到对象列表的第一条数据 对象
# # ret = models.Song.objects.all().last()
# #
# # # exists,判断是否有数据.true false 对象
# # ret = models.Song.objects.filter(pk=3).exists()
# #
# # # exclude,返回满足不条件的列表。对象列表
# # ret = models.Song.objects.exclude(pk=3)
# #
# # print(ret)
#
#
# #
# # import  PythonMagick
# #
# # img = PythonMagick.Image()
# # # 这里要设置一下尺寸，不然会报ico尺寸异常错误
# # img.sample('48x48')
# # img.write('logo.ico')
#
#
# # import os
# # file_name = os.path.basename('logo.jpg')
# # print(file_name)
# # # 输出为 test.py
# # file_name = file_name.split('.')[0]
# # print(file_name+'.ico')
# # # 输出为 test
#
#
#
# # import random
# #
# # list=[]
# #
# # for i in range(0,5):
# #     a = random.randint(0, 9)
# #     list.append(a)
# # print(list)
# # s = ""
# # for i in list:
# #     s = s+str(i)
# # print(s)
import os
import shutil
#
# from MyQR import  myqr
# myqr.run(
#         words=('2'),
#         picture='../static/qrcodedata/img/favicon.png',
#         colorized=True,
#         save_name='npyi.png',
# )

import qrcode

# import qrcode
#
# img = qrcode.make('欲游。')
# img.save('npni.png')


# full_path='../dada.png'#将文件目录与文件名连接起来，形成原来完整路径
# des_path='../static/qrcodedata' #目标路径
# shutil.move(full_path,des_path)


#
# ss = '../static'
# ret = ss.replace('../', '', 1)
# print(ret)


# current_page = 9
# # 得到一的range(可随时变化的列表)
# #
# page_range = list(range(max(current_page - 2, 1), current_page)) + \
#              list(range(current_page, min(current_page + 2, 9) + 1))
# print(page_range)
