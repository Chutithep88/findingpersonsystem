from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)

from django.views.generic.edit import FormView


from .models import Post, PostFree, PostRisk, Postmail, Gender, AgePeople, Postfound, allemail
from django.urls import reverse_lazy # new
from django.db.models import Q # new
from django.contrib.auth.decorators import login_required #new3
from django.core.paginator import Paginator

# sendemail/views.py
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import Sendmail,Sendmail2, Postfoundform, Postrisktopostform, Sendmail3

from django.conf import settings
from django.template.loader import get_template

from django.template import Context, loader

import xlwt

from dateutil import parser as dateutil_parser

import datetime

from django.contrib import auth

def home(request):
    context = {
        'posts': Post.objects.all()
    
    }
    return render(request, 'blog/home.html', context)


class GuideView(TemplateView):
    template_name = 'blog/guide.html'  # <app>/<model>_<viewtype>.html

# class FirstView(ListView): 
#     model = Post
#     template_name = 'blog/index.html' 
#     context_object_name = 'posts'
#     ordering = ['-date_posted']
#     paginate_by = 3

def FirstView(request): #เพิ่มเข้ามาทำหน้าแรกและเพิ่มเนื้อหาคนหายนิดหน่อย
    posts = Post.objects.all().order_by('-date_posted')[:3]
    postfree = Postfound.objects.all().order_by('-date_posted')[:3]
    context={
            'posts':posts,
            'postfree':postfree,
            }
    
    return render(request, 'blog/index.html', context)


