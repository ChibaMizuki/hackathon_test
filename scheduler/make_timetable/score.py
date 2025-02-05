import pandas as pd
import ast


def score(df_cand_subject, conditions):
    df_cand_subject["時限"] = df_cand_subject["時限"].apply(ast.literal_eval)
    jigen = df_cand_subject[df_cand_subject["曜日"] == "火"]["時限"].iloc[0]
    print(jigen[0], conditions.semester)
    df1 = pd.DataFrame(
        data={'時限': [[1], [1, 2], [3]]}
    )
    df1.to_csv("data/test.csv")
    print(df1)
    
    return df_cand_subject


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