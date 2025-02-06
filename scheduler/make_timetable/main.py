import pandas as pd
from scheduler.make_timetable.select_sub import select_sub
from scheduler.make_timetable.score import score
import ast


def make_timetable(conditions):
    df_cand_subject = pd.read_csv("data/subject3.csv")
    df_timetable = pd.DataFrame()
    df_cand_subject.set_index("科目キー", inplace=True)
    df_cand_subject["時限"] = df_cand_subject["時限"].apply(ast.literal_eval)
    df_cand_subject["学科"] = df_cand_subject["学科"].apply(ast.literal_eval)
    df_cand_subject, list_error = score(df_cand_subject, conditions)
    if not list_error[0]:
        return df_timetable, list_error
    df_timetable, list_error = select_sub(df_cand_subject, conditions)

    return df_timetable, list_error


class req:
    def __init__(self, faculty, department, grade, semester, required,
                 easy_level, easy_level_priority, is_ondemand_priority,
                 report_priority, attendance_priority, test_priority,
                 a_group_limit, b_group_limit, c_group_limit,
                 full_day_off, has_empty_slots, excluded_periods):
        self.faculty = faculty
        self.department = department
        self.grade = grade
        self.semester = semester
        self.required = required
        self.easy_level = easy_level
        self.easy_level_priority = easy_level_priority
        self.is_ondemand_priority = is_ondemand_priority
        self.report_priority = report_priority
        self.attendance_priority = attendance_priority
        self.test_priority = test_priority
        self.a_group_limit = a_group_limit
        self.b_group_limit = b_group_limit
        self.c_group_limit = c_group_limit
        self.full_day_off = full_day_off
        self.has_empty_slots = has_empty_slots
        self.excluded_periods = excluded_periods


if __name__ == '__main__':
    cond = req("基幹理工学部", "応用数理学科", 3, "秋学期", True, 1, 2, True, 3, 2, 1, 2, 0, 0, 3, False, [1, 5])
    df, er = make_timetable(cond)
    print(df, er)
