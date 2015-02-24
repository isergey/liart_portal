# -*- coding: utf-8 -*-
from datetime import date
import calendar
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
    events = cache.get(cache_key, [])

    if not events:
        first_month_day, last_month_day = calendar.monthrange(year, month)
        from_date = date(year=year, month=month, day=first_month_day)
        to_date = date(year=year, month=month, day=last_month_day)
        events = list(Event.objects.filter(start_date__gte=from_date, start_date__lte=to_date, active=True))
        cache.set(cache_key, events)

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
            if day == today.day and year == today.year and month == today.month: day_events['today'] = True
            for event in events:
                if event.start_date.day == day:
                    day_events['events'].append({
                        'id': event.id,
                        #                        'title': event.title,
                        #                        'teaser': event.teaser
                    })
            week_events.append(day_events)
        calendar_of_events.append(week_events)
    return {'calendar': calendar_of_events,
            'month': month,
            'year': year,
            'form': form}