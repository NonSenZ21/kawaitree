from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.http import HttpResponse


def home(request):
    if request.user.is_authenticated:
        return redirect('/core/')
    else:
        content = {
            'titre': _("Bonsaï management"),
            'head1': _("what?")
        }

        context = {'content': content}
        return render(request, 'start/home.html', context)


def service_worker(request):
    sw_path = settings.BASE_DIR / "static/js" / "sw.js"
    response = HttpResponse(open(sw_path).read(), content_type='application/javascript')
    return response
