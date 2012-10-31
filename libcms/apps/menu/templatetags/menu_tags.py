# -*- coding: utf-8 -*-
from django.core.cache import cache
from django import template
from django.utils import translation
from django.utils.translation import to_locale, get_language
from ..models import Menu, MenuItemTitle

register = template.Library()

@register.inclusion_tag('menu/tags/drow_menu_horizontal.html', takes_context=True)
def drow_menu_horizontal  (context, menu_slug):
    return build_menu(context, menu_slug)

@register.inclusion_tag('menu/tags/drow_menu_vertical.html', takes_context=True)
def drow_menu_vertical  (context, menu_slug):
    return build_menu(context, menu_slug)


def build_menu(context, menu_slug):
    lang=get_language()[:2]
    menu = cache.get('menu_' + menu_slug + lang, None)
    if not menu:
        try:
            menu = Menu.objects.get(slug=menu_slug)
            cache.set('menu_' + menu_slug + lang, menu)
        except Menu.DoesNotExist:
            return ({
                        'menu': None
                    })

    path = context['request'].META['PATH_INFO']
    host =  context['request'].META['HTTP_HOST']
    nodes = cache.get('menu_nodes' + menu_slug + lang, None)
    if not nodes:
        nodes = list(menu.root_item.get_descendants().exclude(show=False))
        cache.set('menu_nodes' + menu_slug + lang, nodes)


    item_titles = cache.get('menu_item_titles' + menu_slug + lang, None)
    if not item_titles:
        item_titles = list(MenuItemTitle.objects.filter(item__in=nodes, lang=lang))
        cache.set('menu_item_titles' + menu_slug + lang, item_titles)

    nd = {}
    for node in nodes:
        nd[node.id] = node

    search_active = True # искать активный пункт
    for item_title in item_titles:
        if search_active:
            if path[-1] != u'/':
                path += u'/'
            
            if item_title.url == path or \
               item_title.url == (host + path) or \
               item_title.url == ('http://' + host + path) or \
               item_title.url == ('https://' + host + path) :
#            if item_title.url.startswith(path) or\
#               item_title.url.startswith(host + path) or\
#               item_title.url.startswith('http://' + host + path) or\
#               item_title.url.startswith('https://' + host + path) :
                node = nd[item_title.item_id]
                node.is_active = True
                search_active = False
                parent_id = node.parent_id

                while parent_id and parent_id in nd:
                    parent_node = nd[parent_id]
                    parent_node.is_active = True
                    parent_id = parent_node.parent_id

        nd[item_title.item_id].item_title = item_title

    if not item_titles:
        nodes = []
    return ({
                'nodes': nodes,
                'menu': menu,
                'path': path
            })