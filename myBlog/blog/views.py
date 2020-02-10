from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import markdown
# Create your views here.

from .models import Blog

@login_required
def index(request):    
    latest_blog_posts_list = Blog.objects.order_by('-pub_date')
    context = {'latest_blog_posts_list': latest_blog_posts_list, 'title': 'Blog Index'}
    return render(request, 'blog/index.html', context)

@login_required
def detail(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    content = markdown.markdown(blog.content) # 'renders' the html
    context = {'content': content, 'title': blog.title, 'author': blog.author, 'pub_date': blog.pub_date, 'last_edited_date': blog.last_edited_date}
    return render(request,'blog/details.html',context=context)
