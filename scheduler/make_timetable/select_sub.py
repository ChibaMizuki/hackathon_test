import pandas as pd
import ast


def score_0(row, max_row):
    if row["曜日"] == max_row[0] and len(set(row["時限"]) & set(max_row[1])) >= 1:
        return 0
    else:
        return row["score"]
    

def score_0_fullday(row, list_youbi):
    if row["曜日"] in list_youbi or row["曜日"] == "無":
        return row["score"]
    else:
        return 0


def select_sub(df_cand_subject, conditions):
    list_error = [True, "正常に終了"]
    is_fin = False
    do_full_day = False
    df_timetable = pd.DataFrame()
    i = 1
    while not is_fin:
        # 残っている科目候補の中で最大スコアのものを取得
        max_label = df_cand_subject["score"].idxmax()
        s_append = df_cand_subject.loc[max_label]
        if s_append["score"] == 0:
            list_error = [False, "条件を変えて再入力してください"]
            return df_timetable, list_error
        df_timetable = pd.concat([df_timetable, s_append.to_frame().T])
        df_cand_subject.drop(max_label, inplace=True)
        # 取得した科目と曜日と時限が等しい科目候補のスコアを0にする
        youbi = s_append["曜日"]
        jigen = s_append["時限"]
        df_cand_subject["score"] = df_cand_subject[["曜日", "時限", "score"]].apply(score_0, axis=1, args=([youbi, jigen],))
        # 現在の全休の数を計算
        list_youbi = df_timetable["曜日"].unique()
        if "無" in list_youbi:
            num_fullday = 6 - len(list_youbi)
        else:
            num_fullday = 5 - len(list_youbi)
        # 全休の数が指定の数になったタイミングで、現状の曜日以外のスコアを0にする
        if not do_full_day and num_fullday == conditions.full_day_off:
            df_cand_subject["score"] = df_cand_subject[["曜日", "score"]].apply(score_0_fullday, axis=1, args=(list_youbi,))
            do_full_day = True

        # 指定した単位数を超えたら終了
        a_unit = df_timetable[df_timetable["群"] == "A"]["単位数"].sum()
        b_unit = df_timetable[df_timetable["群"] == "B"]["単位数"].sum()
        c_unit = df_timetable[df_timetable["群"] == "C"]["単位数"].sum()
        print(a_unit)
        if i == 4:
            is_fin = True
        i+=1
        #print(df_cand_subject.loc[df_cand_subject["score"].idxmax()]["科目名"])
    
    return df_timetable, list_error


class req:
    def __init__(self, faculty, department, grade, semester, a_group_limit,
                 b_group_limit, c_group_limit, full_day_off):
        self.faculty = faculty
        self.department = department
        self.grade = grade
        self.semester = semester
        self.a_group_limit = a_group_limit
        self.b_group_limit = b_group_limit
        self.c_group_limit = c_group_limit
        self.full_day_off = full_day_off


if __name__ == '__main__':
    cond = req("基幹理工学部", "応用数理学科", "3", "秋学期", 2, 2, 2, 3)
    df_cand_subject = pd.read_csv("data/subject2.csv")
    df_cand_subject["時限"] = df_cand_subject["時限"].apply(ast.literal_eval)
    df_cand_subject.set_index("科目キー", inplace=True)
    df_timetable, list_error = select_sub(df_cand_subject, cond)
    print(df_timetable[["科目名", "曜日", "時限"]])
    df_timetable[["科目名", "曜日", "時限"]].to_csv("data/dataframe.csv")
