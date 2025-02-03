from django.urls import path
from .views import HomeView, InputFormView, GeneratingView, ResultView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('input/', InputFormView.as_view(), name='input_form'),
    path('generating/', GeneratingView.as_view(), name='generating'),
    path('result/', ResultView.as_view(), name='result'),
]
