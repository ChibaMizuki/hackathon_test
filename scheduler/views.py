from django.views.generic import TemplateView, FormView, RedirectView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import ScheduleCriteriaForm
from .models import ScheduleCriteria
import time

class HomeView(TemplateView):
    template_name = "scheduler/home.html"

class InputFormView(FormView):
    template_name = "scheduler/input_form.html"
    form_class = ScheduleCriteriaForm
    success_url = reverse_lazy('generating')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class GeneratingView(RedirectView):
    pattern_name = 'result'

    def get(self, request, *args, **kwargs):
        # 生成処理（仮で1秒待つ処理を入れる）
        time.sleep(1)
        last = ScheduleCriteria.objects.last()
        department = last.department
        print(department)
        return super().get(request, *args, **kwargs)

class ResultView(TemplateView):
    template_name = "scheduler/result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['criteria'] = ScheduleCriteria.objects.last()
        return context
