from django.db import models

class ScheduleCriteria(models.Model):
    # 学部の選択肢
    FACULTY_CHOICES = [
        ('fundamental', '基幹'),
        ('advanced', '先進'),
        ('creative', '創造'),
    ]
    
    # 学科
    DEPARTMENT_CHOICES = [
        ('mathematics', '数学'),
        ('intermedia', '表現'),
        ('chemistry', '化学'),
    ]
    
    # 学期
    SEMESTER_CHOICES = [
        ('spring', '春'),
        ('autumn', '秋'),
    ]
    
    # 学年
    GRADE_CHOICES = [
        (1, '1年'),
        (2, '2年'),
        (3, '3年'),
        (4, '4年'),
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
        (2, '高'),
        (3, '中'),
        (4, '低'),
    ]
    
    # 授業内容区分の選択肢
    CONTENT_TYPE_CHOICES = [
        ('report', 'レポート'),
        ('attendance', '出席'),
        ('test', 'テスト'),
    ]

    # 学期のフィールド
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='spring')
    
    # 学年のフィールド
    grade = models.IntegerField(choices=GRADE_CHOICES, default=1)

    # 学部のフィールド
    faculty = models.CharField(max_length=50, choices=FACULTY_CHOICES, default='fundamental')
    
    # 学科のフィールド
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='mathematics')

    # 楽単度のフィールド
    easy_level = models.IntegerField(choices=EASY_LEVEL_CHOICES, default=1)
    easy_level_priority = models.IntegerField(choices=PRIORITY_CHOICES, default=4)  # 要望レベルを追加

    # 必修含むかどうかのフィールド
    required = models.BooleanField(default=True)  # 必修含むかどうか
    required_priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)  # 要望レベルを追加

    # A群、B群、C群の下限値
    a_group_limit = models.IntegerField(default=0, blank=True, null=True)  # A群必要単位数下限値
    b_group_limit = models.IntegerField(default=0, blank=True, null=True)  # B群下限値
    c_group_limit = models.IntegerField(default=0, blank=True, null=True)  # C群下限値

    # 授業内容区分
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='attendance')

    # オンデマ優先か否か
    is_ondemand_priority = models.BooleanField(default=False)

    # 全休のフィールド
    full_day_off = models.IntegerField(choices=[(i, f'{i}日') for i in range(1, 6)], default=1)

    # 空コマの有無
    has_empty_slots = models.BooleanField(default=False)
    
    # 入れない時限
    excluded_periods = models.JSONField(default=list, blank=True)  # 空リストをデフォルトに設定


    def __str__(self):
        excluded_periods_display = ', '.join(f"{i}限" for i in self.excluded_periods) if self.excluded_periods else '除外なし'

        return (
            f"{self.get_semester_display()}\n "
            f"{self.get_grade_display()}\n "
            f"{self.get_faculty_display()}\n "
            f"{self.get_department_display()}\n "
            f"{self.get_easy_level_display()}({self.get_easy_level_priority_display()})\n "
            f"{'必修含む' if self.required else '必修なし'}({self.get_required_priority_display()})\n "
            f"A群: {self.a_group_limit}単位 B群: {self.b_group_limit}単位 C群: {self.c_group_limit}単位\n "
            f"授業内容: {self.get_content_type_display()}\n "
            f"{'オンデマ優先' if self.is_ondemand_priority else 'オンデマ優先なし'}\n "
            f"全休: {self.full_day_off}日\n "
            f"{'空コマあり' if self.has_empty_slots else '空コマなし'}\n "
            f"除外時限: {excluded_periods_display}\n "
        )

