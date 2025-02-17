from django.db import models
from users.models import User


class Vehicle(models.Model):
    code = models.CharField(
        max_length=100, unique=False, verbose_name="车辆编码"
    )  # 车辆编码
    name = models.CharField(
        max_length=100, unique=False, verbose_name="车辆名称"
    )  # 车辆名称
    image = models.ImageField(
        upload_to="vehicles/", verbose_name="车辆图片"
    )  # 车辆图片
    note = models.TextField(
        unique=False, blank=True, verbose_name="车主备注"
    )  # 车主备注
    charging_time = models.IntegerField(
        unique=False, verbose_name="充电时长"
    )  # 充电时长
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="vehicles",
        verbose_name="所属用户",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "车辆信息"
