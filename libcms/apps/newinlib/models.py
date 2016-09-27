# -*- encoding: utf-8 -*-
import datetime
from django.shortcuts import reverse
from django.conf import settings
from django.db import models


class Item(models.Model):
    create_date = models.DateTimeField(default=datetime.datetime.now, verbose_name=u"Дата создания", db_index=True)
    publicated = models.BooleanField(verbose_name=u'Опубликовано?', default=True, db_index=True)
    #main = models.BooleanField(verbose_name=u'Установить в качестве главного анонса',default=False ,blank=True, db_index=True)
    avatar_img_name = models.CharField(max_length=100, blank=True)
    def get_absolute_url(self):
        return reverse('newinlib:frontend:show', args=[self.id])

#    def save(self):
#        if self.main:
#            if hasattr(self, 'id'):
#                items = list(Item.objects.filter(main=True).exclude(id=self.id)[0:1])
#            else:
#                items = list(Item.objects.filter(main=True)[0:1])
#
#            if items:
#                items[0].main=False
#                items[0].save()
#        super(Item, self).save()

class ItemContent(models.Model):
    item = models.ForeignKey(Item)
    lang = models.CharField(verbose_name=u"Язык", db_index=True, max_length=2, choices=settings.LANGUAGES)
    title = models.CharField(verbose_name=u'Заглавие', max_length=512)
    content = models.TextField(verbose_name=u'Содержание')
    class Meta:
        unique_together = (('item', 'lang'),)

