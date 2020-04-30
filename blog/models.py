from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from wtforms.fields.html5 import DateField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

#ใช้เพื่อ upload image to cloudinary
from cloudinary.models import CloudinaryField

#ส่วนเก็บข้อมูลช่วงอายุและเพศ (ช่วงอายุและเพศใช้เฉพาะแจ้งเบาะแส)
class AgePeople(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Gender(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

#ส่วนอีเมล์ที่เก็บไว้เพื่อใช้ในการส่งเมล์ไปยังสื่อ
class allemail(models.Model):
    position = models.CharField(max_length=200, default='',)
    mail = models.CharField(max_length=200, default='',)
    organization = models.CharField(max_length=200, default='',)
    places = models.CharField(max_length=200, default='',)

    def __str__(self):
        return self.position
    

#ส่วนของผู้ที่เจอแล้ว ไม่ใช้คนหายอีกต่อไป
class Postfound(models.Model):
    # title = models.CharField(max_length=100, verbose_name = "<font color='red'>หัวข้อ</font>")
    realname = models.CharField(max_length=150, default='', verbose_name = "<font color='red'>ชื่อจริงและนามสกุล</font>")
    nickname = models.CharField(max_length=50, default='', verbose_name = "<font color='red'>ชื่อเล่น</font>")
    realnameEng = models.CharField(max_length=150, blank=True, null=True, verbose_name = "ชื่ออังกฤษ")
    age = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(100)], 
    blank=True, null=True, verbose_name = "<font color='red'>อายุ(ปี)</font>",
    help_text="กรอกอายุ 1- 100")

    nationality = models.CharField(max_length=10, default='', verbose_name = "<font color='red'>เชื้อชาติ</font>")
    lostday = models.CharField(max_length=10, blank=True, null=True, verbose_name = "วันที่หาย",
    help_text="กรอกวันที่ เช่น 21/01/2530",)
    lostTime = models.CharField(max_length=5, blank=True, null=True, verbose_name = "เวลาที่หาย",
    help_text="กรอกเวลา เช่น 12.00 , 19.30")
    lostWhere = models.CharField(max_length=100, blank=True, null=True, verbose_name = "สถานที่หาย")
    lostReason = models.CharField(max_length=200, blank=True, null=True, verbose_name = "เหตุผลที่หาย")
    identities = models.CharField(max_length=100, default='', verbose_name = "<font color='red'>ลักษณะพิเศษ</font>",
    help_text="ลักษณะพิเศษ เช่น มีไฝบนหน้า ใส่สร้องทอง ผิวคล้ำเป็นต้น")

    # image = models.ImageField(upload_to='images4', blank=True, null=True, verbose_name = "รูปภาพ",
    # help_text="รูปภาพของผู้สูญหาย")
    image = CloudinaryField('รูปภาพ', blank=True, null=True)

    content = models.TextField(blank=True, null=True, verbose_name = "รายละเอียดเพิ่มเติม", 
    help_text="กรอกรายละเอียดเพิ่มเติม")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    gender = models.CharField(max_length=5, default='', verbose_name = "<font color='red'>เพศ</font>")

    telephone = models.CharField(max_length=10, default='', verbose_name = "<font color='red'>เบอร์โทรติดต่อกับผู้บันทึกข้อมูล</font>")
    email = models.CharField(max_length=100, default='', verbose_name = "<font color='red'>อีเมล์ของผู้บันทึกข้อมูล</font>")
    

    DATE_INPUT_FORMATS = ['%d-%m-%Y']

    def __str__(self):
        return self.realname

    def get_absolute_url(self):
        return reverse('postFound-detail', kwargs={'pk': self.pk})

