from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Tree, Task, Photo, User, Species, Link, Faq
from .forms import TaskCreateForm, TaskUpdateForm, PhotoCreateForm, PhotoListallFormTree
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.paginator import Paginator
from PIL import Image
from datetime import timedelta, datetime, date


# Dashboard
@login_required
def tdb(request):
    trees = Tree.objects.filter(ownerfk=request.user).order_by('tname')
    treetasks = Task.objects.select_related('treefk__ownerfk').filter(treefk__ownerfk=request.user,
                                                                      real_date__isnull=False,).order_by('-real_date')
    nexttasks = Task.objects.select_related('treefk__ownerfk').filter(treefk__ownerfk=request.user,
                                                                      real_date__isnull=True,
                                                                      plan_date__isnull=False,
                                                                      plan_date__gt=timezone.now(),
                                                                      plan_date__lt=timezone.now() + timedelta(
                                                                          days=92)).order_by('plan_date')
    overduetasks = Task.objects.select_related('treefk__ownerfk').filter(treefk__ownerfk=request.user,
                                                                         real_date__isnull=True,
                                                                         plan_date__isnull=False,
                                                                         plan_date__lt=timezone.now()).order_by('plan_date')
    content = {
        'titre': _("Dashboard"),
    }
    context = {
        'content': content,
        'trees': trees,
        'tasks': treetasks,
        'nexttasks': nexttasks,
        'overduetasks': overduetasks,
    }
    return render(request, 'core/tdb.html', context)


# Manage the trees
class TreeListView(ListView):
    model = Tree
    # template_name = 'core/tree_list.html'
    context_object_name = 'trees'
    ordering = ['tname']


