def profile(request):
	if request.user.is_authenticated():
		profile_picture_url = "https://graph.facebook.com/{0}/picture".format(request.user.social_auth.get().uid)
	else:
		profile_picture_url = ""

	return {
		"profile_picture_url": profile_picture_url,
	}
