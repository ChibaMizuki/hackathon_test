from django.db import models

class ScheduleCriteria(models.Model):
    # 学部の選択肢
    DEPARTMENT_CHOICES = [
        ('engineering', '工学部'),
        ('science', '理学部'),
        ('literature', '文学部'),
    ]
    
    # 楽単度の選択肢
    EASY_LEVEL_CHOICES = [
        (1, '楽単'),
        (2, '落胆'),
        (3, '落単'),
    ]
    
    # 要望レベルの選択肢
    PRIORITY_CHOICES = [
        (1, '絶対'),
        (2, 'あればよし'),
        (3, 'なくてよい'),
    ]

    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    department_priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3)  # 要望レベルを追加

    easy_level = models.IntegerField(choices=EASY_LEVEL_CHOICES)
    easy_level_priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3)  # 要望レベルを追加

    required = models.BooleanField(default=True)  # 必修含むかどうか
    required_priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)  # 要望レベルを追加

    def __str__(self):
        return (
            f"{self.get_department_display()}({self.get_department_priority_display()}) - "
            f"{self.get_easy_level_display()}({self.get_easy_level_priority_display()}) - "
            f"{'必修含む' if self.required else '必修なし'}({self.get_required_priority_display()})"
        )
