import pandas as pd


def score(df_cand_subject, conditions):
    list_error = [True, "正常に終了"]

    return df_cand_subject, list_error


class req:
    def __init__(self, faculty, department, grade, semester):
        self.faculty = faculty
        self.department = department
        self.grade = grade
        self.semester = semester


if __name__ == '__main__':
    cond = req("基幹理工学部", "応用数理学科", "3", "秋学期")
    df_cand_subject = pd.read_csv("data/subject.csv")
    df_timetable = pd.DataFrame()
    score(df_cand_subject, cond)