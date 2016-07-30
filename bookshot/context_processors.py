from bookshot import models 

def profile(request):
	profile_picturel_url = models.get_user_profile_picture_url(request.uesr)

	return {
		"profile_picture_url": profile_picture_url,
	}

