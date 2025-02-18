from django.db import models
from users.models import User


class Notifications(models.Model):
    message = models.TextField(blank=False, verbose_name="消息内容")
    send_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name="发送者",
        related_name="send_user",
    )
    receive_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name="接收者",
        related_name="receive_user",
    )
    send_time = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")

    class Meta:
        verbose_name = "消息"
        verbose_name_plural = "消息列表"
        ordering = ["-send_time"]
