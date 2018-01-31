from django.conf.urls import url
from django.contrib.auth import views as auth_views

from user.form import CustomAuthenticationForm
from user.views import signup, logout_view

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True,
                                                  authentication_form = CustomAuthenticationForm), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
]