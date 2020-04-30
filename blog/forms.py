# sendemail/forms.py
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from wtforms.fields.html5 import DateField
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import Post, PostRisk,allemail, PostFree

#สำหรับส่งเมล์และอื่นๆ
class Sendmail(forms.Form):
    subject = forms.CharField(required=True)
    from_email = forms.EmailField(required=True)
    realname = forms.CharField(required=True)
    nickname = forms.CharField(required=True)
    realnameEng = forms.CharField(required=True)
    age = forms.IntegerField(required=True)
    nationality = forms.CharField(required=True)
    lostday = forms.CharField(required=True)
    lostTime = forms.CharField(required=True)
    lostWhere = forms.CharField(required=True)
    lostReason = forms.CharField(required=True)
    identities = forms.CharField(required=True)
    image = forms.ImageField(required=False)
    content = forms.CharField(required=True)

    class Meta:
        model = Post  # with attr somedata
        fields = ('realname', 'author')

#บันทึกข้อมูลคนหายพร้อมกับส่งอีเมล์ไปยังสื่อด้วย
class Sendmail2(ModelForm):
    # subject = forms.CharField(required=True)
    # from_email = forms.EmailField(required=True)

    # realname = forms.CharField(required=True, label="<font color='red'>ชื่อจริงและนามสกุล</font>" )
    # nickname = forms.CharField(required=True, label="<font color='red'>ชื่อเล่น</font>" )
    # realnameEng = forms.CharField(required=False, label="ชื่ออังกฤษ" )
    # gender = forms.CharField(required=True, label="<font color='red'>เพศ</font>" )
    # age = forms.IntegerField(required=True, label="<font color='red'>อายุ</font>" )
    # nationality = forms.CharField(required=True, label="<font color='red'>เชื้อชาติ</font>" )
    # lostday = forms.CharField(required=False, label="วันที่ผู้สูญหายได้หายไป" )
    # lostTime = forms.CharField(required=False, label="เวลาที่หาย" )
    # lostWhere = forms.CharField(required=False, label="สถานที่ที่หาย" )
    # lostReason = forms.CharField(required=False, label="เหตุผลที่หาย" )
    # identities = forms.CharField(required=True, label="<font color='red'>ลักษณะพิเศษ</font>" )
    image = forms.ImageField(required=False, label="รูปภาพ" )
    # content = forms.CharField(required=False, label="รายละเอียด", widget=forms.Textarea)
    # telephone = forms.CharField(required=True, label="<font color='red'>เบอร์โทรศัพท์</font>" )
    # email = forms.CharField(required=True, label="<font color='red'>อีเมล์ของคุณ</font>" )

    # position = forms.CharField(required=False, label="ตำแหน่งขององค์กร(ส่วนนี้จะกรอกหรือไม่กรอ)" ,help_text="")
    # mail = forms.CharField(required=False, label="อีเมล์องค์กร" )
    # organization = forms.CharField(required=False, label="องค์กร(เช่น มูลนิธิกระจกเงา , กรมตำรวจ)" )
    # places = forms.CharField(required=False, label="สถานที่" )

    class Meta:
        model = Post  # with attr somedata
        fields = (
            'realname', 
            'nickname',
            'realnameEng',
            'gender',
            'age',
            'nationality',
            'lostday',
            'lostTime',
            'lostWhere',
            'lostReason',
            'identities',
            'image',
            'content',
            'telephone',
            'email',
            )
            

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk': self.pk})


