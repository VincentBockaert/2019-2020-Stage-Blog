from django.shortcuts import render
from django.http import HttpResponse
import markdown
# Create your views here.

from .models import Blog


def index(request):
    # return render(request,'blog.html')
    latest_blog_posts_list = Blog.objects.order_by('-pub_date')
    context = {'latest_blog_posts_list': latest_blog_posts_list, 'title': 'Blog Index'}
    return render(request, 'blog/index.html', context)

def detail(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    content = markdown.markdown(blog.content) # 'renders' the html
    context = {'content': content, 'title': blog.title, 'author': blog.author, 'pub_date': blog.pub_date, 'last_edited_date': blog.last_edited_date}
    return render(request,'blog/details.html',context=context)
