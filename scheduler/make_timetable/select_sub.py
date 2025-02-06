import pandas as pd
import ast


def score_0(row, max_row):
    # 選択した科目と時間が被っている科目のスコアを0にする
    if row["曜日"] == max_row[0] and len(set(row["時限"]) & set(max_row[1])) >= 1:
        return 0
    else:
        return row["score"]


def score_emptyslot(row, max_row):
    # 選択したコマの前と後の科目のスコアに40加算する
    if len(row["時限"]) == 0 or len(max_row[1]) == 0:
        return row["score"]

    isbefore = max_row[1][0] != 1 and max_row[1][0] - row["時限"][-1] == 1
    isafter = max_row[1][-1] != 6 and max_row[1][-1] - row["時限"][0] == -1
    if row["曜日"] == max_row[0] and (isbefore or isafter):
        if row["score"] == 0:
            return 0
        else:
            return row["score"] + 40
    else:
        return row["score"]


def score_0_fullday(row, list_youbi):
    # 全休希望日数を越さないように、その他の科目のスコアを0にする
    if row["曜日"] in list_youbi or row["曜日"] == "無":
        return row["score"]
    else:
        if row["score"] >= 10000:
            return row["score"]
        else:
            return 0


def select_sub(df_cand_subject, conditions):
    list_error = [True, "正常に終了"]
    is_fin = False
    req_fin = False
    a_fin = False
    b_fin = False
    c_fin = False
    do_full_day = False
    df_timetable = pd.DataFrame()

    while not is_fin:
        # 残っている科目候補の中で最大スコアのものを取得
        max_label = df_cand_subject["score"].idxmax()
        s_append = df_cand_subject.loc[max_label]
        # 最大スコアが0で、まだ終了していない場合、エラー出力
        if s_append["score"] == 0:
            msg_error = ""
            if not a_fin:
                msg_error += "A群の必要単位数下限が多すぎます。"
            if not b_fin:
                msg_error += "B群の必要単位数下限が多すぎます。"
            if not c_fin:
                msg_error += "C群の必要単位数下限が多すぎます。"
            if do_full_day:
                msg_error += "全休希望日数が多すぎます。"
            msg_error += "条件を変えて再入力してください"
            list_error = [False, msg_error]
            return df_timetable, list_error
        # 取得した科目の群がまだ必要かを確認
        if ((s_append["群"] == "A" and a_fin) or (s_append["群"] == "B" and b_fin) or (s_append["群"] == "C" and c_fin)) and req_fin:
            df_cand_subject.drop(max_label, inplace=True)
        else:
            df_timetable = pd.concat([df_timetable, s_append.to_frame().T])
            df_cand_subject.drop(max_label, inplace=True)
            # 取得した科目と曜日と時限が等しい科目候補のスコアを0にする
            youbi = s_append["曜日"]
            jigen = s_append["時限"]
            df_cand_subject["score"] = df_cand_subject[["曜日", "時限", "score"]].apply(score_0, axis=1, args=([youbi, jigen],))

            # 空きコマを作らせない場合、追加する科目の前後の時限のスコアを+40する
            if conditions.has_empty_slots:
                df_cand_subject["score"] = df_cand_subject[["曜日", "時限", "score"]].apply(score_emptyslot, axis=1, args=([youbi, jigen],))

            # 現在の全休の数を計算
            list_youbi = df_timetable["曜日"].unique()
            if "無" in list_youbi:
                num_fullday = 6 - len(list_youbi)
            else:
                num_fullday = 5 - len(list_youbi)

            # 全休の数が指定の数になったタイミングで、現状の曜日以外のスコアを0にする
            if (not do_full_day) and num_fullday == conditions.full_day_off:
                df_cand_subject["score"] = df_cand_subject[["曜日", "score"]].apply(score_0_fullday, axis=1, args=(list_youbi,))
                do_full_day = True

            # 指定した単位数を超えたら終了
            a_unit = df_timetable[df_timetable["群"] == "A"]["単位数"].sum()
            b_unit = df_timetable[df_timetable["群"] == "B"]["単位数"].sum()
            c_unit = df_timetable[df_timetable["群"] == "C"]["単位数"].sum()
            if a_unit >= conditions.a_group_limit:
                a_fin = True
            if b_unit >= conditions.b_group_limit:
                b_fin = True
            if c_unit >= conditions.c_group_limit:
                c_fin = True
            # A,B,C群をすべて取り、必修も取り切ったら終了
            if a_fin and b_fin and c_fin:
                max_label = df_cand_subject["score"].idxmax()
                s_append = df_cand_subject.loc[max_label]
                if not s_append["score"] >= 10000:
                    is_fin = True
    df_timetable = df_timetable[["科目名", "曜日", "時限", "群"]]
    df_timetable["URL"] = "https://www.wsl.waseda.jp/syllabus/JAA104.php?pKey=2602012001012024260101200526&pLng=jp"
    subkey_nasi = df_timetable[df_timetable["曜日"] == "無"].index.to_list()
    for i, key in enumerate(subkey_nasi):
        df_timetable.loc[key, "時限"] = [i+1]
    return df_timetable, list_error


class req:
    def __init__(self, faculty, department, grade, semester, a_group_limit,
                 b_group_limit, c_group_limit, full_day_off, has_empty_slots):
        self.faculty = faculty
        self.department = department
        self.grade = grade
        self.semester = semester
        self.a_group_limit = a_group_limit
        self.b_group_limit = b_group_limit
        self.c_group_limit = c_group_limit
        self.full_day_off = full_day_off
        self.has_empty_slots = has_empty_slots


if __name__ == '__main__':
    cond = req("基幹理工学部", "応用数理学科", "3", "秋学期", 12, 0, 0, 3, False)
    df_cand_subject = pd.read_csv("data/subject2.csv")
    df_cand_subject["時限"] = df_cand_subject["時限"].apply(ast.literal_eval)
    df_cand_subject.set_index("科目キー", inplace=True)
    df_timetable, list_error = select_sub(df_cand_subject, cond)
    print(df_timetable[["科目名", "曜日", "時限", "群"]])
    print(list_error)
    df_timetable[["科目名", "曜日", "時限", "群"]].to_csv("data/dataframe.csv")
