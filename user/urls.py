from django.conf.urls import re_path
from django.contrib.auth import views as auth_views

from user.form import CustomAuthenticationForm
from user.views import signup, logout_view

urlpatterns = [
    re_path('^signup/$', signup, name='signup'),
    re_path('^login/$', auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True,
                                                  authentication_form = CustomAuthenticationForm), name='login'),
    re_path('^logout/$', logout_view, name='logout'),
]
