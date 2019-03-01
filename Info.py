# coding: utf-8
"""
基本信息数据库
"""
from FactorLib.data_source.tsl_data_source import CsQuery, decode_date
from datetime import datetime
from .utils import _get_secIDs


def StockBaseInfoGet(secID=None, ticker=None, field=None):
    """A股基础信息
    field包括：
        'name': 股票简称
        'list_date': 上市日期
        'sw_level_1': 所属申万一级行业
        'sw_level_2': 所属申万二级行业
    """
    field_dict = {
        "'name'": 'base(10004)',
        "'list_date'": 'firstday()',
        "'sw_level_1'": 'base(10029)',
        "'sw_level_2'": 'base(10030)',
    }
    today = datetime.today()
    end_date = datetime(today.year, today.month, today.day)
    stocks = _get_secIDs(secID, ticker)
    data = CsQuery(field_dict, end_date, stock_list=stocks)
    data['name'] = data['name'].str.decode('GBK')
    data['sw_level_1'] = data['sw_level_1'].str.decode('GBK')
    data['sw_level_2'] = data['sw_level_2'].str.decode('GBK')
    data['list_date'] = data['list_date'].apply(decode_date)
    data.sort_index(inplace=True)
    if field is None:
        return data
    return data[field]
