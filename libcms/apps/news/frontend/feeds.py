# -*- coding: utf-8 -*-

from django.utils.translation import get_language
from news.models import News



from django.contrib.syndication.views import Feed


class LatestEntriesFeed(Feed):
    title = u"Новости"
    link = "/news/"
    description = u"Новостная лента"

    def items(self):
        return index()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.teaser


def index():
    news_list =  News.objects.filter(publicated=True, lang=get_language()[:2]).order_by('-create_date')[:5]
    return news_list

#def show(request, id):
#    cur_language = translation.get_language()
#    news = get_object_or_404(News, id=id)
#    try:
#        content = NewsContent.objects.get(news=news, lang=cur_language[:2])
#    except Content.DoesNotExist:
#        content = None
#
#    return render(request, 'news/frontend/show.html', {
#        'news': news,
#        'content': content
#    })
