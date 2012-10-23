# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.utils import translation
from django.utils.translation import get_language
from django.db.models import Q
from common.pagination import get_page
from ..models import News



def index(request):
    news_page = get_page(request, News.objects.filter(publicated=True, lang=get_language()[:2]).order_by('-create_date'))

    return render(request, 'news/frontend/list.html', {
        'news_list': news_page.object_list,
        'news_page': news_page,
        })

def show(request, id):
    try:
        news = News.objects.get(publicated=True,id=id)
    except News.DoesNotExist:
        raise Http404()


    return render(request, 'news/frontend/show.html', {
        'news': news,
    })

