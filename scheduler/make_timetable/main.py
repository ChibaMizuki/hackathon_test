import pandas as pd


def make_timetable(conditions):

    df_cand_subject = pd.read_csv("data/subject.csv")
    df_timetable = pd.DataFrame({
        '授業名': ['数学基礎論'],
        '曜日': ["木"],
        '時限': [5]
        })
    df_timetable = get_req_sub(df_timetable, df_cand_subject, conditions)


    return df_timetable


if __name__ == '__main__':
    df = make_timetable("aa")
