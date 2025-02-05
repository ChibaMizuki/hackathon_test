from django.core.exceptions import ValidationError
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
        (1, '楽単優先'),
        (2, '挑戦優先'),
    ]
    
    # 要望レベルの選択肢
    PRIORITY_CHOICES = [
        (1, '最優先'),
        (2, '優先'),
        (3, '考慮せず'),
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
    easy_level_priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)  # 要望レベルを追加

    # 必修含むかどうかのフィールド
    required = models.BooleanField(default=True)

    # A群、B群、C群の下限値
    a_group_limit = models.PositiveSmallIntegerField(default=0, blank=True, null=True)  # A群必要単位数下限値
    b_group_limit = models.PositiveSmallIntegerField(default=0, blank=True, null=True)  # B群下限値
    c_group_limit = models.PositiveSmallIntegerField(default=0, blank=True, null=True)  # C群下限値

    # 授業内容区分
    attendance_priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    report_priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    test_priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3)

    # オンデマ優先か否か
    is_ondemand_priority = models.BooleanField(default=False)

    # 全休のフィールド
    full_day_off = models.IntegerField(choices=[(i, f'{i}日') for i in range(0, 6)], default=0)

    # 空コマの有無
    has_empty_slots = models.BooleanField(default=False)
    
    # 入れない時限
    excluded_periods = models.JSONField(default=list, blank=True)  # 空リストをデフォルトに設定


    def __str__(self):
        excluded_periods_display = ', '.join(f"{i}限" for i in self.excluded_periods) if self.excluded_periods else '除外なし'

        return (
            f"学期: {self.get_semester_display()}\n "
            f"学年: {self.get_grade_display()}\n "
            f"学部: {self.get_faculty_display()}\n "
            f"学科: {self.get_department_display()}\n "
            f"授業難易度: {self.get_easy_level_display()} ({self.get_easy_level_priority_display()})\n "
            f"{'必修含む' if self.required else '必修なし'}\n "
            f"A群: {self.a_group_limit}単位 B群: {self.b_group_limit}単位 C群: {self.c_group_limit}単位\n "
            f"出席: {self.get_attendance_priority_display()}\n "
            f"レポート: {self.get_report_priority_display()}\n "
            f"テスト: {self.get_test_priority_display()}\n "
            f"{'オンデマ優先' if self.is_ondemand_priority else 'オンデマ優先なし'}\n "
            f"全休: {self.full_day_off}日\n "
            f"{'空コマあり' if self.has_empty_slots else '空コマなし'}\n "
            f"除外時限: {excluded_periods_display}\n "
        )