#เก็บข้อมูลสำหรับคนที่ส่งข้อมูลคนหายให้กับสื่อ
class Postmail(models.Model):
    realname = models.CharField(max_length=150, default='', verbose_name = "<font color='red'>ชื่อจริงและนามสกุล</font>")
    nickname = models.CharField(max_length=50, default='', verbose_name = "<font color='red'>ชื่อเล่น</font>")
    realnameEng = models.CharField(max_length=150, blank=True, null=True, verbose_name = "ชื่ออังกฤษ")
    age = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(100)], 
    blank=True, null=True, verbose_name = "<font color='red'>อายุ(ปี)</font>",
    help_text="กรอกอายุ 1- 100")

    nationality = models.CharField(max_length=10, default='', verbose_name = "<font color='red'>เชื้อชาติ</font>")
    lostday = models.CharField(max_length=10, blank=True, null=True, verbose_name = "วันที่หาย",
    help_text="กรอกวันที่ เช่น 21/01/2530",)
    lostTime = models.CharField(max_length=5, blank=True, null=True, verbose_name = "เวลาที่หาย",
    help_text="กรอกเวลา เช่น 12.00 , 19.30")
    lostWhere = models.CharField(max_length=100, blank=True, null=True, verbose_name = "สถานที่หาย")
    lostReason = models.CharField(max_length=200, blank=True, null=True, verbose_name = "เหตุผลที่หาย")
    identities = models.CharField(max_length=100, default='', verbose_name = "<font color='red'>ลักษณะพิเศษ</font>",
    help_text="ลักษณะพิเศษ เช่น มีไฝบนหน้า ใส่สร้องทอง ผิวคล้ำเป็นต้น")

    # image = models.ImageField(upload_to='images', blank=True, null=True, verbose_name = "รูปภาพ",
    # help_text="รูปภาพของผู้สูญหาย")
    image = CloudinaryField('รูปภาพ', blank=True, null=True)


    content = models.TextField(blank=True, null=True, verbose_name = "รายละเอียดเพิ่มเติม", 
    help_text="กรอกรายละเอียดเพิ่มเติม")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    fromEmail = models.CharField(max_length=150, default='')

    gender = models.CharField(max_length=5, default='', verbose_name = "<font color='red'>เพศ</font>")

    def __str__(self):
        return self.realname


#ส่วนของญาติผู้สูญหายกรอกข้อมูลลงระบบ
class Post(models.Model):
    # title = models.CharField(max_length=100, verbose_name = "<font color='red'>หัวข้อ</font>")
    realname = models.CharField(max_length=150, default='', verbose_name = "<font color='red'>ชื่อจริงและนามสกุล</font>")
    nickname = models.CharField(max_length=50, default='', verbose_name = "<font color='red'>ชื่อเล่น</font>")
    realnameEng = models.CharField(max_length=150, blank=True, null=True, verbose_name = "ชื่ออังกฤษ")
    age = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(100)], 
    blank=True, null=True, verbose_name = "<font color='red'>อายุ(ปี)</font>",
    help_text="กรอกอายุ 1- 100 (จำเป็นต้องกรอก)")

    nationality = models.CharField(max_length=10, default='', verbose_name = "<font color='red'>เชื้อชาติ</font>")
    lostday = models.CharField(max_length=10, blank=True, null=True, verbose_name = "วันที่หาย",
    help_text="กรอกวันที่ เช่น 21/01/2530",)
    lostTime = models.CharField(max_length=5, blank=True, null=True, verbose_name = "เวลาที่หาย",
    help_text="กรอกเวลา เช่น 12.00 , 19.30")
    lostWhere = models.CharField(max_length=100, blank=True, null=True, verbose_name = "สถานที่หาย")
    lostReason = models.CharField(max_length=200, blank=True, null=True, verbose_name = "เหตุผลที่หาย")
    identities = models.CharField(max_length=100, default='', verbose_name = "<font color='red'>ลักษณะพิเศษ</font>",
    help_text="ลักษณะพิเศษ เช่น มีไฝบนหน้า ใส่สร้องทอง ผิวคล้ำเป็นต้น")

    # image = models.ImageField(upload_to='images', blank=True, null=True, verbose_name = "รูปภาพ",
    # help_text="รูปภาพของผู้สูญหาย")
    image = CloudinaryField('รูปภาพ', blank=True, null=True)

    content = models.TextField(blank=True, null=True, verbose_name = "รายละเอียดเพิ่มเติม", 
    help_text="กรอกรายละเอียดเพิ่มเติม")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    gender = models.CharField(max_length=5, default='', verbose_name = "<font color='red'>เพศ</font>")

    
    telephone = models.CharField(max_length=10, default='', verbose_name = "<font color='red'>เบอร์โทรติดต่อกับผู้บันทึกข้อมูล</font>")
    email = models.CharField(max_length=100, default='', verbose_name = "<font color='red'>อีเมล์ของผู้บันทึกข้อมูล</font>")
    

    DATE_INPUT_FORMATS = ['%d-%m-%Y']

    def __str__(self):
        return self.realname

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

