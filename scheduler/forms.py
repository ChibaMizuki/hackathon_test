from django import forms
from .models import ScheduleCriteria

class ScheduleCriteriaForm(forms.ModelForm):
    # 除外する時限を複数選択できるように、1~5限のボタンを作成
    EXCLUDED_PERIOD_CHOICES = [
        (1, '1限'),
        (2, '2限'),
        (3, '3限'),
        (4, '4限'),
        (5, '5限'),
    ]
    excluded_periods = forms.MultipleChoiceField(
        choices=EXCLUDED_PERIOD_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,  # 空でも問題ない
        initial=[],  # 空のリストを初期値として設定
    )

    class Meta:
        model = ScheduleCriteria
        fields = [
            'semester', 'grade',
            'faculty', 'department',
            'easy_level', 'easy_level_priority',
            'required', 'required_priority',
            'a_group_limit', 'b_group_limit', 'c_group_limit',
            'content_type', 'is_ondemand_priority',
            'full_day_off', 'has_empty_slots',
            'excluded_periods'
        ]
