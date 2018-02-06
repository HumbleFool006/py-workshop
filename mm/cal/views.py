from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    c = {}
    return TemplateResponse(request=request, template="fullcalendar.html", context=c)