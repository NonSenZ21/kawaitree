from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Species, Tree
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.translation import gettext as _


@login_required
def tdb(request):

    #trees = Tree.objects.all()
    trees = Tree.objects.filter(ownerfk=request.user).order_by('tname')
    content = {
        'titre': _("Dashboard"),
    }
    context = {
        'content': content,
        'trees': trees}
    return render(request, 'core/tdb.html',context)

class TreeListView(ListView):
    model = Tree
    #template_name = 'core/tree_list.html'
    context_object_name = 'trees'
    ordering = ['tname']

class TreeListView(ListView):
    model = Tree
    #template_name = 'core/tree_list.html'
    context_object_name = 'trees'
    ordering = ['tname']

class TreeDetailView(DetailView):
    model = Tree

class TreeCreateView(LoginRequiredMixin, CreateView):
    model = Tree
    fields = ['tname', 'shop', 'description', 'speciesfk', 'bdate', 'adate']

    def form_valid(self, form):
        form.instance.ownerfk = self.request.user
        return super().form_valid(form)

class TreeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tree
    fields = ['tname', 'shop', 'description', 'speciesfk', 'bdate', 'adate']

    def form_valid(self, form):
        form.instance.ownerfk = self.request.user
        return super().form_valid(form)

    def test_func(self):
        tree = self.get_object()
        if self.request.user == tree.ownerfk:
            return True
        return False

class TreeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tree
    success_url = '/core/'

    def test_func(self):
        tree = self.get_object()
        if self.request.user == tree.ownerfk:
            return True
        return False

@login_required
def about(request):
    content = {
        'titre': _("About"),
    }
    context = {'content': content}
    return render(request, 'core/about.html',context)