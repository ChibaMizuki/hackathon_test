from django import forms
from .models import ScheduleCriteria

class ScheduleCriteriaForm(forms.ModelForm):
    class Meta:
        model = ScheduleCriteria
        fields = ['department', 'easy_level', 'required']
