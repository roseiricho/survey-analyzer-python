import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class SurveyAnalyzer:
    def __init__(self, file_path, layout):
        self.file_path = file_path
        self.layout = layout
        self.data = pd.read_csv(self.file_path)

    def format_data(self):
        # 列名に'_\d+入力欄'という文字列が含まれる列から'_'のみを削除
        # たとえば'Q5_12入力欄'を'Q5入力欄'に変更
        self.data.columns = self.data.columns.str.replace(r'_(\d+)入力欄', r'入力欄')

        prefixes = self.data.columns.str.split('_', n=1).str[0].unique()
        df_new = pd.DataFrame()
        for prefix in prefixes:
            # prefix+'_'で始める列を取得．マッチする列がない場合はprefixと完全一致する列を取得
            cols = self.data.columns[self.data.columns.str.match(prefix+'_')].tolist() or self.data.columns[self.data.columns == prefix].tolist()

            if cols:  # Check if cols is not empty 
                df_new[prefix] = self.data[cols].apply(lambda row: row.tolist(), axis=1) if len(cols) > 1 else self.data[cols[0]]
            
            # df_new[prefix]に配列が格納された場合，配列の中で1になっている要素がある場合はそのインデックスに1を足した値を格納
            if df_new[prefix].apply(lambda x: isinstance(x, list)).all():
                df_new[prefix] = df_new[prefix].apply(lambda x: [i+1 for i, v in enumerate(x) if v == 1])

        self.data = df_new
    
    def map_layout(self):
        for l in self.layout:
            column = l['column_name']
            answer_text = l['answer_text']
            if self.data[column].apply(lambda x: isinstance(x, list)).all():
                self.data[column] = self.data[column].apply(lambda x: [answer_text[i] for i in x])
            else:
                self.data[column] = self.data[column].map(answer_text)
    
    def download(self, file_path):
        self.data.to_csv(file_path, index=False)