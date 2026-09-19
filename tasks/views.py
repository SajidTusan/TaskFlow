from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .forms import RegisterForm, TaskForm
from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    """Dashboard: only shows the logged-in user's own tasks."""

    model = Task
    template_name = "tasks/home.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user).select_related("category")

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(title__icontains=search)

        status = self.request.GET.get("status")
        if status == "completed":
            queryset = queryset.filter(completed=True)
        elif status == "pending":
            queryset = queryset.filter(completed=False)

        priority = self.request.GET.get("priority")
        if priority:
            queryset = queryset.filter(priority=priority)

        return queryset.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Stats must describe ALL of the user's tasks, not just the filtered list.
        all_tasks = Task.objects.filter(user=self.request.user)
        context["total_tasks"] = all_tasks.count()
        context["completed_tasks"] = all_tasks.filter(completed=True).count()
        context["pending_tasks"] = all_tasks.filter(completed=False).count()
        context["high_priority"] = all_tasks.filter(priority="high").count()
        return context


@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task created successfully!")
            return redirect("home")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form})


# Changing data with a plain GET link is unsafe (CSRF / link prefetching),
# so delete and toggle only accept POST requests.
@login_required
@require_POST
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()
    messages.success(request, "Task deleted successfully!")
    return redirect("home")


@login_required
@require_POST
def toggle_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.completed = not task.completed
    task.save(update_fields=["completed", "updated_at"])
    return redirect("home")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Account created! Please log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})
