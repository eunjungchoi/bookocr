"""bookocr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from bookshot import views

urlpatterns = [
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    # url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True, }),    
    url(r'^admin/', admin.site.urls),

    url(r'^login/$',  views.auth.log_in, name='log_in'),
    url(r'^logout/$', views.auth.log_out, name='log_out'),

    #
    #url(r'^$', views.index, name='_index'),
    url(r'^$', views.index, name='index'),

    url(r'^quotes/new$', views.quote.new, name='new_quote'),
    url(r'^add/$', views.quote.add, name='add'),
    #url(r'^(?P<quote_id>[0-9]+)$', views.detail, name='detail'),

    url(r'^bookform/$', views.book.form, name='bookform'),
    url(r'^addbook/$', views.book.add, name='add_book'),

    url(r'^me$', views.user.me, name='me'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#
# 마지막 static 라인은, debug= True일 때만 동작. 
