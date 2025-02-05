import pandas as pd


def score(df_cand_subject, conditions):
    list_error = [True, "正常に終了"]
    df = df_cand_subject
    #必修処理
    if conditions.required == True:
        if df["必修"] == "必修":
            score += 10000
        elif df["必修"] == "選択必修":
            score += 5000
        #選択の場合は省略
    #科目難易度のスコア算出
    if conditions.easy_level == 1:
        score += conditions.easy_level_priority * df["レベル"]  # 楽単優先なら難易度
    else:
        score += conditions.easy_level_priority * (5 - df["レベル"])  # 高難易度優先なら 5-難易度
    # 内容区分のスコア
    score += conditions.attendance_priority*df["出席"]
    score += conditions.test_priority*df["テスト"]
    score += conditions.report_priority*df["レポート"]
    #オンデマのスコア
    if conditions.is_ondemand_priorit == True:
        score += 80 
    return df, list_error


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