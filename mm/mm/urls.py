from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('user.urls')),
    url(r'^', include('cal.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('zinnia.urls')),
]

