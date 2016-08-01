from bookshot import models

def profile(request):
	profile_picture_url = models.get_user_profile_picture_url(request.user)

	return {
		"profile_picture_url": profile_picture_url,
	}
