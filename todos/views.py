from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TaskForm
from .models import Task


def home(request):
    """Requirement 1: insert data. Shows the form and the full task list."""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TaskForm()
    return render(request, "todos/home.html", {"form": form, "tasks": Task.objects.all()})


def search(request):
    """Requirement 2: search data by keyword in title or notes."""
    query = request.GET.get("q", "").strip()
    results = []
    if query:
        results = Task.objects.filter(Q(title__icontains=query) | Q(notes__icontains=query))
    return render(request, "todos/search.html", {"query": query, "results": results})


@require_POST
def toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.done = not task.done
    task.save()
    return redirect(request.POST.get("next") or "home")


@require_POST
def delete(request, pk):
    get_object_or_404(Task, pk=pk).delete()
    return redirect("home")
