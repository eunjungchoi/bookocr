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

    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.log_in, name='log_in'),
    url(r'^logout/$', views.log_out, name='log_out'),
    url(r'^(?P<quote_id>[0-9]+)$', views.detail, name='detail'),
    url(r'^form/$', views.form, name='form'),
    url(r'^add/$', views.add, name='add'),

    url(r'^bookform/$', views.bookform, name='bookform'),
    url(r'^addbook/$', views.add_book, name='add_book'),
    #
    url(r'^test/$', views.test_index, name='index'),
    url(r'^test/me$', views.test_me, name='me'),
    url(r'^test/quotes/new$', views.test_new_quote, name='new_quote'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#
# 마지막 static 라인은, debug= True일 때만 동작. 