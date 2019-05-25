import pandas as pd

def save_data_from_file(file_name, sep, flg_have_header):
    if flg_have_header:
        pd_dic = pd.read_csv(file_name, sep='\t')
    else:
        pd_dic = pd.read_csv(file_name, sep='\t', header=None)
    final_dict = [dic for index, dic in pd_dic.to_dict(orient="index").items() if index!=0]
    # 下記は後ほど説明
    save_dict("your collection", final_dict)

if __name__ == "__main__":
    save_data_from_file(file_name='pn.csv', sep='\t', flg_have_header=None)