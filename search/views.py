from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from blog.models import PostFree, Gender, AgePeople,Post
from django.views.generic import TemplateView, ListView

#ค้นหาข้อมูลผู้สูญหาย
class SearchPageView(TemplateView):
    template_name = 'Post_search.html'

class SearchResultsView(ListView):
    model = Post
    template_name = 'Post_result.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(realname__icontains=query).order_by('-date_posted')
        return object_list





#ส่วนของค้นหาเบาะแส
def is_valid_queryparam(param):
    return param != '' and param is not None


def BootstrapFilterView(request):
    qs = PostFree.objects.all().order_by('-date_posted')
    categories = Gender.objects.all()
    age = AgePeople.objects.all()
    category = request.GET.get('category')
    ages = request.GET.get('ages')
    title_contains_query = request.GET.get('title_contains')
    
    

    if is_valid_queryparam(category) and category != 'Choose...':
        qs = qs.filter(gender__name=category)

    if is_valid_queryparam(ages) and ages != 'Choose...':
        qs = qs.filter(age__name=ages)
    
    if is_valid_queryparam(title_contains_query) and title_contains_query != '':
        qs = qs.filter(identities__icontains=title_contains_query)

    

    context = {
        'queryset': qs,
        'categories': categories,
        'age':age
    }
    return render(request, "bootstrap_form.html", context)

def resultView(request):
    qs = PostFree.objects.all().order_by('-date_posted')
    categories = Gender.objects.all()
    age = AgePeople.objects.all()
    category = request.GET.get('category')
    ages = request.GET.get('ages')
    title_contains_query = request.GET.get('title_contains')
    
    if is_valid_queryparam(category) and category != 'Choose...':
        qs = qs.filter(gender__name=category)

    if is_valid_queryparam(ages) and ages != 'Choose...':
        qs = qs.filter(age__name=ages)
    
    if is_valid_queryparam(title_contains_query) and title_contains_query != '':
        qs = qs.filter(identities__icontains=title_contains_query)

    

    context = {
        'queryset': qs,
        'categories': categories,
        'age':age
    }
    return render(request, "result.html", context)
    