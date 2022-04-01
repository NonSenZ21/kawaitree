# from .forms import TreeUpdateForm
# from django.contrib import messages
from django.shortcuts import render, redirect
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
    trees = Tree.objects.filter(ownerfk=request.user).order_by('tname')
    content = {
        'titre': _("Dashboard"),
    }
    context = {
        'content': content,
        'trees': trees}
    return render(request, 'core/tdb.html',context)

# @login_required
# def UpdateTree(request,pk):
#     tree = Tree.objects.filter(id=pk).first()
#
#     if request.method == 'POST':
#         tree_form = TreeUpdateForm(request.POST, request.FILES)
#         if tree_form.is_valid():
#             tree_form.instance.ownerfk = tree.ownerfk
#             tree_form.instance.id = pk
#             if tree_form.instance.treePic == "default.png" and tree.treePic != "default.png":
#                 tree_form.instance.treePic = tree.treePic
#             tree_form.save()
#             messages.success(request, f'Your tree has been updated!')
#             messages.info(request, f'tree_form.instance.treePic : {tree_form.instance.treePic}')
#             messages.info(request, f'tree.treePic : {tree.treePic}')
#         else:
#             messages.warning(request, f'Something went wrong!')
#             return redirect('core-tdb')
#     else:
#         tree_form = TreeUpdateForm(instance=tree)
#
#     context = {
#         'tree_form': tree_form,
#     }
#     return render(request,'core/tree_form.html',context)

class TreeListView(ListView):
    model = Tree
    #template_name = 'core/tree_list.html'
    context_object_name = 'trees'
    ordering = ['tname']

class TreeDetailView(DetailView):
    model = Tree

class TreeCreateView(LoginRequiredMixin, CreateView):
    model = Tree
    fields = ['tname', 'shop', 'description', 'speciesfk', 'bdate', 'adate', 'treePic']

    def form_valid(self, form):
        form.instance.ownerfk = self.request.user
        return super().form_valid(form)

    def get_form(self):
        form = super().get_form()
        form.fields['bdate'].widget.input_type = 'date'
        form.fields['adate'].widget.input_type = 'date'
        return form

class TreeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tree
    fields = ['tname', 'shop', 'description', 'speciesfk', 'bdate', 'adate', 'treePic']

    def form_valid(self, form):
        form.instance.ownerfk = self.request.user
        return super().form_valid(form)

    def test_func(self):
        tree = self.get_object()
        if self.request.user == tree.ownerfk:
            return True
        return False

    def get_form(self):
        form = super().get_form()
        form.fields['bdate'].widget.input_type = 'date'
        form.fields['adate'].widget.input_type = 'date'
        return form

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