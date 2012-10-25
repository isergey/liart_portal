# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from common.pagination import get_page


from core.forms import LanguageForm
from ..models import News
from forms import NewsForm

@login_required
@permission_required_or_403('news.add_news')
def index(request):
    return redirect('news:administration:news_list')


@login_required
@permission_required_or_403('news.add_news')
def news_list(request):
    lang = request.GET.get('lang', 'ru')
    news_page = get_page(request, News.objects.filter(lang=lang).order_by('-create_date'))
    return render(request, 'news/administration/news_list.html', {
        'news_list': news_page.object_list,
        'news_page': news_page,
        'langs': settings.LANGUAGES
        })



@login_required
@permission_required_or_403('news.add_news')
@transaction.commit_on_success
def create_news(request):

    if request.method == 'POST':
        news_form = NewsForm(request.POST,prefix='news_form')

        if news_form.is_valid():
                news = news_form.save(commit=False)
                if 'news_form_avatar' in request.FILES:
                    avatar_img_name = handle_uploaded_file(request.FILES['news_form_avatar'])
                    news.avatar_img_name = avatar_img_name
                news.save()
                if 'save_edit' in request.POST:
                    return redirect('news:administration:edit_news', news.id)
                else:
                    return redirect('news:administration:news_list')
    else:
        news_form = NewsForm(prefix="news_form")

    return render(request, 'news/administration/create_news.html', {
        'news_form': news_form,
        })

@login_required
@permission_required_or_403('news.change_news')
@transaction.commit_on_success
def edit_news(request, id):
    news = get_object_or_404(News, id=id)
    if request.method == 'POST':
        news_form = NewsForm(request.POST,prefix='news_form', instance=news)

        if news_form.is_valid():
            news = news_form.save(commit=False)
            if 'news_form_avatar' in request.FILES:
                if news.avatar_img_name:
                    handle_uploaded_file(request.FILES['news_form_avatar'], news.avatar_img_name)
                else:
                    avatar_img_name = handle_uploaded_file(request.FILES['news_form_avatar'])
                    news.avatar_img_name = avatar_img_name
            news.save()
            if 'save_edit' in request.POST:
                return redirect('news:administration:edit_news', news.id)
            else:
                return redirect('news:administration:news_list')
    else:
        news_form = NewsForm(prefix="news_form", instance=news)
    return render(request, 'news/administration/edit_news.html', {
        'news_form': news_form,
        })


@login_required
@permission_required_or_403('news.delete_news')
@transaction.commit_on_success
def delete_news(request, id):
    news = get_object_or_404(News, id=id)
    news.delete()
    delete_avatar(news.avatar_img_name)
    return redirect('news:administration:news_list')




import os
import Image
import uuid
from datetime import datetime
#def handle_uploaded_file(f, old_name=None):
#    upload_dir = settings.MEDIA_ROOT + 'uploads/newsavatars/'
#    now = datetime.now()
#    dirs = [
#        upload_dir,
#        upload_dir  + str(now.year) + '/',
#        upload_dir  + str(now.year) + '/' + str(now.month) + '/',
#        ]
#    for dir in dirs:
#        if not os.path.isdir(dir):
#            os.makedirs(dir, 0744)
#    size = 147, 110
#    if old_name:
#        name = old_name
#    else:
#        name = str(now.year) + '/' + str(now.month) + '/' + uuid.uuid4().hex + '.jpg'
#    path = upload_dir + name
#    with open(path, 'wb+') as destination:
#        for chunk in f.chunks():
#            destination.write(chunk)
#    im = Image.open(path)
#    im = im.resize(size, Image.ANTIALIAS)
#    im.save(path, "JPEG",  quality=95)
#    return name


def handle_uploaded_file(f, old_name=None):
    upload_dir = settings.MEDIA_ROOT + 'uploads/newsavatars/'
    now = datetime.now()
    dirs = [
        upload_dir,
        upload_dir  + str(now.year) + '/',
        upload_dir  + str(now.year) + '/' + str(now.month) + '/',
        ]
    for dir in dirs:
        if not os.path.isdir(dir):
            os.makedirs(dir, 0744)
    size = 147, 110
    if old_name:
        name = old_name
    else:
        name = str(now.year) + '/' + str(now.month) + '/' + uuid.uuid4().hex + '.jpg'
    path = upload_dir + name
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    im = Image.open(path)
    image_width = im.size[0]
    image_hight = im.size[1]
    image_ratio = float(image_width) / image_hight

    box = [0, 0, 0, 0]
    if image_ratio <= 1:
        new_hight = int(image_width / 1.333)
        vert_offset = int((image_hight - new_hight) / 2)
        box[0] = 0
        box[1] = vert_offset
        box[2] = image_width
        box[3] = vert_offset + new_hight
    else:
        new_width = image_hight * 1.333
        if new_width > image_width:
            new_width = image_width
            new_hight = int(new_width / 1.333)
            vert_offset = int((image_hight - new_hight) / 2)
            box[0] = 0
            box[1] = vert_offset
            box[2] = new_width
            box[3] = vert_offset + new_hight
        else:
            gor_offset = int((image_width - new_width) / 2)
            box[0] = gor_offset
            box[1] = 0
            box[2] = int(gor_offset + new_width)
            box[3] = image_hight

    im = im.crop(tuple(box))

    final_hight = 110
    image_ratio = float(im.size[0]) / im.size[1]
    final_width = int((image_ratio * final_hight))
    im = im.resize((final_width, final_hight), Image.ANTIALIAS)
    im.save(path, "JPEG",  quality=95)
    return name

def delete_avatar(name):
    upload_dir = settings.MEDIA_ROOT + 'uploads/newsavatars/'
    if os.path.isfile(upload_dir + name):
        os.remove(upload_dir + name)
