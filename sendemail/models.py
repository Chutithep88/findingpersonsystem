from django.db import models
from django.urls import reverse

# Create your models here.
class Dataemail(models.Model):
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    from_email = models.EmailField()

    def get_absolute_url(self):
        return reverse("success")

#ส่วนอีเมล์ที่เก็บไว้เพื่อใช้ในการส่งเมล์ไปยังเจ้าหน้าที่ของระบบสนับสนุนการป้องกันและค้นหาคนหาย
class allemailtoadmin(models.Model):
    name = models.CharField(max_length=200, default='',)

    def __str__(self):
        return self.name