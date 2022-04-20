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
from .models import Tree, Task
from .forms import TaskCreateForm, TaskUpdateForm, PhotoCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.translation import gettext as _
from django.utils import timezone
from datetime import timedelta


# Dashboard
@login_required
def tdb(request):
    trees = Tree.objects.filter(ownerfk=request.user).order_by('tname')
    tasks = Task.objects.select_related('treefk__ownerfk').filter(treefk__ownerfk=request.user).order_by('-real_date')
    nexttasks = Task.objects.select_related('treefk__ownerfk').filter(treefk__ownerfk=request.user,
                                                                      plan_date__isnull=False,
                                                                      plan_date__gt=timezone.now(),
                                                                      plan_date__lt=timezone.now() + timedelta(
                                                                          days=92)).order_by('plan_date')
    content = {
        'titre': _("Dashboard"),
    }
    context = {
        'content': content,
        'trees': trees,
        'tasks': tasks,
        'nexttasks': nexttasks,
    }
    return render(request, 'core/tdb.html', context)


# Manage the trees
class TreeListView(ListView):
    model = Tree
    # template_name = 'core/tree_list.html'
    context_object_name = 'trees'
    ordering = ['tname']


class TreeDetailView(UserPassesTestMixin, DetailView):
    model = Tree

    def test_func(self):
        tree = self.get_object()
        if self.request.user == tree.ownerfk or tree.ownerfk.profile.public_profile:
            return True
        return False


class TreeCreateView(LoginRequiredMixin, CreateView):
    model = Tree
    fields = ['tname', 'originfk', 'description', 'speciesfk', 'bdate', 'adate', 'treePic', 'url']

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
    fields = ['tname', 'originfk', 'description', 'speciesfk', 'bdate', 'adate', 'treePic', 'url']

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


# Manage the tasks
class TaskDetailView(UserPassesTestMixin, DetailView):
    model = Task

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.treefk.ownerfk or task.treefk.ownerfk.profile.public_profile:
            return True
        return False


@login_required
def TaskCreate(request, treepk):
    # tree = Tree.objects.get(id=treepk)
    form = TaskCreateForm()
    form.fields['plan_date'].widget.input_type = 'date'
    form.fields['real_date'].widget.input_type = 'date'
    form.fields['treefk'].queryset = Tree.objects.filter(pk=treepk)

    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core-tdb')
    else:
        context = {'form': form}
        return render(request, 'core/task_form.html', context)

@login_required
def TaskUpdate(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskUpdateForm(instance=task)
    form.fields['plan_date'].widget.input_type = 'date'
    form.fields['real_date'].widget.input_type = 'date'
    form.fields['treefk'].queryset = Tree.objects.filter(ownerfk=request.user)

    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('core-tdb')
    else:
        context = {'form': form}
        return render(request, 'core/task_form.html', context)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = '/core/'

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.treefk.ownerfk:
            return True
        return False

@login_required
def PhotoCreate(request):
    form = PhotoCreateForm()
    # form.fields['shot_date'].widget.input_type = 'date'
    # form.fields['treefk'].queryset = Tree.objects.filter(pk=treepk)

    if request.method == 'POST':
        form = PhotoCreateForm(request.POST,request.FILES)

        if form.is_valid():
            # form.fields['thumb'] = form.fields['picture']
            form.save()
            return redirect('core-tdb')
        else:
            print("error !!!!")
            print(form.errors)
            print(form.non_field_errors)
            print(request.POST)
            return redirect('photo-create')
    else:
        context = {'form': form}
        return render(request, 'core/photo_form.html', context)



@login_required
def about(request):
    content = {
        'titre': _("About"),
    }
    context = {'content': content}
    return render(request, 'core/about.html', context)
