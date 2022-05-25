from django.db import models
from app_login import models as login

# Create your models here.
class Sections(models.Model):
    section_id = models.AutoField("id", primary_key=True)
    section_name = models.CharField("类型", unique=True,max_length=32)

    class Meta:
        db_table = 'table_section'  # 重命名


class Source(models.Model):
    source_id = models.AutoField(primary_key=True)
    source_title = models.CharField(max_length=32)
    source_desc = models.CharField(max_length=255)
    source_url = models.CharField(max_length=255)
    source_section = models.CharField(max_length=32)
    source_time = models.DateTimeField(auto_now_add=True)
    source_author = models.CharField(max_length=32)
    is_delete = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'table_source'  # 重命名


class Comment(models.Model):  # 定义评论模型
    article = models.ForeignKey(to=Source, on_delete=models.DO_NOTHING, verbose_name='评论文章')
    comment_content = models.TextField(verbose_name='评论内容')
    comment_author = models.ForeignKey(to=login.User, on_delete=models.DO_NOTHING, verbose_name='评论者')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    pre_comment = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True,
                                    verbose_name='父评论id')  # 父级评论，如果没有父级则为空NULL, "self"表示外键关联自己

    class Meta:
        db_table = 'table_comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name