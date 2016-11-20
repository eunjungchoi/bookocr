from bookshot import models
from bookshot.models import UserProxy


def auth(request):
    """
    Returns context variables required by apps that use Django's authentication
    system.

    If there is no 'user' attribute in the request, uses AnonymousUser (from
    django.contrib.auth).
    """
    if hasattr(request, 'user'):
        try:
            user = UserProxy.objects.get(pk=request.user.id)
        except UserProxy.DoesNotExist:
            from django.contrib.auth.models import AnonymousUser
            user = AnonymousUser()
    return {
        'user': user,
    }


def profile(request):
	profile_picture_url = None
	if not request.user.is_anonymous():
		profile_picture_url = models.get_user_profile_picture_url(request.user)

	return {
		"profile_picture_url": profile_picture_url,
	}
