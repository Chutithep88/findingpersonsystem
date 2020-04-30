# sendemail/forms.py
from django import forms
from django.forms import ModelForm
from .models import Dataemail

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True, label="อีเมล์ของผู้ใช้งานระบบ")
    subject = forms.CharField(required=True, label="หัวข้อ")
    message = forms.CharField(widget=forms.Textarea, required=True, label="ข้อความ")

class ContactForm2(ModelForm):
    subject = forms.CharField(required=True, label="หัวข้อ")
    from_email = forms.EmailField(required=True, label="อีเมล์ของผู้ใช้งานระบบ")
    message = forms.CharField(widget=forms.Textarea, required=True, label="ข้อความ")
    class Meta:
        model = Dataemail  # with attr somedata
        fields = (
            'subject', 
            'from_email',
            'message',
            )
        
