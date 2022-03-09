from django.shortcuts import render
from .models import Species, Tree
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

@login_required
def tdb(request):

    #trees = Tree.objects.all()
    trees = Tree.objects.filter(ownerfk=request.user)
    content = {
        'titre': _("Dashboard"),
    }
    context = {
        'content': content,
        'trees': trees}
    return render(request, 'core/tdb.html',context)

@login_required
def about(request):
    content = {
        'titre': _("About"),
    }
    context = {'content': content}
    return render(request, 'core/about.html',context)