#ส่วนของผู้แจ้งเบาะแสกรอกข้อมูลเข้าไป
class PostFree(models.Model):
    title = models.CharField(max_length=100, default='', verbose_name = "<font color='red'>หัวข้อ</font>", 
    help_text="กรอกข้อมูลเช่น พบเจอเด็กหลง , พบเจอคนแก่อยู่ที่ถนน... เป็นต้น")

    # image = models.ImageField(upload_to='images2', blank=True, null=True, verbose_name = "รูปภาพ",
    # help_text="สำหรับใส่รูปภาพแกติทั่วไป เช่น รูปเด็กหลงทาง รูปคนแก่หาย เป็นต้น")
    # image2 = models.ImageField(upload_to='images2/imageSensitive', blank=True, null=True, verbose_name = "รูปภาพ (รูปที่ส่อถึงความรุนแรง)",
    # help_text="สำหรับใส่รูปภาพที่รุนแรง ไม่ดีต่อการเผยรูปนี้เป็นลำดับแรก รูปนี้จะโผล่ไปในข้อมูลภายในซึ่งญาติผู้สูญหายจะเห็นได้เท่านั้น เช่น รูปผู้เสียชีวิต เป็นต้น")
    image = CloudinaryField('รูปภาพ (สำหรับใส่รูปภาพแกติทั่วไป เช่น รูปเด็กหลงทาง รูปคนแก่หาย เป็นต้น)', blank=True, null=True)
    image2 = CloudinaryField('รูปภาพ2 (สำหรับใส่รูปภาพที่รุนแรง ไม่ต้องการเผยรูปนี้ในหน้าโชว์ข้อมูล เช่น รูปเสียชีวิตเป็นต้น)', blank=True, null=True)

    where = models.CharField(max_length=100, default='', verbose_name = "<font color='red'>สถานที่พบเจอ</font>", 
    help_text="กรอกข้อมูลเช่น พบเจอที่ราชดำเนิน เป็นต้น")
    content = models.TextField(verbose_name = "รายละเอียดเพิ่มเติม", help_text="กรุณากรอกข้อความให้ครบถ้วนเพื่อสิทธิประโยชน์ของท่านและสำหรับผู้แจ้งเบาะแส"
    , blank=True, null=True)
    identities = models.CharField(max_length=100, default='', verbose_name = "<font color='red'>ลักษณะพิเศษ</font>", 
    help_text="ลักษณะพิเศษ เช่น มีไฝบนหน้า ใส่สร้องทอง ผิวคล้ำเป็นต้น")

    email = models.CharField(max_length=100, blank=True, null=True, verbose_name = "อีเมล์",
    help_text="ส่วนของข่อมูลส่วนบุคคล กรอกอีเมล์สำหรับให้ญาติของผู้สูญหายสามารถติดต่อกลับได้")
    telephone = models.CharField(max_length=10, blank=True, null=True, verbose_name = "เบอร์โทรติดต่อของผู้บันทึกข้อมูล",
    help_text="ส่วนของข่อมูลส่วนบุคคล กรอกเบอร์โทรสำหรับให้ญาติของผู้สูญหายสามารถติดต่อกลับได้")
    
    date_posted = models.DateTimeField(default=timezone.now)

    gender = models.ManyToManyField(Gender, verbose_name = "<font color='red'>เพศ</font>")
    age = models.ManyToManyField(AgePeople, verbose_name = "<font color='red'>อายุ</font>")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

#ส่วนของญาติผู้สูญหายกรอกข้อมูลลงระบบ (ผู้มีความเสี่ยงจะสูญหาย)
class PostRisk(models.Model):
    realname = models.CharField(max_length=150, default='', verbose_name = "<font color='red'>ชื่อจริงและนามสกุล</font>")
    nickname = models.CharField(max_length=50, default='', verbose_name = "<font color='red'>ชื่อเล่น</font>")
    realnameEng = models.CharField(max_length=150, blank=True, null=True, verbose_name = "ชื่ออังกฤษ")
    age = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(100)],blank=True, null=True, 
    verbose_name = "<font color='red'>อายุ</font>")
    nationality = models.CharField(max_length=10, default='', verbose_name = "<font color='red'>เชื้อชาติ</font>")
    # lostday = models.IntegerField(blank=True, null=True, verbose_name = "วันที่หาย")
    # lostTime = models.IntegerField(blank=True, null=True, verbose_name = "เวลาที่หาย")
    # lostWhere = models.CharField(max_length=100, blank=True, null=True, verbose_name = "สถานที่ที่หาย")
    # lostReason = models.CharField(max_length=200, blank=True, null=True, verbose_name = "เหตุผลที่หาย")
    identities = models.CharField(max_length=100, default='', verbose_name = "<font color='red'>ลักษณะพิเศษ</font>",
    help_text="ลักษณะพิเศษ เช่น มีไฝบนหน้า ใส่สร้องทอง ผิวคล้ำเป็นต้น")

    # image = models.ImageField(upload_to='images3', blank=True, null=True, verbose_name = "รูปภาพ",
    # help_text="รูปภาพของผู้มีความเสี่ยงจะหาย")
    image = CloudinaryField('รูปภาพ', blank=True, null=True)

    content = models.TextField(blank=True, null=True, verbose_name = "รายละเอียดเพิ่มเติม", 
    help_text="กรอกรายละเอียดเพิ่มเติม")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    gender = models.CharField(max_length=5, default='', verbose_name = "<font color='red'>เพศ</font>")

    
    def __str__(self):
        return self.realname

    def get_absolute_url(self):
        return reverse('postRisk-detail', kwargs={'pk': self.pk})