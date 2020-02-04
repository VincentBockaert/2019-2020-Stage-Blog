from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from .models import Blog

def index(request):
    # return render(request,'blog.html')
    latest_blog_posts_list = Blog.objects.order_by('-pub_date')
    context = {'latest_blog_posts_list': latest_blog_posts_list}
    return render(request, 'blog.html', context)

def detail(request, blog_id):
    return HttpResponse("You're looking at blog post %s." % blog_id)