class ShowOrganizationView(ListView):
    model = allemail
    template_name = 'blog/showorganization.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 20

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
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
        ]
    

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = [
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
        ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/home'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


#ส่วนของการแจ้งเบาะแส
class PostCreateFreeView(CreateView):
    model = PostFree
    fields = [
        'title',
        'gender',
        'age',
        'image',
        'image2',
        'where',
        'content',
        'identities',
        'email',
        'telephone',
        ]
    success_url = reverse_lazy('thx')

class ThanksView(TemplateView):
    template_name = 'blog/thanksforpost.html'  # <app>/<model>_<viewtype>.html


class PostListFreeView(ListView):
    model = PostFree
    template_name = 'blog/homefree.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'postsfree'
    ordering = ['-date_posted']
    paginate_by = 5


class PostDetailFreeView(DetailView):
    model = PostFree

#ส่วนของการค้นหาข้อมูลเบาะแส

class SearchView(TemplateView):
    template_name = 'blog/searchfree1.html'  # <app>/<model>_<viewtype>.html

class ResultSearchView(ListView):
    model = PostFree
    template_name = 'blog/searchfree2.html'
    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = PostFree.objects.filter(
            Q(title__icontains=query) | Q(identities__icontains=query)
        )
        return object_list


#ส่วนของส่งข้อมูลญาติผู้มีความเสี่ยงจะหาย PostRisk
class PostListRiskView(ListView):
    model = PostRisk
    template_name = 'blog/homeRisk.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListRiskView(ListView):
    model = PostRisk
    template_name = 'blog/userRisk_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'postsRisk'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return PostRisk.objects.filter(author=user).order_by('-date_posted')


class PostDetailRiskView(DetailView):
    model = PostRisk


class PostCreateRiskView(LoginRequiredMixin, CreateView):
    model = PostRisk
    fields = [
        'realname',
        'nickname',
        'realnameEng',
        'gender',
        'age',
        'nationality',
        'identities',
        'image',
        'content',
        ]
    

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostUpdateRiskView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PostRisk
    fields = [
        'realname',
        'nickname',
        'realnameEng',
        'gender',
        'age',
        'nationality',
        'identities',
        'image',
        'content',
        ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteRiskView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PostRisk
    success_url = '/homeRisk'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

#โพสข้อมูลผู้สูญหายและส่งเมล์ไปหาสื่อด้วย
class PostCreateEmailSeView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = [
    #     'realname',
    #     'nickname',
    #     'realnameEng',
    #     'gender',
    #     'age',
    #     'nationality',
    #     'lostday',
    #     'lostTime',
    #     'lostWhere',
    #     'lostReason',
    #     'identities',
    #     'image',
    #     'content',
    #     'telephone',
    #     'email',
    #     ]
    form_class = Sendmail2
    template_name = "post_formEmail.html"

    def form_valid(self, form):
        #ใช้บันทึก author_id ใน Post
        form.instance.author = self.request.user

        realname = form.cleaned_data['realname']
        nickname = form.cleaned_data['nickname']
        realnameEng = form.cleaned_data['realnameEng']
        gender = form.cleaned_data['gender']
        age = form.cleaned_data['age']
        nationality = form.cleaned_data['nationality']
        lostday = form.cleaned_data['lostday']
        lostTime = form.cleaned_data['lostTime']
        lostWhere = form.cleaned_data['lostWhere']
        lostReason = form.cleaned_data['lostReason']
        identities = form.cleaned_data['identities']
        image = form.cleaned_data['image']
        content = form.cleaned_data['content']
        telephone = form.cleaned_data['telephone']
        fromEmail = form.cleaned_data['email']
        userid = self.request.user.pk
        

        # obj2save = Post(
        #         realname = realname88, 
        #         nickname = nickname88, 
        #         realnameEng = realnameEng88,
        #         gender = gender88,
        #         age = age88,
        #         nationality = nationality88,
        #         lostday = lostday88,
        #         lostTime = lostTime88,
        #         lostWhere = lostWhere88,
        #         lostReason = lostReason88,
        #         identities = identities88,
        #         image = image88,
        #         content = content88,
        #         telephone = telephone88,
        #         email = fromEmail88,
        #         author_id= userid,)

        #obj2save.save()
        
        
        authorname = self.request.user.username #ดึงข้อมูลชื่อของ user ในตอนนี้เพื่อใช้ในการทำลิ้งให้องค์กรเปิดดูข้อมูลคนสูญหายได้

       
        for user in allemail.objects.all():
            recievers = []
            recievers.append(user.mail)

            position = []
            position.append(user.position)

            organization = []
            organization.append(user.organization)

            places = []
            places.append(user.places)

            context = {
                    'realname': realname,
                    'nickname': nickname,
                    'realnameEng': realnameEng,
                    'gender': gender,
                    'age': age,
                    'nationality': nationality,
                    'lostday': lostday,
                    'lostTime': lostTime,
                    'lostWhere': lostWhere,
                    'lostReason': lostReason,
                    'identities': identities,
                    'image': image,
                    'content': content,
                    'fromEmail': fromEmail,
                    'authorname': authorname,
                    'position': position,
                    'organization': organization,
                    'places': places,
                }

            contact_message = get_template('contact_message.html').render(context)

            send_mail(realname, contact_message, fromEmail, recievers)

        #อาจเพราะ Createview มองว่าต้องบันทึกข้อมูลได้แค่อย่างใดอย่างหนึ่ง เลยทำให้ต้องเอาส่วนบันทึกข้อมูลลง Postmail ออกก่อนไม่งั้น
        #ไม่งั้นมันจะไม่บันทึกลง Post ได้แค่บันทึกลง Postmail เท่านั้น
        # objsave = Postmail(
        #         realname = realname, 
        #         nickname = nickname, 
        #         realnameEng = realnameEng,
        #         gender = gender,
        #         age = age,
        #         nationality = nationality,
        #         lostday = lostday,
        #         lostTime = lostTime,
        #         lostWhere = lostWhere,
        #         lostReason = lostReason,
        #         identities = identities,
        #         image = image,
        #         content = content,
        #         fromEmail= fromEmail,
        #         author_id= userid,)

        # objsave.save()

        return super().form_valid(form)


class PostCreateEmailSeView2(LoginRequiredMixin, CreateView):
    model = allemail
    form_class = Sendmail3
    template_name = "post_formEmail2.html"

    def form_valid(self, form):
        position = form.cleaned_data['position']
        mail = form.cleaned_data['mail']
        organization = form.cleaned_data['organization']
        places = form.cleaned_data['places']

            
        objsave = allemail(
                position = position, 
                mail = mail,
                organization = organization,
                places = places,
                )


        objsave.save()

        return redirect('post-mail2')
       
        return super().form_valid(form)
        

    


# def emailView(request):
#     if request.method == 'GET':
#         form = Sendmail()
#     else:
#         form = Sendmail(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             from_email = form.cleaned_data['from_email']
#             realname = form.cleaned_data['realname']
#             nickname = form.cleaned_data['nickname']
#             realnameEng = form.cleaned_data['realnameEng']
#             age = form.cleaned_data['age']
#             nationality = form.cleaned_data['nationality']
#             lostday = form.cleaned_data['lostday']
#             lostTime = form.cleaned_data['lostTime']
#             lostWhere = form.cleaned_data['lostWhere']
#             lostReason = form.cleaned_data['lostReason']
#             identities = form.cleaned_data['identities']
#             image = form.cleaned_data['image']
#             content = form.cleaned_data['content']
            
#             objsave = Post(
#                 realname = realname, 
#                 nickname = nickname, 
#                 realnameEng = realnameEng,
#                 age = age,
#                 nationality = nationality,
#                 lostday = lostday,
#                 lostTime = lostTime,
#                 lostWhere = lostWhere,
#                 lostReason = lostReason,
#                 identities = identities,
#                 image = image,
#                 content = content,
#                 author_id = author,
#                 )

            

#             objsave.save()

#             context = {
#                 'user': subject,
#                 'email': from_email,
#             }

#             contact_message = get_template('contact_message.txt').render(context)

#             try:
#                 send_mail(subject, contact_message, from_email, ['admin@example.com'])
#             except BadHeaderError:
#                 return HttpResponse('Invalid header found.')
#             return redirect('success')
#     return render(request, "post_formEmail.html", {'form': form})

# def successView(request):
#     return HttpResponse('Success! Thank you for your message.')

#ส่งข้อมูลคนหายไปเก็บไว้ใน Postfound
class FindsuccessView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = Postfoundform
    # fields = [
    #     'realname',
    #     'nickname',
    #     'realnameEng',
    #     'age',
    #     'nationality',
    #     'lostday',
    #     'lostTime',
    #     'lostWhere',
    #     'lostReason',
    #     'identities',
    #     'image',
    #     'content',
    #     ]


    def form_valid(self, form):
        form.instance.author = self.request.user

        realname = self.request.POST.get('realname')
        nickname = self.request.POST.get('nickname')
        realnameEng = self.request.POST.get('realnameEng')
        gender = self.request.POST.get('gender')
        age = self.request.POST.get('age')
        nationality = self.request.POST.get('nationality')
        lostday = self.request.POST.get('lostday')
        lostTime = self.request.POST.get('lostTime')
        lostWhere = self.request.POST.get('lostWhere')
        lostReason = self.request.POST.get('lostReason')
        identities = self.request.POST.get('identities')
        content = self.request.POST.get('content')
        image = form.cleaned_data['image']
        userid = self.request.user.pk
        telephone = self.request.POST.get('telephone')
        email = self.request.POST.get('email')

        pri = self.kwargs['pk'] #เก็บค่า pk ในหน้านี้เพื่อไว้ใช้ในการลบข้อมูล

        objsave = Postfound(
                realname = realname, 
                nickname = nickname, 
                realnameEng = realnameEng,
                gender = gender,
                age = age,
                nationality = nationality,
                lostday = lostday,
                lostTime = lostTime,
                lostWhere = lostWhere,
                lostReason = lostReason,
                identities = identities,
                image = image,
                content = content,
                author_id= userid,
                telephone = telephone,
                email = email,
                )

    
        try:
            objsave.save() #บันทึกข้อมูลลงในคนหายเจอตัวแล้ว
            Post.objects.filter(id=pri).delete() #ลบข้อมูลคนสูญหายหลังจากบันทึกข้อมูลไปยังพบเจอคนหายแล้ว
        except BadHeaderError:
            return HttpResponse('เกิดข้อผิดพลาดขึ้นในส่วนของการเก็บข้อมูล.')
        template = loader.get_template("blog/Thanksforsavepostfound.html")
        return HttpResponse(template.render())


        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostfoundListView(ListView):
    model = Postfound
    template_name = 'blog/homeFound.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'postsfound'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostfoundListView(ListView):
    model = Postfound
    template_name = 'blog/userFound_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'postsfound'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Postfound.objects.filter(author=user).order_by('-date_posted')


class PostfoundDetailView(DetailView):
    model = Postfound

class PostfoundUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Postfound
    fields = [
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
        ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostfoundDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Postfound
    success_url = '/homeFound'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

#คนเสี่ยงหายต้องการเก็บข้อมูลไว้ในคนหาย
class PostrisktopostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PostRisk
    form_class = Postrisktopostform
    # fields = [
    #     'realname',
    #     'nickname',
    #     'realnameEng',
    #     'age',
    #     'nationality',
    #     'lostday',
    #     'lostTime',
    #     'lostWhere',
    #     'lostReason',
    #     'identities',
    #     'image',
    #     'content',
    #     ]

    def form_valid(self, form):
        form.instance.author = self.request.user

        realname = self.request.POST.get('realname')
        nickname = self.request.POST.get('nickname')
        realnameEng = self.request.POST.get('realnameEng')
        gender = self.request.POST.get('gender')
        age = self.request.POST.get('age')
        nationality = self.request.POST.get('nationality')
        lostday = self.request.POST.get('lostday')
        lostTime = self.request.POST.get('lostTime')
        lostWhere = self.request.POST.get('lostWhere')
        lostReason = self.request.POST.get('lostReason')
        identities = self.request.POST.get('identities')
        content = self.request.POST.get('content')

        lostday = form.cleaned_data['lostday']
        lostTime = form.cleaned_data['lostTime']
        lostWhere = form.cleaned_data['lostWhere']
        image = form.cleaned_data['image']
        userid = self.request.user.pk

        telephone = form.cleaned_data['telephone']
        email = form.cleaned_data['email']
        
        pri = self.kwargs['pk'] #เก็บค่า pk ในหน้านี้เพื่อไว้ใช้ในการลบข้อมูล

        objsave = Post(
                realname = realname, 
                nickname = nickname, 
                realnameEng = realnameEng,
                gender = gender,
                age = age,
                nationality = nationality,
                lostday = lostday,
                lostTime = lostTime,
                lostWhere = lostWhere,
                lostReason = lostReason,
                identities = identities,
                image = image,
                content = content,
                author_id= userid,
                telephone = telephone,
                email = email,
                )

        objsave.save()
    
        try:
            objsave.save() #บันทึกข้อมูลลงคนสูญหาย
            PostRisk.objects.filter(id=pri).delete() #ลบข้อมูลคนเสี่ยงจะหายหลังจากบันทึกข้อมูลไปยังคนสูญหายแล้ว
        except BadHeaderError:
            return HttpResponse('เกิดข้อผิดพลาดขึ้นในส่วนของการเก็บข้อมูล.')
        template = loader.get_template("blog/Thanksforsavepost.html")
        return HttpResponse(template.render())


        return super(PostrisktopostView, self).form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


#ส่วนของการแสดงข้อมูลว่าเคยโพสในคนหายหรือคนเสี่ยงจะหายไปแล้วเท่าไหร่
class UserPostView(ListView):
    model = Post
    template_name = 'blog/userpostview.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'postsposts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class UserPostRiskView(ListView):
    model = PostRisk
    template_name = 'blog/userpostriskview.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'postspostsRisk'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return PostRisk.objects.filter(author=user).order_by('-date_posted')


#ไฟล์Excel ข้อมูลของ User ในระบบ
def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id','Username', 'First Name', 'Last Name', 'Email Address', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = User.objects.all().values_list('id','username', 'first_name', 'last_name', 'email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

#ไฟล์ Excel ข้อมูลคนหายในระบบ
def export_post_xls(request):
    response = HttpResponse(content_type='application/ms-excel;charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Post.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Post Data') # this will make a sheet named Post Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'ชื่อ-นามสกุล', 'ชื่อเล่น', 'ชื่อ-นามสกุล(ภาษาอังกฤษ)', 'อายุ', 
            'เชื้อชาติ','วันที่หาย','เวลาที่หาย','สถานที่หาย','เหตุผลที่หาย',
            'ลักษณะพิเศษ','รายละเอียดเพิ่มเติม','ผู้บันทึกข้อมูล','วันที่บันทึกข้อมูล']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Post.objects.all().values_list('id', 'realname', 'nickname', 'realnameEng', 'age', 'nationality',
             'lostday','lostTime','lostWhere','lostReason','identities','content', 'author','date_posted')
     
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

#ไฟล์ Excel ข้อมูลคนเสี่ยงจะหายในระบบ
def export_postRisk_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="PostRisk.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('PostRisk Data') # this will make a sheet named PostRisk Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'ชื่อ-นามสกุล', 'ชื่อเล่น', 'ชื่อ-นามสกุล(ภาษาอังกฤษ)', 'อายุ', 
            'เชื้อชาติ','ลักษณะพิเศษ','รายละเอียดเพิ่มเติม','ผู้บันทึกข้อมูล','วันที่บันทึกข้อมูล']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = PostRisk.objects.all().values_list('id', 'realname', 'nickname', 'realnameEng', 'age', 'nationality',
             'identities','content', 'author','date_posted')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

#ไฟล์ Excel ข้อมูลเบาะแสในระบบ
def export_postFree_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="PostFree.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('PostFree Data') # this will make a sheet named PostFree Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'หัวเรื่อง', 'สถานที่พบเจอ', 'รายละเอียดเพิ่มเติม', 'ลักษณะพิเศษ', 
            'อีเมล์ของผู้ส่งข้อมูล','เบอร์โทรศัพท์','เพศ','อายุ','วันที่บันทึกข้อมูล' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = PostFree.objects.all().values_list('id', 'title', 'where', 'content','identities','email',
                                        'telephone','gender','age','date_posted')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

#ไฟล์ Excel ข้อมูลผู้ที่ถูกพบเจอตัวแล้วในระบบ
def export_postFound_xls(request):
    response = HttpResponse(content_type='application/ms-excel;charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="PostFound.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('PostFound Data') # this will make a sheet named PostFound Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'ชื่อ-นามสกุล', 'ชื่อเล่น', 'ชื่อ-นามสกุล(ภาษาอังกฤษ)', 'อายุ', 
            'เชื้อชาติ','วันที่หาย','เวลาที่หาย','สถานที่หาย','เหตุผลที่หาย',
            'ลักษณะพิเศษ','รายละเอียดเพิ่มเติม','ผู้บันทึกข้อมูล','วันที่บันทึกข้อมูล']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Postfound.objects.all().values_list('id', 'realname', 'nickname', 'realnameEng', 'age', 'nationality',
             'lostday','lostTime','lostWhere','lostReason','identities','content', 'author','date_posted')
     
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response



#ไฟล์Excel ข้อมูลของ User เฉพาะคนที่ล็อกอิน(ใช้สำหรับ ในการโหลดข้อมูลเจอคนหายขององค์กรด้วย เป็นกรณีศึกษา โหลดของข้อมูลผู้สูญหายเฉพาะเจาะจงได้แล้ว)
#สามารถนำไปปรับเปลี่ยนเป็นองค์กรไหนเจอคนหายแล้วจะบันทึกไว้ได้ (ต้องคิดLogic อีกทีสำหรับขั้นตอนให้องค์กรกด เจอแล้ว ในเมล์แล้ว)
def export_PostExceptUser_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="PostExcepUser.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('PostExcepUser Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'ชื่อ-นามสกุล', 'ชื่อเล่น', 'ชื่อ-นามสกุล(ภาษาอังกฤษ)', 'อายุ', 
            'เชื้อชาติ','วันที่หาย','เวลาที่หาย','สถานที่หาย','เหตุผลที่หาย',
            'ลักษณะพิเศษ','รายละเอียดเพิ่มเติม','ผู้บันทึกข้อมูล','วันที่บันทึกข้อมูล']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()


    
    userid = User.objects.get(id=request.user.pk)
    

    rows = Post.objects.filter(author_id=userid).values_list('id', 'realname', 'nickname', 'realnameEng', 'age', 'nationality',
             'lostday','lostTime','lostWhere','lostReason','identities','content', 'author','date_posted')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response