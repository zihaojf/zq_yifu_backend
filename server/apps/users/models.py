# from tabnanny import verbose

from django.db import models
from zq_django_util.utils.user.models import AbstractUser


class User(AbstractUser):
    """
    基本用户表
    """

    # 自定义字段

    # extra-checks-disable-next-line field-text-null
    openid = models.CharField(
        max_length=64, unique=True, null=True, verbose_name="微信openid"
    )

    union_id = models.UUIDField(
        unique=True, null=True, blank=True, verbose_name="自强union_id"
    )

    STATUS_CHOICES = (
        ("idle", "空闲中"),
        ("queuing", "排队中"),
        ("assigned", "已分配充电桩"),
        ("charging", "充电中"),
        ("waiting", "充电完毕等待挪车"),
        ("moved", "已被挪车"),
    )
    nickname = models.CharField("昵称", max_length=64, default="新用户", blank=True)
    phone = models.CharField("手机号", max_length=20, blank=True)
    faculty = models.CharField("学部", max_length=100, blank=True)
    avatar = models.ImageField("头像", upload_to="avatar/", null=True, blank=True)
    credit_score = models.IntegerField("信用分", default=100)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="idle",
        verbose_name="用户状态",
    )
    update_time = models.DateTimeField(auto_now=True, verbose_name="状态更新时间")

    class Meta:
        app_label = "users"
        db_table = "zq_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name
