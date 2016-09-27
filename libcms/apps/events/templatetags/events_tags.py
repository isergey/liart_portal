# -*- coding: utf-8 -*-
from datetime import date, datetime
import calendar
from django.db.models import Q
from django import template
from django.core.cache import cache
from ..models import Event
from ..frontend.forms import CalendarFilterForm, get_current_month_choice, get_current_year_choice

register = template.Library()


@register.inclusion_tag('events/tags/events_calendar.html', takes_context=True)
def events_calendar(context, y=0, m=0):
    request = context['request']

    if request.method == 'POST':
        form = CalendarFilterForm(request.POST)
        if form.is_valid():
            y = int(form.cleaned_data['year'])
            m = int(form.cleaned_data['month'])
    else:
        form = CalendarFilterForm(initial={'month': get_current_month_choice(),
                                           'year': get_current_year_choice()})
    today = date.today()
    year = today.year
    month = today.month

    if y: year = y
    if m: month = m
    weeks = calendar.monthcalendar(year, month)
    cache_key = 'events_y_m' + str(year) + str(month) + 'active=1'

    month_range = calendar.monthrange(year, month)
    start = datetime(year, month, 1)
    end = datetime(year, month, month_range[1] - 1, 23, 59, 59)
    extra = u'\
	YEAR(start_date) <= %(year)s AND MONTH(start_date) <= %(month)s\
	AND YEAR(end_date) >= %(year)s AND MONTH(end_date) >= %(month)s\
	AND active=1'\
      % {'year': int(year), 'month': int(month)}
	  
    query = Q(start_date__lte=start, end_date__gte=end, active=True)
    # events = cache.get(cache_key, [])
    events = Event.objects.extra(where=[extra])
    # events = Event.objects.filter(query)
    if not events:
        events = list(events)
        cache.set(cache_key, events)

    #events = Event.objects.filter(query)

    calendar_of_events = []
    for week in weeks:
        week_events = []
        for day in week:
            day_events = {
                'day': 0,
                'today': False,
                'events': [],
            }
            day_events['day'] = day
            if day == today.day and year == today.year and month == today.month:
                day_events['today'] = True
            print 'calendar', day
            for event in events:
                if event.start_date.day <= day and event.start_date.year <= year and event.start_date.year < year\
                        and event.end_date.day >= day and event.end_date.year >= year and event.end_date.month >= month:
                    day_events['events'].append({
                        'id': event.id,
                        #                        'title': event.title,
                        #                        'teaser': event.teaser
                    })
            week_events.append(day_events)
        calendar_of_events.append(week_events)
    # print calendar_of_events
    return {
        'calendar': calendar_of_events,
        'month': month,
        'year': year,
        'form': form
    }
