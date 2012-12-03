# -*- encoding: utf-8 -*-
from django.shortcuts import urlresolvers
from django.conf import settings
from django.db import models
from django.db.models import Count
from datetime import datetime

NEWS_TYPE_CHOICES = (
    (0, u'Публичные'),
    (1, u'Профессиональные'),
    (2, u'Общие'),
)

class News(models.Model):
    show_avatar = models.BooleanField(verbose_name=u"Показывать аватарку", default=False)
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Дата создания", db_index=True)
    publicated = models.BooleanField(verbose_name=u'Опубликовано?', default=True, db_index=True)
    avatar_img_name = models.CharField(max_length=100, blank=True)
    lang = models.CharField(verbose_name=u"Язык", db_index=True, max_length=2, choices=settings.LANGUAGES, default=settings.LANGUAGES[0])
    title = models.CharField(verbose_name=u'Заглавие', max_length=512)
    teaser = models.CharField(verbose_name=u'Тизер', max_length=512, help_text=u'Краткое описание новости')
    content = models.TextField(verbose_name=u'Содержание новости')
    def get_absolute_url(self):
        return urlresolvers.reverse('news:frontend:show', args=[self.id])






