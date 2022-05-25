import json

from django.http import JsonResponse, HttpResponse
from app_login import models as login
from app_dashboard import models
from dependencies import ok, fail
# 搜索一条留言的所有子留言，广度优先
import queue


def get_source_list(request):
    section = request.GET.get("section")
    if not section or section == str(91):
        filter_source = models.Source.objects.filter(is_delete=0).order_by('-source_time')
    else:
        filter_source = models.Source.objects.filter(is_delete=0, source_section=section).order_by('-source_time')
    source_list = []
    for i in filter_source:
        # 获取作者头像
        author_name = ""
        author_avatar = ""
        filter_user = login.User.objects.filter(user_id=i.source_author)
        for j in filter_user:
            author_name = j.user_name
            author_avatar = j.user_avatar
        source_list.append({
            "source_id": i.pk,
            "source_title": i.source_title,
            "source_desc": i.source_desc,
            "source_url": i.source_url,
            "source_section": i.source_section,
            "author_name": author_name,
            "author_avatar": author_avatar
        })
    #     获取类型
    filter_sections = models.Sections.objects.all()
    section_list = []
    for section in filter_sections:
        section_list.append({
            section.pk: section.section_name
        })
    return JsonResponse(ok({"source_list": source_list,
                            "section_list": section_list}), safe=False)
    # return HttpResponse("ok")


