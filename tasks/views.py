from django.contrib.auth.decorators import login_required
from django.db.models import Case, IntegerField, Value, When
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import TaskForm
from .models import Task

def index(request):
    return render(request, 'tasks/index.html')

@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user).annotate(
        priority_order=Case(
            When(priority=Task.HIGH, then=Value(0)),
            When(priority=Task.NORMAL, then=Value(1)),
            default=Value(2), output_field=IntegerField(),
        ),
        no_due_date=Case(When(due_date__isnull=True, then=Value(1)),
                         default=Value(0), output_field=IntegerField()),
    ).order_by('completed', 'priority_order', 'no_due_date', 'due_date', 'id')
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'now': timezone.now()})

@login_required
def task_new(request):
    form = TaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.owner = request.user
        task.save()
        return redirect('tasks:task_list')
    return render(request, 'tasks/task_form.html', {'form': form, 'heading': 'Новая задача'})

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id, owner=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('tasks:task_list')
    return render(request, 'tasks/task_form.html', {'form': form, 'heading': 'Редактирование задачи'})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, owner=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks:task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_toggle(request, task_id):
    task = get_object_or_404(Task, pk=task_id, owner=request.user)
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    task.completed = not task.completed
    task.save(update_fields=['completed'])
    return redirect('tasks:task_list')
