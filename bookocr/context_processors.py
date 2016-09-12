from django.conf import settings
from bookshot import models

def profile(request):
	profile_picture_url = models.get_user_profile_picture_url(request.user)

	return {
		"profile_picture_url": profile_picture_url,
	}

def load_additional_settings(request):
	print('loading additional settings..', settings.GOOGLE_ANALYTICS_TRACKER_ID)
	return {
		"GOOGLE_ANALYTICS_TRACKER_ID": settings.GOOGLE_ANALYTICS_TRACKER_ID,
	}

