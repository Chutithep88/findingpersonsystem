from django.urls import path,include
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    #ส่วนของแจ้งเบาะแส
    PostCreateFreeView,
    ThanksView,
    PostListFreeView,
    PostDetailFreeView,
    FirstView,
    #ส่วนค้นหาข้อมูลแจ้งเบาะแส
    SearchView,
    ResultSearchView,
    #ส่วนเพิ่มข้อมูลผู้มีความเสี่ยงจะหาย
    PostListRiskView,
    UserPostListRiskView,
    PostDetailRiskView,
    PostCreateRiskView,
    PostUpdateRiskView,
    PostDeleteRiskView,
    
    #เพิ่มข้อมูลผู้สูญหายและส่งเมล์ไปหาสื่อ
    PostCreateEmailSeView,
    PostCreateEmailSeView2,
    #Guide
    GuideView,

    #เมื่อคนหายถูกพบแล้ว
    FindsuccessView,
    PostfoundListView,
    UserPostfoundListView,
    PostfoundDetailView,
    PostfoundUpdateView,
    PostfoundDeleteView,

    #คนเสี่ยงจะหาย บันทึกไปยัง คนสูญหาย
    PostrisktopostView,

    #ส่วนของการแสดงข้อมูลว่าเคยโพสในคนหายหรือคนเสี่ยงจะหายไปแล้วเท่าไหร่
    UserPostView,
    UserPostRiskView,

    #ส่วนการแสดงองค์กรต่างๆที่สนับสุนการค้นหาคนหาย
    ShowOrganizationView,
)
from . import views
from blog import views
from django.contrib.auth.decorators import login_required #ทำให้ต้องล็อกอินก่อนถึงจะเข้าถึงข้อมูลได้

urlpatterns = [
    path('', views.FirstView, name='index'),
    path('home', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    #ส่วนของแจ้งเบาะแส
    path('post/newFree/', PostCreateFreeView.as_view(), name='post-createFree'),
    path('thanks', ThanksView.as_view(), name='thx'),
    path('homefree/', PostListFreeView.as_view(), name='blog-homefree'),
    path('postfree/<int:pk>/', PostDetailFreeView.as_view(), name='postfree-detail'),
    #ส่วนค้นหาข้อมูลเบาะแส
    # path('search/', SearchView.as_view(), name='search-page'), ไม่ใช้เนื่องจากทำตัวใหม่แล้ว ใน search.urls
    # path('result/', ResultSearchView.as_view(), name='resultsearch-page'), ไม่ใช้เนื่องจากทำตัวใหม่แล้ว ใน search.urls(ค้นหาและแสดงผลในหน้าเดียว)
    
    #ส่วนเพิ่มข้อมูลญาติผู้มีความเสี่ยงจะหาย
    path('homeRisk', PostListRiskView.as_view(), name='blog-homeRisk'),
    path('post/newRisk/', PostCreateRiskView.as_view(), name='post-createRisk'),
    path('postRisk/<int:pk>/', PostDetailRiskView.as_view(), name='postRisk-detail'),
    path('postRisk/<int:pk>/update/', PostUpdateRiskView.as_view(), name='postRisk-update'),
    path('postRisk/<int:pk>/delete/', PostDeleteRiskView.as_view(), name='postRisk-delete'),
    path('userRisk/<str:username>', UserPostListRiskView.as_view(), name='userRisk-posts'),

    #โพสข้อมูลผู้สูญหายแบบส่งEmail
    path('postmail2/', PostCreateEmailSeView.as_view(), name='post-mail2'),
    path('postmail/', PostCreateEmailSeView2.as_view(), name='post-mail'),

    #Guide
    path('guide/', GuideView.as_view(), name='guide'),

    #เมื่อคนหายถูกพบแล้ว
    path('post/<int:pk>/found/', FindsuccessView.as_view(), name='FindsuccessView'),

    #คนเสี่ยงจะหาย บันทึกไปยัง คนสูญหาย
    path('postRisk/<int:pk>/save/', PostrisktopostView.as_view(), name='postRisk-save'),
    path('homeFound', PostfoundListView.as_view(), name='blog-homeFound'),
    path('postFound/<int:pk>/', PostfoundDetailView.as_view(), name='postFound-detail'),
    path('postFound/<int:pk>/update/', PostfoundUpdateView.as_view(), name='postFound-update'),
    path('postFound/<int:pk>/delete/', PostfoundDeleteView.as_view(), name='postFound-delete'),
    path('userFound/<str:username>', UserPostfoundListView.as_view(), name='userFound-posts'),

    #ส่วนของการแสดงข้อมูลว่าเคยโพสในคนหายหรือคนเสี่ยงจะหายไปแล้วเท่าไหร่
    path('userpost/<str:username>', UserPostView.as_view(), name='posts-user'),
    path('userRiskpost/<str:username>', UserPostRiskView.as_view(), name='posts-userRisk'),

    #โหลดไฟล์ข้อมูลในระบบแบบ Excel
    path('export/excelUsers', views.export_users_xls, name='export_excelUsers'),
    path('export/excelPost', views.export_post_xls, name='export_excelPost'),
    path('export/excelPostRisk', views.export_postRisk_xls, name='export_excelPostRisk'),
    path('export/excelPostFree', views.export_postFree_xls, name='export_excelPostFree'),
    path('export/excelPostFound', views.export_postFound_xls, name='export_excelPostFound'),

    #เทสเอาไว้ปรับปรุงสำหรับ องค์กร ที่กด เจอแล้ว ในเมล์ เพื่อให้บันทึกว่าข้อมูลคนหายคนนั้นองค์กรเป็นคนเจอ
    path('export/excelPostExceptUser', views.export_PostExceptUser_xls, name='export_excelPostExceptUser'),

    #ส่วนโชว์องค์กรที่มีเมล์ที่สามารถส่งไปยังองค์กรเพื่อสนับสนุนการช่วยเหลือ
    path('showorganization', ShowOrganizationView.as_view(), name='showorganization'),

]
