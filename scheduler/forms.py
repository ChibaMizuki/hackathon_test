from django import forms
from .models import ScheduleCriteria

class ScheduleCriteriaForm(forms.ModelForm):
    class Meta:
        model = ScheduleCriteria
        fields = [
            'department', 'department_priority', 
            'easy_level', 'easy_level_priority', 
            'required', 'required_priority'
        ]
