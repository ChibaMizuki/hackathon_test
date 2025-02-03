import pandas as pd


def make_timetable(conditions):
    df_timetable = pd.DataFrame({
        '授業名' :['数学基礎論'],
        '曜日' : ["木"],
        '時限' : [5]
        })
    return df_timetable


if __name__ == '__main__':
    df = make_timetable("aa")