# -*- coding: utf-8 -*-
from django.conf import settings
from django import template
from django.utils.translation import get_language
from ..models import News

register = template.Library()
@register.inclusion_tag('news/tags/news_feed.html')
def news_feed(count=10):

    lang=get_language()[:2]
    news_list = list(News.objects.filter(publicated=True, lang=lang).order_by('-create_date')[:count])
    return ({
        'news_list': news_list,
        'MEDIA_URL': settings.MEDIA_URL
    })

