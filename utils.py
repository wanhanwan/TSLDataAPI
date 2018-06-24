# coding: utf-8
from pathlib import Path
import pandas as pd


def read_tableinfo():
    file_pth = Path(__file__).parents[0] / 'resource' / 'tsl_tableinfo.xlsx'
    tableInfo = pd.read_excel(file_pth, header=0, index_col=0)
    return tableInfo


def get_period_range(start, end, freq='1Q'):
    return pd.date_range(start, end, freq='1Q').strftime("%Y%m%d").tolist()


def get_all_cycles():
    prefix = 'cy_'
    freqs = ['60m', '6s', 'day', 'detail', '10m', '10s', '120m', '12s',
             '15m', '15s', '1m', '1s', '20m', '20s', '2m', '2s', '30m',
             '30s', '3m', '3s', '40m', '4s', '5m', '5s', 'month', 'quarter',
             'week', 'year']
    return [prefix+x for x in freqs]


def cycle_value_of(cycle_str):
    dict_ = {'m': '分钟线', 's': '秒线', 'quarter': '季线', 'week': '周线',
             'year': '年线', 'day': '日线', 'month': '月线'}
    freq = cycle_str.replace('cy_', '')
    if freq.isalpha():
        return dict_[freq]
    else:
        return freq[:-1]+dict_[freq[-1]]


def to_pandas_freq(freq_str):
    dict_ = {'m': 'T', 's': 'S', 'week': 'w',
             'month': 'm', 'quarter': 'q', 'day': 'd'}
    return dict_[freq_str]


def get_tsl_fundid(secID, ticker):
    if secID is not None:
        return ['OF%s' % x[:-2] for x in secID]
    return ['OF' + x for x in ticker]


if __name__ == '__main__':
    data = read_tableinfo()
