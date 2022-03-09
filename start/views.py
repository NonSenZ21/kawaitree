from django.shortcuts import render, redirect
from django.utils.translation import gettext as _



def home(request):
   if request.user.is_authenticated:
      return redirect('/core/')
   else:
      content = {
         'titre': _("Bonsaï management"),
         'head1': _("what?")
      }

      context = {'content': content}
      return render(request,'start/home.html',context)