#บันทึกข้อมูลคนหายพร้อมกับส่งอีเมล์ไปยังสื่อด้วย
class Sendmail3(ModelForm):
    # subject = forms.CharField(required=True)
    # from_email = forms.EmailField(required=True)
    # realname = forms.CharField(required=True)
    # nickname = forms.CharField(required=True)
    # realnameEng = forms.CharField(required=True)
    # age = forms.IntegerField(required=False)
    # nationality = forms.CharField(required=True)
    # lostday = forms.CharField(required=True)
    # lostTime = forms.CharField(required=True)
    # lostWhere = forms.CharField(required=True)
    # lostReason = forms.CharField(required=True)
    # identities = forms.CharField(required=True)
    # image = forms.ImageField(required=False)
    # content = forms.CharField(required=True)

    # fromEmail = forms.CharField(required=True, label="<font color='red'>อีเมล์ของคุณ</font>" )

    position = forms.CharField(required=True, label="ตำแหน่งขององค์กร")
    mail = forms.EmailField(required=True, label="อีเมล์องค์กร" )
    organization = forms.CharField(required=True, label="องค์กร(เช่น มูลนิธิกระจกเงา , กรมตำรวจ)" )
    places = forms.CharField(required=True, label="สถานที่" )

    class Meta:
        model = allemail  # with attr somedata
        fields = (
            'position', 
            'mail',
            'organization',
            'places',
          
            )
   

#แบบฟอร์มเมื่อคนหายเจอแล้ว กดจะบันทึกข้อมูลลงใน Postfound
class Postfoundform(ModelForm):
    # subject = forms.CharField(required=True)
    # from_email = forms.EmailField(required=True)
    # realname = forms.CharField(required=True)
    # nickname = forms.CharField(required=True)
    # realnameEng = forms.CharField(required=True)
    # age = forms.IntegerField(required=False)
    # nationality = forms.CharField(required=True)
    # lostday = forms.CharField(required=True)
    # lostTime = forms.CharField(required=True)
    # lostWhere = forms.CharField(required=True)
    # lostReason = forms.CharField(required=True)
    # identities = forms.CharField(required=True)
    # image = forms.ImageField(required=False)
    # content = forms.CharField(required=True)

    # image = forms.ImageField(required=False, label="รูปภาพ" )

    class Meta:
        model = Post  # with attr somedata
        fields = (
            'realname', 
            'nickname',
            'realnameEng',
            'gender',
            'age',
            'nationality',
            'lostday',
            'lostTime',
            'lostWhere',
            'lostReason',
            'lostReason',
            'identities',
            'image',
            'content',
            'telephone',
            'email',
            )

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

#form ของผู้ที่อยากเอาข้อมูลคนเสี่ยงจะหายไปเป็นคนหาย
class Postrisktopostform(ModelForm):
    # subject = forms.CharField(required=True)
    # from_email = forms.EmailField(required=True)
    # realname = forms.CharField(required=True)
    # nickname = forms.CharField(required=True)
    # realnameEng = forms.CharField(required=True)
    # age = forms.IntegerField(required=False)
    # nationality = forms.CharField(required=True)
    # lostday = forms.CharField(required=True)
    # lostTime = forms.CharField(required=True)
    # lostWhere = forms.CharField(required=True)
    # lostReason = forms.CharField(required=True)
    # identities = forms.CharField(required=True)
    # image = forms.ImageField(required=False)
    # content = forms.CharField(required=True)

    lostday = forms.CharField(required=False, label="วันที่หาย")
    lostTime = forms.CharField(required=False, label="เวลาที่หาย")
    lostWhere = forms.CharField(required=False, label="สถานที่หาย")
    lostReason = forms.CharField(required=False, label="เหตุผลที่หาย")

    telephone = forms.CharField(required=True, label="<font color='red'>เบอร์โทรติดต่อกับผู้บันทึกข้อมูล</font>")
    email = forms.CharField(required=False, label="อีเมล์ของผู้บันทึกข้อมูล")

    #image = forms.ImageField(required=False, label="รูปภาพ")

    class Meta:
        model = PostRisk  # with attr somedata
        fields = (
            'realname', 
            'nickname',
            'realnameEng',
            'gender',
            'age',
            'nationality',
            'identities',
            'image',
            'content',
            )

    def get_absolute_url(self):
        return reverse('postRisk-detail', kwargs={'pk': self.pk})
