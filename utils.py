# coding: utf-8
from pathlib import Path
import pandas as pd


def read_tableinfo():
    file_pth = Path(__file__).parents[0] / 'resource' / 'tsl_tableinfo.xlsx'
    tableInfo = pd.read_excel(file_pth, header=0, index_col=0)
    return tableInfo


def get_period_range(start, end, freq='1Q'):
    return pd.date_range(start, end, freq='1Q').strftime("%Y%m%d").tolist()


if __name__ == '__main__':
    data = read_tableinfo()
