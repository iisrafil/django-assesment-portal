from django.contrib import messages
from django.shortcuts import render, redirect

from todo.forms import TodoForm
from todo.models import Task


def task_list(request):
    pending = Task.objects.filter(user=request.user, completed=False)
    done = Task.objects.filter(user=request.user, completed=True)

    context = {
        'pendings': pending,
        'dones': done
    }
    return render(request, 'todo/list.html', context)


def create_task(request):
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f'Your task has been added successfully !')
            return redirect("todo")
    else:
        form = TodoForm()

    context = {
        'form': form
    }
    return render(request, 'todo/forms.html', context)


def mark(request, pk):
    task = Task.objects.get(pk=pk)
    task.completed = True
    task.save()

    return redirect("todo")
