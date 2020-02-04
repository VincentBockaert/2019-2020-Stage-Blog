from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Blog

class LatestPostsFeed(Feed):
    title = "Blog stage posts feed"
    link = "/feed/"
    description = "Updates on changes and additions to the internship blog."

    def items(self):
        return Blog.objects.order_by('-pub_date')[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.description
    
    def item_link(self, item):
        return reverse('blog_detail',args=[item.pk])