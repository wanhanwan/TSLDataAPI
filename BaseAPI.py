# coding: utf-8
from FactorLib.utils.tool_funcs import windcode_to_tradecode
from FactorLib.data_source.tsl_data_source import CsQuery
from datetime import datetime
import pandas as pd

from .TableInfo import tsl_dict
from .utils import get_period_range


def StatementGet(table_id, reportDateField, secID=None, ticker=None, beginReportDate=None, endReportDate=None,
                 baseDate=None, reportDate=None, field='*'):
    """
    报表因子的提取
    输入天软某张表的ID，返回这张表的字段。适用于财务报表等按季度更新的数据, 并以天软中report函数为基础。

    Parameters:
    ----------------------------------
        table_id: int
            天软数据库中的表ID
        reportDateField: str
            该表中作为报告期的字段名称
        secID: str or list of str
            Wind格式的股票代码
        ticker: str or list of str
            股票交易代码
        beginReportDate: str
            起始报告期, YYYYMMDD
        endReportDate: str
            结束报告期
        baseDate: str
            基准日。这是天软数据库的特色，天软在取数据时，首先应该设置pn_date()。这样做的
            目的是为了防止使用到未来数据。该API返回的所有数据都确保能在baseDate当日获得。
        reportDate: str
            报告期
        filed: list
            返回字段, '*'代表返回所有字段
    """
    if secID is not None:
        if isinstance(secID, str):
            stocks = [windcode_to_tradecode(secID)]
        else:
            stocks = [windcode_to_tradecode(x) for x in secID]
    elif ticker is not None:
        if isinstance(ticker, str):
            stocks = [ticker]
        else:
            stocks = ticker
    else:
        stocks = None

    if field == '*':
        factor_ids = tsl_dict.get_table_columns(table_id)
    else:
        if reportDateField not in field:
            field.append(reportDateField)
        factor_ids = tsl_dict.get_factor_id_by_names(field)
    eng_names = tsl_dict.get_factor_eng_names_by_id(factor_ids)
    baseDate = datetime.strptime(baseDate, "%Y%m%d") if baseDate is not None else datetime.today().date()
    reportDate_eng_name = tsl_dict.get_factor_eng_names([reportDateField])[0]

    if reportDate is None:
        all_dates = get_period_range(beginReportDate, endReportDate)
    else:
        all_dates = [reportDate]

    rslt = []
    for d in all_dates:
        field_dict = {"'%s'"%name: 'report(%d, %s)'%(func, d) for name, func in zip(eng_names, factor_ids)}
        if stocks is not None:
            data = CsQuery(field_dict, baseDate, "''", stocks)
        else:
            data = CsQuery(field_dict, baseDate)
        data[reportDate_eng_name] = data[reportDate_eng_name].replace(0, int(d))
        rslt.append(data)
    return pd.concat(rslt)
