from django.db import models
from django.utils import timezone


# Create your models here.


class Email(models.Model):
    get_id = models.PositiveIntegerField(
        primary_key=True, verbose_name="流水號", db_column='流水號', unique=True
    )
    name = models.CharField(verbose_name="員工姓名", db_column='員工姓名', max_length=50)
    email = models.EmailField(verbose_name='信箱', db_column='信箱')
    times = models.PositiveSmallIntegerField(default=0, verbose_name='訪問次數', db_column='訪問次數')

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'tb_data_management'


class Data(models.Model):
    num = models.ForeignKey(Email, db_column='流水號', on_delete=models.CASCADE, related_name='data')
    pub_time = models.DateTimeField(
        default=timezone.now, verbose_name='訪問時間', db_column='訪問時間'
    )

    def __str__(self):
        return f'{self.pub_time}'

    class Meta:
        db_table = 'tb_data_all'

