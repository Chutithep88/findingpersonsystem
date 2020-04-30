# sendemail/views.py
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm, ContactForm2
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.views.generic.edit import FormView
from .models import Dataemail,allemailtoadmin

class FormView(LoginRequiredMixin, CreateView):
    model = Dataemail
    form_class = ContactForm2
    template_name = "email.html"
    
    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        from_email = form.cleaned_data['from_email']
        message = form.cleaned_data['message']
        
        for user in allemailtoadmin.objects.all():
            recievers = []
            recievers.append(user.name)
            try:
                send_mail(subject, message, from_email, recievers)
            except BadHeaderError:
                return HttpResponse('เกิดข้อผิดพลาดขึ้น รอ Admin ตรวจสอบเพื่อปรับปรุง')
            return redirect('success')

        return super().form_valid(form)
    


# def emailView(request):
#     if request.method == 'GET':
#         form = ContactForm()
#     else:
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             from_email = form.cleaned_data['from_email']
#             message = form.cleaned_data['message']
#             try:
#                 send_mail(subject, message, from_email, ['betogetza@gmail.com'],fail_silently=False,)
#             except BadHeaderError:
#                 return HttpResponse('Invalid header found.')
#             return redirect('success')
#     return render(request, "email.html", {'form': form})


def successView(request):
    return render(request, "success.html")