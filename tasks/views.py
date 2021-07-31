from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from .models import Task
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


class TasksListView(LoginRequiredMixin,ListView):
    template_name = "tasks/tasks.html"
    extra_context = {
        "today": timezone.now().strftime('%B %d, %Y'),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_date = self.request.GET.get("date") or timezone.now().strftime('%B %d, %Y')
        context['filter_date'] = filter_date
        context['filter_date_next'] = (datetime.strptime(filter_date,'%B %d, %Y') + timedelta(days=1)).strftime('%B %d, %Y')
        context['filter_date_previous'] = (datetime.strptime(filter_date,'%B %d, %Y') + timedelta(days=-1)).strftime('%B %d, %Y')
        context['total_tasks'] = self.request.user.task_set.all().count()
        context['completed_tasks'] = self.request.user.task_set.filter(completed=True).count()
        return context


    def get_queryset(self):
        if self.request.GET.get("search"):
            queryset = self.request.user.task_set.filter(title__contains=self.request.GET.get("search"))
        else:
            date = self.request.GET.get("date") or timezone.now().strftime('%B %d, %Y')
            date = datetime.strptime(date,'%B %d, %Y')
            queryset = self.request.user.task_set.filter(date=date)
        return queryset



@login_required
def toggle_check(request,id):
    if request.method == "GET":
        obj = Task.objects.get(id=id)
        obj.completed = not obj.completed
        obj.save()
        return redirect('tasks')


class TaskUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Task
    fields = ['title']
    template_name = "tasks/task-update.html"
    success_url = reverse_lazy("tasks")

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.user:
            return True
        return False

class TaskDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Task
    success_url = reverse_lazy("tasks")
    template_name = "tasks/task-delete.html"

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.user:
            return True
        return False

class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    fields = ["title"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        date = self.request.GET.get("date") or timezone.now().strftime('%B %d, %Y')
        obj.date = datetime.strptime(date,'%B %d, %Y')
        return super(TaskCreateView, self).form_valid(form)

    def get_success_url(self,**kwargs):
        date = self.request.GET.get("date") or timezone.now().strftime('%B %d, %Y')
        return reverse("tasks") + f"?date={date}"
