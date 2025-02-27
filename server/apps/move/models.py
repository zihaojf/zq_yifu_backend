from django.db import models
from users.models import User
from vehicle.models import Vehicle


class MoveRecord(models.Model):
    move_user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="挪车用户", related_name="挪车用户"
    )
    moved_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="被挪车用户",
        related_name="被挪车用户",
    )
    move_vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, verbose_name="被挪车辆"
    )
    move_time = models.DateTimeField(auto_now=True, verbose_name="挪车时间")
    move_image = models.ImageField(
        upload_to="move_images/", verbose_name="挪车图片", blank=True, null=True
    )
    move_note = models.TextField(blank=True, verbose_name="挪车备注")

    is_initial = models.BooleanField(default=False, verbose_name="充电桩初始是否空闲")

    class Meta:
        verbose_name = "挪车记录"
