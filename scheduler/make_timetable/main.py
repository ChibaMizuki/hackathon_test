import pandas as pd
from select_sub import select_sub
from score import score
import ast


def make_timetable(conditions):
    df_cand_subject = pd.read_csv("data/subject.csv")
    df_timetable = pd.DataFrame()
    df_cand_subject["時限"] = df_cand_subject["時限"].apply(ast.literal_eval)
    df_cand_subject["score"] = 10
    df_cand_subject, list_error = score(df_cand_subject, conditions)
    if not list_error[0]:
        return df_timetable, list_error
    df_timetable, list_error = select_sub(df_cand_subject, conditions)
    #print("学部表示:"+conditions.department)
    #df_cand_subject = score(df_timetable, df_cand_subject, conditions)

    return df_timetable, list_error


if __name__ == '__main__':
    df = make_timetable("aa")
