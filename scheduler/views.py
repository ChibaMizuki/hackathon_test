from django.views.generic import TemplateView, FormView, RedirectView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import ScheduleCriteriaForm
from .models import ScheduleCriteria
import time
from scheduler.make_timetable.main import make_timetable

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
        # 生成処理
        condition = ScheduleCriteria.objects.last()
        timetable = make_timetable(conditions=condition)
        return super().get(request, *args, **kwargs)

class ResultView(TemplateView):
    template_name = "scheduler/result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last = ScheduleCriteria.objects.last()
        context['criteria'] = last
        return context
