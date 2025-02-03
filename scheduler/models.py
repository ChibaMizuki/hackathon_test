from django.db import models

class ScheduleCriteria(models.Model):
    DEPARTMENT_CHOICES = [
        ('engineering', '工学部'),
        ('science', '理学部'),
        ('literature', '文学部'),
    ]
    
    EASY_LEVEL_CHOICES = [
        (1, '楽単'),
        (2, '落胆'),
        (3, '落単'),
    ]
    
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    easy_level = models.IntegerField(choices=EASY_LEVEL_CHOICES)
    required = models.BooleanField(default=True)  # 必修含むかどうか

    def __str__(self):
        return f"{self.get_department_display()} - {self.get_easy_level_display()} - {'必修含む' if self.required else '必修なし'}"
