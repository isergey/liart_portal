# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
#    (r'^admin/', include('pages.administration.urls', namespace='administration')),
    (r'^', include('testapp.frontend.urls', namespace='frontend')),

)
