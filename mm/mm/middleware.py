from django.shortcuts import redirect
from social_core.exceptions import AuthCanceled
from social_django.middleware import SocialAuthExceptionMiddleware


class SocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if type(exception) == AuthCanceled:
            return redirect("/login/")
        else:
            raise exception