def verify_token(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    user = login.Login.objects.filter(user_token=token)
    if not user:
        return 1


# 新增
def insert_source(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    post_body = request.body
    json_result = json.loads(post_body)
    if verify_token(request) == 1:
        return JsonResponse(fail(999, "您还未登录"), safe=False)
    else:
        # 获取token的用户
        filter_user = login.User.objects.filter(user_token=token)
        source_author = ""
        if filter_user:
            for i in filter_user:
                source_author = i.pk
            models.Source.objects.create(
                source_title=json_result["source_title"],
                source_desc=json_result["source_desc"],
                source_url=json_result["source_url"],
                source_section=json_result["source_section"],
                source_author=source_author
            )
            return JsonResponse(ok("插入成功"), safe=False)
        else:
            return JsonResponse(fail(10, "插入失败，可以尝试一下重新登录"), safe=False)


def get_single_source(request):
    source_id = request.GET.get("source_id")
    source_obj = ""
    filter_source = models.Source.objects.filter(is_delete=0, pk=source_id)
    for i in filter_source:
        # 获取作者头像
        author_name = ""
        author_avatar = ""
        filter_user = login.User.objects.filter(user_id=i.source_author)
        for j in filter_user:
            author_name = j.user_name
            author_avatar = j.user_avatar
        source_obj = {
            "source_id": i.pk,
            "source_title": i.source_title,
            "source_desc": i.source_desc,
            "source_url": i.source_url,
            "source_section": i.source_section,
            "author_name": author_name,
            "author_avatar": author_avatar,
            "source_time": i.source_time,
        }
    section = filter_source.values('source_section').get()
    # 推荐
    recommend_list = []
    recommend_source = models.Source.objects.filter(is_delete=0, source_section=section['source_section']).order_by(
        '?')[:2]
    for i in recommend_source:
        # 获取作者头像
        author_name = ""
        author_avatar = ""
        filter_user = login.User.objects.filter(user_id=i.source_author)
        for j in filter_user:
            author_name = j.user_name
            author_avatar = j.user_avatar
        recommend_list.append({
            "source_id": i.pk,
            "source_title": i.source_title,
            "source_desc": i.source_desc,
            "source_url": i.source_url,
            "source_section": i.source_section,
            "author_name": author_name,
            "author_avatar": author_avatar
        })
    #     获取类型
    filter_sections = models.Sections.objects.all()
    section_list = []
    for section in filter_sections:
        section_list.append({
            section.pk: section.section_name
        })
    return JsonResponse(ok({"source_list": source_obj,
                            "section_list": section_list,
                            "recommend_list": recommend_list
                            }), safe=False)


# 点赞c
# def get_collection(request):
#     token = request.META.get("HTTP_AUTHORIZATION")
#     post_body = request.body
#     json_result = json.loads(post_body)
#     if verify_token(request) == 1:
#         return JsonResponse(fail(999, "您还未登录"), safe=False)
#     else:
#         # 获取token的用户
#         filter_user = login.User.objects.filter(user_token=token)
#         collection = ""
#         if filter_user:
#             for i in filter_user:
#                 if i.user_collection == -1:
#                     collection = json_result["source_id"]
#                 else:
#                     collection = i.user_collection + ","
#                 collection += json_result["source_id"]
#                 print(collection)
#             filter_user.update(user_collection=collection)
#             return JsonResponse(ok("插入成功"), safe=False)
#         # return JsonResponse(ok(
#         #     {"filter_user": filter_user}
#         # ), safe=False)


# 获取已发布

def get_is_published(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    post_body = request.body
    json_result = json.loads(post_body)
    if verify_token(request) == 1:
        return JsonResponse(fail(999, "您还未登录"), safe=False)
    else:
        # 获取token的用户
        filter_user = login.User.objects.filter(user_token=token)
        filter_source = ""
        if filter_user:
            for i in filter_user:
                filter_source = models.Source.objects.filter(is_delete=0, source_author=i.pk).order_by('-source_time')
        pulished_list = []
        for i in filter_source:
            # 获取作者头像
            pulished_list.append({
                "source_id": i.pk,
                "source_title": i.source_title,
                "source_desc": i.source_desc,
                "source_url": i.source_url,
                "source_section": i.source_section,
            })
        #     获取类型
        filter_sections = models.Sections.objects.all()
        section_list = []
        for section in filter_sections:
            section_list.append({
                section.pk: section.section_name
            })
        return JsonResponse(ok({"source_list": pulished_list,
                                "section_list": section_list}), safe=False)
        # return JsonResponse(ok(
        #     {"filter_user": filter_user}
        # ), safe=False)


# 更新资源
def update_published(request):
    post_body = request.body
    json_result = json.loads(post_body)
    models.Source.objects.filter(source_id=json_result["source_id"]).update(
        source_title=json_result['source_title'],
        source_desc=json_result['source_desc'],
        source_url=json_result['source_url'],
        source_section=json_result['source_section']
    )
    return JsonResponse(ok("更新成功"), safe=False)


# 更新资源
def delete_published(request):
    post_body = request.body
    json_result = json.loads(post_body)
    models.Source.objects.filter(source_id=json_result["source_id"]).update(is_delete=1)
    return JsonResponse(ok("删除成功"), safe=False)


# 搜搜资源
def search_source(request):
    if verify_token(request) == 1:
        return JsonResponse(fail(999, "您还未登录"), safe=False)
    else:
        source_id = request.GET.get("source_id")
        filter_source = models.Source.objects.filter(is_delete=0, pk=source_id)
        for i in filter_source:
            # 获取作者头像
            author_name = ""
            author_avatar = ""
            filter_user = login.User.objects.filter(user_id=i.source_author)
            for j in filter_user:
                author_name = j.user_name
                author_avatar = j.user_avatar
            source_obj = {
                "source_id": i.pk,
                "source_title": i.source_title,
                "source_desc": i.source_desc,
                "source_url": i.source_url,
                "source_section": i.source_section,
                "author_name": author_name,
                "author_avatar": author_avatar,
                "source_time": i.source_time,
            }
        q = request.GET.get("q")
        search_list = []
        filter_search_title = models.Source.objects.filter(is_delete=0, source_title__icontains=q)
        filter_search_desc = models.Source.objects.filter(is_delete=0, source_desc__icontains=q)
        for i in filter_search_title:
            search_list.append({
                "source_id": i.pk,
                "source_title": i.source_title,
                "type": 1
            })
        for i in filter_search_desc:
            search_list.append({
                "source_id": i.source_id,
                "source_title": i.source_title,
                "type": 2
            })
        return JsonResponse(ok({"search_list": search_list}), safe=False)


# 新增评论
def insert_comment(request):
    if verify_token(request) == 1:
        return JsonResponse(fail(999, "您还未登录"), safe=False)
    else:
        token = request.META.get("HTTP_AUTHORIZATION")
        post_body = request.body
        json_result = json.loads(post_body)
        filter_user = login.User.objects.filter(user_token=token)
        comment = {}
        if filter_user:
            for i in filter_user:
                comment = models.Comment.objects.create(
                    comment_content=json_result['comment_content'],
                    pre_comment_id=json_result['pre_comment_id'],
                    article_id=json_result['article_id'],
                    comment_author_id=i.pk
                )
        return JsonResponse(ok({"comment_time": comment.comment_time}),
                            safe=False)
        # JsonResponse返回JSON字符串，自动序列化，如果不是字典类型，则需要添加safe参数为False


# 获取评论
def get_comment_list(request):
    article_id = request.GET.get("source_id")
    comment_list = []
    filter_comment = models.Comment.objects.filter(article_id=article_id).order_by('-comment_time')
    for i in filter_comment:
        comment_list.append({
            "author": i.comment_author.user_name,
            "avatar": i.comment_author.user_avatar,
            "content": i.comment_content,
            "datetime": i.comment_time,
            "id": i.pk,
            "pre_id": i.pre_comment_id,
        })
    new_comment_list = sortMsg(comment_list)
    return JsonResponse(ok({
        "comment_list": new_comment_list,
        "comment": comment_list
    }), safe=False)


#
# 整理留言信息返回格式
def sortMsg(allMsg):
    list = []
    for i in range(len(allMsg)):
        tmpParent = allMsg[i]
        tmpChild = []
        # 如果没有属于根评论，则搜索该评论下的所有子评论
        if tmpParent.get('pre_id') == None:
            tmpChild = bfs(tmpParent, allMsg)
        # 如果是子评论则跳过，子评论最终会出现在根评论的子节点中
        else:
            continue
        tmpParent['children'] = tmpChild
        list.append(tmpParent)
    return list


# 搜索一条留言的所有子留言，广度优先
import queue


def bfs(parent, allMsg):
    childrenList = []
    q = queue.Queue()
    q.put(parent)
    while (not q.empty()):
        tmpChild = q.get()
        for i in range(len(allMsg)):
            if allMsg[i]['pre_id'] is not None and allMsg[i]['pre_id'] == tmpChild['id']:
                childrenList.append(allMsg[i])
                q.put(allMsg[i])
    return childrenList
