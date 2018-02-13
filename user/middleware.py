from django.shortcuts import redirect
from social_core.exceptions import AuthCanceled
from social_django.middleware import SocialAuthExceptionMiddleware
from social_django.models import UserSocialAuth

class SocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if type(exception) == AuthCanceled:
            return redirect("/login/")
        else:
            raise exception

    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                users = UserSocialAuth.objects.get(user=request.user)
                request.fbid = users.uid
            except Exception as e:
            	pass