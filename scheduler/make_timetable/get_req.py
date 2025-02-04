import pandas as pd


def get_req_sub(df_timetable, df_cand_subject, conditions):

    
    return df_timetable


class req:
    def __init__(self, faculty, department, grade, semester):
        self.faculty = faculty
        self.department = department
        self.grade = grade
        self.semester = semester


if __name__ == '__main__':
    cond = req("基幹理工学部", "応用数理学科", "3", "秋")
    df_cand_subject = pd.read_csv("data/subject.csv")
    df_timetable = pd.DataFrame()
    get_req_sub(df_timetable, df_cand_subject, cond)