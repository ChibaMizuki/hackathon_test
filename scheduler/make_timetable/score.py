import pandas as pd
import ast


def score(df_cand_subject, conditions):
    list_error = [True, "正常に終了"]
    df = df_cand_subject
    df["score"] = 1
    df = df.reset_index(drop=True)  # インデックスをリセット
    # 必修処理
    if conditions.required:
        df.loc[df["必修"] == "必修", "score"] += 10000
        df.loc[df["必修"] == "選択必修", "score"] += 5000
    # 選択の場合は省略
    # 科目難易度のスコア算出
    if conditions.easy_level == 1:
        df["score"] += conditions.easy_level_priority * df["単位取得難易度"].astype(float)  # 楽単優先なら難易度
    else:
        df["score"] += conditions.easy_level_priority * (5 - df["単位取得難易度"])  # 高難易度優先なら 5-難易度
    # 内容区分のスコア
    df["score"] += conditions.report_priority*df["レポート"]
    df["score"] += conditions.attendance_priority*df["出席"]
    df["score"] += conditions.test_priority*df["テスト"]
    # オンデマのスコア
    if conditions.is_ondemand_priority:
        df.loc[df["授業方法区分"] == "【オンライン】フルオンデマンド", "score"] += 80
        df["score"] += 80
    df.loc[
       ~((df["学部"] == conditions.faculty) &
         (df['学科'].apply(lambda x: conditions.department in x)) &
         (df["学年"] == conditions.grade) &
         (df["学期"] == conditions.semester)),
       "score"
    ] = 0
    for t in conditions.excluded_periods:
        t = int(t)
        df.loc[df['時限'].apply(lambda x: t in x), "score"] = 0

    return df, list_error


class req:
    def __init__(self, faculty, department, grade, semester, required, easy_level, easy_level_priority, is_ondemand_priority, report_priority, attendance_priority, test_priority, excluded_periods):
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
        self.excluded_periods = excluded_periods


if __name__ == '__main__':
    cond = req("基幹理工学部", "応用数理学科", 3, "春学期", True,1,2,True,3,2,1,[1,5])
    df_cand_subject = pd.read_csv("data/subject3.csv")
    df_cand_subject["時限"] = df_cand_subject["時限"].apply(ast.literal_eval)
    df_timetable = pd.DataFrame()
    df_cand_subject = score(df_cand_subject, cond)
    print(df_cand_subject)
