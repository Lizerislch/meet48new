import pandas as pd

def mk_df():
    file_path = '1.xlsx'
    df = pd.read_excel(file_path,dtype={'身高': str, '生日': str})
    df = df.dropna()
    return df


def constract_ques(df,question_text):
    matching_columns = [col for col in df.columns if col in question_text]
    if matching_columns:
        matching_column = matching_columns[0]
        matching_rows = df[df['姓名'].apply(lambda x: x in question_text)]

        if not matching_rows.empty:
            row_index = matching_rows.index[0]
            extracted_content = df.loc[row_index, matching_column]

    return extracted_content