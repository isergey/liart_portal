# -*- coding: utf-8 -*-

from django.utils.translation import get_language
from ..models import Item, ItemContent



from django.contrib.syndication.views import Feed


class LatestEntriesFeed(Feed):
    title = u"Новые поступления"
    link = "/newinlib/"
    description = u"Лента новых поступлений"

    def items(self):
        return index()

    def item_title(self, item):
        item_content = getattr(item, 'item_content', None)
        if not item_content:
            return u''
        return item_content.title

    def item_description(self, item):
        item_content = getattr(item, 'item_content', None)
        if not item_content:
            return u''


def index():
    items_list =  Item.objects.filter(publicated=True).order_by('-create_date')[:5]

    item_contents = list(ItemContent.objects.filter(item__in=list(items_list), lang=get_language()[:2]))

    t_dict = {}
    for item in items_list:
        t_dict[item.id] = {'item': item}

    for item_content in item_contents:
        t_dict[item_content.item_id]['item'].item_content = item_content

    return items_list