@login_required
def treedetail(request, pk):
    tree = Tree.objects.get(pk=pk)
    treetasks = Task.objects.filter(treefk=pk).order_by('real_date', 'plan_date')
    photos = Photo.objects.filter(treefk=pk).order_by('-shot_date')
    paginator = Paginator(photos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user != tree.ownerfk and not tree.ownerfk.profile.public_profile:
        mes = _("Trying to see private tree?")
        messages.warning(request, mes)
        return redirect('core-tdb')

    context = {'tree': tree, 'page_obj': page_obj, 'tasks': treetasks}
    return render(request, 'core/tree_detail.html', context)


class TreeCreateView(LoginRequiredMixin, CreateView):
    model = Tree
    fields = ['tname', 'originfk', 'description', 'speciesfk', 'bdate', 'adate', 'treePic', 'url']

    def form_valid(self, form):
        form.instance.ownerfk = self.request.user
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
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

    def get_form(self, *args, **kwargs):
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
@login_required
def taskdetail(request, pk):
    task = Task.objects.get(pk=pk)
    photos_before = Photo.objects.filter(taskfk=pk).filter(before_pic=True)
    photos_during = Photo.objects.filter(taskfk=pk).exclude(before_pic=True).exclude(after_pic=True)
    photos_after = Photo.objects.filter(taskfk=pk).filter(after_pic=True)
    if request.user != task.treefk.ownerfk and not task.treefk.ownerfk.profile.public_profile:
        mes = _("Trying to see private task?")
        messages.warning(request, mes)
        return redirect('core-tdb')

    context = {'task': task, 'photos_before': photos_before, 'photos_during': photos_during,
               'photos_after': photos_after}
    return render(request, 'core/task_detail.html', context)


@login_required
def taskcreate(request, treepk):
    # tree = Tree.objects.get(id=treepk)
    form = TaskCreateForm()
    form.fields['plan_date'].widget.input_type = 'date'
    form.fields['real_date'].widget.input_type = 'date'
    form.fields['treefk'].queryset = Tree.objects.filter(pk=treepk)

    if request.method == 'POST':

        print('request.post', request.POST.get('plan_date'))
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            if not request.POST.get('plan_date') and not request.POST.get('real_date'):
                mes = _("You need to specify a planned date or a realisation date please.")
                messages.warning(request, mes)
                context = {'form': form}
                return render(request, 'core/task_form.html', context)
            else:
                form.save()
                return redirect('tree-detail', pk=treepk)
    else:
        context = {'form': form}
        return render(request, 'core/task_form.html', context)


@login_required
def taskupdate(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskUpdateForm(instance=task)
    form.fields['plan_date'].widget.input_type = 'date'
    form.fields['real_date'].widget.input_type = 'date'
    form.fields['treefk'].queryset = Tree.objects.filter(ownerfk=request.user)

    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            if not request.POST.get('plan_date') and not request.POST.get('real_date'):
                mes = _("You need to specify a planned date or a realisation date please.")
                messages.warning(request, mes)
                context = {'form': form}
                return render(request, 'core/task_form.html', context)
            else:
                form.save()
                return redirect('task-detail', pk=pk)
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
def photolist(request, owner):
    ownerobj = get_object_or_404(User, pk=owner)
    if ownerobj == request.user or ownerobj.profile.public_profile is True:
        photos = Photo.objects.filter(treefk__ownerfk=ownerobj).order_by('-shot_date')
        paginator = Paginator(photos, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'owner': ownerobj, 'page_obj': page_obj}
        print(context)
        return render(request, 'core/photo_list.html', context)
    else:
        mes = _("Are you trying to list private pictures?")
        messages.warning(request, mes)
        return redirect('core-tdb')


@login_required
def photolistall(request, owner, species):
    # Methode POST
    if request.method == 'POST':
        owner = request.POST.get('ownerfk')
        if owner != "":
            owner = int(owner)
        else:
            owner = 0

        species = request.POST.get('speciesfk')
        if species != "":
            species = int(species)
        else:
            species = 0
        return redirect('photo-listall', owner, species)

    # Methode GET
    if owner != 0:
        ownerobj = get_object_or_404(User, pk=owner)
        if ownerobj != request.user and ownerobj.profile.public_profile is False:
            mes = _("Are you trying to list private pictures?")
            messages.warning(request, mes)
            return redirect('core-tdb')
    if species != 0:
        speciesobj = get_object_or_404(Species, pk=species)

    if owner != 0 and species != 0:
        photos = Photo.objects.filter(treefk__ownerfk=ownerobj, treefk__speciesfk=speciesobj).order_by('-shot_date')[:100]
    elif owner != 0:
        photos = Photo.objects.filter(treefk__ownerfk=ownerobj).order_by('-shot_date')[:100]
    elif species != 0:
        photos = Photo.objects.filter(treefk__ownerfk__profile__public_profile=True).filter(treefk__speciesfk=speciesobj).order_by('-shot_date')[:100]
    else:
        photos = Photo.objects.filter(treefk__ownerfk__profile__public_profile=True).order_by('-shot_date')[:100]

    paginator = Paginator(photos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = PhotoListallFormTree(initial={'ownerfk': owner, 'speciesfk': species})
    context = {'form': form, 'owner': owner, 'species': species, 'page_obj': page_obj}
    # print(context)
    return render(request, 'core/photo_listall.html', context)


class PhotoDetailView(UserPassesTestMixin, DetailView):
    model = Photo

    def test_func(self):
        photo = self.get_object()
        if self.request.user == photo.treefk.ownerfk or photo.treefk.ownerfk.profile.public_profile:
            return True
        return False


@login_required
def photocreate(request, tree, task):
    if tree == 0:
        mes = _('Trying to add an image to unidentified tree?')
        messages.warning(request, mes)
        return redirect('core-tdb')
    else:
        mytree = Tree.objects.get(id=tree)
        if mytree.ownerfk != request.user:
            mes = _("Trying to add an image to someone else's tree?")
            messages.warning(request, mes)
            return redirect('core-tdb')

    form = PhotoCreateForm()

    if request.method == 'POST':
        form = PhotoCreateForm(request.POST, request.FILES)

        if form.is_valid():
            img = Image.open(request.FILES['picture'])
            if img.format != 'JPEG':
                mes = _('Only JPG images are allowed, sorry!')
                messages.warning(request, mes)
                return redirect('photo-create', tree=tree, task=task)
            else:
                form.save()
                if task != 0:
                    return redirect('task-detail', pk=task)
                elif tree != 0:
                    return redirect('tree-detail', pk=tree)
                else:
                    return redirect('photo-create', tree=tree, task=task)

        else:
            mes = _("Your form is not valid and I don't know why!")
            messages.warning(request, mes)
            return redirect('core-tdb')
    else:
        form.fields['treefk'].queryset = Tree.objects.filter(pk=tree)
        if task == 0:
            form.fields['taskfk'].queryset = Task.objects.filter(treefk=tree)
        else:
            form.fields['taskfk'].queryset = Task.objects.filter(pk=task)
            form.initial['taskfk'] = task
        context = {'form': form}
        return render(request, 'core/photo_form.html', context)


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo
    success_url = '/core/'

    def test_func(self):
        photo = self.get_object()
        if self.request.user == photo.treefk.ownerfk:
            return True
        return False


@login_required
def tasks(request, action):
    # Next tasks
    if action == 1:
        nexttasks = Task.objects.select_related('treefk__ownerfk').filter(treefk__ownerfk=request.user,
                                                                          real_date__isnull=True,
                                                                          plan_date__isnull=False,
                                                                          plan_date__gt=timezone.now()).order_by('plan_date')
        context = {'title': _('Next tasks'), 'tasks': nexttasks, 'action': 1}
        return render(request, 'core/tasks.html', context)
    # Overdue tasks
    elif action == 2:
        overduetasks = Task.objects.select_related('treefk__ownerfk').filter(treefk__ownerfk=request.user,
                                                                             real_date__isnull=True,
                                                                             plan_date__isnull=False,
                                                                             plan_date__lt=timezone.now()).order_by('plan_date')
        context = {'title': _('Overdue tasks'), 'tasks': overduetasks, 'action': 2}
        return render(request, 'core/tasks.html', context)
    # All tasks
    elif action == 3:
        treetasks = Task.objects.select_related('treefk__ownerfk').filter(treefk__ownerfk=request.user).order_by(
            '-real_date')
        context = {'title': _('All tasks'), 'tasks': treetasks, 'action': 3}
        return render(request, 'core/tasks.html', context)

    # url hack
    else:
        mes = _('Unknown action... WTF are you doing?')
        messages.warning(request, mes)
        return redirect('core-tdb')

# calendar
@login_required
def calendar(request):
    treetasks = Task.objects.select_related('treefk__ownerfk').filter(treefk__ownerfk=request.user).order_by(
        'real_date', 'plan_date')
    list_tasks = []
    for t in treetasks:
        # print(t.id)
        # print(t.tasklistfk.name)
        # print(t.plan_date.day)
        # print(t.plan_date.month)
        # print(t.plan_date.year)
        # print(t.real_date)
        task = {'id': str(t.id), 'name': t.tasklistfk.name, 'tree': t.treefk.tname}
        if t.real_date:
            task['day'] = t.real_date.day
            task['month'] = t.real_date.month
            task['year'] = t.real_date.year
            task['statut'] = 'done'
        else:
            task['day'] = t.plan_date.day
            task['month'] = t.plan_date.month
            task['year'] = t.plan_date.year
            if t.plan_date < date.today():
                task['statut'] = 'late'
            else:
                task['statut'] = 'planned'

        list_tasks.append(task)

    context = {'tasks': list_tasks}
    return render(request, 'core/calendar.html', context)

@login_required
def membersmap(request):
    members = User.objects.filter(profile__public_profile=True)
    context = {'title': _('Members map'), 'members': members}
    return render(request, 'core/membersmap.html', context)


class LinksView(LoginRequiredMixin, ListView):
    model = Link
    # template_name = 'core/link_list.html'
    context_object_name = 'links'
    ordering = ['linkcatfk', 'order']


class FaqView(LoginRequiredMixin, ListView):
    model = Faq
    # template_name = 'core/link_list.html'
    context_object_name = 'faqs'
    ordering = ['faqcatfk', 'order']

