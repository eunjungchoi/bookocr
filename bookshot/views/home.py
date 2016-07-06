from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from bookshot.models import *


#@login_required
#def _index(request):
#	quote_list = Quote.objects.filter(user=request.user).order_by('-id')
#	user = request.user
#	social = user.social_auth.get()
#	#profile_picture_url = 'https://graph.facebook.com/{0}/picture?type=small'.format(social.uid)
#	profile_picture_url = 'https://graph.facebook.com/{0}/picture'.format(social.uid)
#
#	context = {
#		'quote_list' : quote_list,
#		'user' : user,
#		'profile_picture_url' : profile_picture_url
#	}
#	return render(request, 'index.html', context)

@login_required
def index(request):
	quote_list = Quote.objects.order_by('-id')

	context = {
		'quote_list' : quote_list,
	}
	return render(request, 'index.html', context)
	

@login_required
def detail(request):
	pass

