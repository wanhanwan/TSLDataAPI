# coding: utf-8
from FactorLib.utils.tool_funcs import windcode_to_tradecode, windcode_to_tslcode, tradecode_to_tslcode
from FactorLib.data_source.tsl_data_source import (CsQuery, PanelQuery, PanelQueryByStocks,
                                                   CsQueryMultiFields, run_function)
from FactorLib.utils.TSDataParser import parse1DArray, parse2DArrayWithIDIndex
from FactorLib.data_source.base_data_source_h5 import tc
from datetime import datetime
import pandas as pd

from .TableInfo import tsl_dict
from .utils import get_period_range, get_all_cycles, cycle_value_of, to_pandas_freq


def _get_secIDs(secID, ticker):
    if secID is not None:
        if isinstance(secID, str):
            stocks = [windcode_to_tslcode(secID)]
        else:
            stocks = [windcode_to_tslcode(x) for x in secID]
    elif ticker is not None:
        if isinstance(ticker, str):
            stocks = [tradecode_to_tslcode(ticker)]
        else:
            stocks = [tradecode_to_tslcode(x) for x in ticker]
    else:
        stocks = None
    return stocks


def StatementGet(table_id, reportDateField, secID=None, ticker=None, beginReportDate=None, endReportDate=None,
                 baseDate=None, reportDate=None, field='*', func_name='report'):
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
    stocks = _get_secIDs(secID, ticker)

    if field == '*':
        factor_ids = tsl_dict.get_table_columns(table_id)
    else:
        if reportDateField not in field:
            field.append(reportDateField)
        factor_ids = tsl_dict.get_factor_id_by_names(table_id, field)
    eng_names = tsl_dict.get_factor_eng_names_by_id(factor_ids)
    baseDate = datetime.strptime(baseDate, "%Y%m%d") if baseDate is not None else datetime.today()
    reportDate_eng_name = tsl_dict.get_factor_eng_names([reportDateField])[0]

    if reportDate is None:
        all_dates = get_period_range(beginReportDate, endReportDate)
    else:
        all_dates = [reportDate]

    rslt = []
    for d in all_dates:
        if func_name == 'report':
            field_dict = {"'%s'"%name: '%s(%d, %s)'%(func_name, func, d)
                          for name, func in zip(eng_names, factor_ids)}
        else:
            field_dict = {"'%s'" % name: '%s(%s, %d)' % (func_name, d, func)
                          for name, func in zip(eng_names, factor_ids)}
        if stocks is not None:
            data = CsQuery(field_dict, baseDate, "''", stocks, code_transfer=False)
        else:
            data = CsQuery(field_dict, baseDate)
        data[reportDate_eng_name] = data[reportDate_eng_name].replace(0, int(d))
        rslt.append(data)
    return pd.concat(rslt)


def QuotaGet(table_id, secID=None, ticker=None, beginTradeDate=None, endTradeDate=None, tradeDate=None,
             field='*', cycle='cy_day', rate=0, sysparams=None, **kwargs):
    """
    历史行情数据提取，例如高开低收量额等字段。支持时间序列和横截面提取。


    Parameters:
    ----------------------------------
        table_id: int
            天软数据库中的表ID
        secID: str or list of str
            Wind格式的股票代码
        ticker: str or list of str
            股票交易代码
        beginTradeDate: str
            起始交易日, YYYYMMDD
        endTradeDate: str
            结束交易日
        reportDate: str
            单个交易日
        filed: list
            返回字段, '*'代表返回所有字段
        cycle: str
            时间周期，年线、月线、周线、日线、分钟线、秒线
        rate: int
            是否复权
    """
    def _get_params(func_params):
        r = []
        for f_id, p in func_params.items():
            if p == '':
                r.append(p)
            else:
                pv = [str(kwargs.get(x, 0)) for x in p]
                r.append(','.join(pv))
        return r

    all_cycles = get_all_cycles()
    assert cycle in all_cycles
    cycle_value = cycle_value_of(cycle)

    stocks = _get_secIDs(secID, ticker)

    if cycle.split('_')[1][-1] in ['s', 'm']:
        pandas_freq = cycle.split('_')[1][:-1] + to_pandas_freq(cycle.split('_')[1][-1])
        dates = tc.get_trade_time(beginTradeDate+' 09:30:00', endTradeDate+' 15:00:00',
                                  freq=pandas_freq, retstr=None)
    elif tradeDate is not None:
        dates = [pd.to_datetime(tradeDate)]
    else:
        pandas_freq = '1' + to_pandas_freq(cycle.split('_')[1])
        dates = tc.get_trade_days(beginTradeDate, endTradeDate, freq=pandas_freq, retstr=None)

    if field == '*':
        factor_ids = tsl_dict.get_table_columns(table_id)
    else:
        factor_ids = tsl_dict.get_factor_id_by_names(table_id, field)
    funcs = tsl_dict.get_note_by_id(factor_ids)
    func_params = _get_params(tsl_dict.get_params_by_id(factor_ids))
    factor_names = tsl_dict.get_factor_eng_names_by_id(factor_ids)

    sysparams2 = {'bRate': rate, 'Cycle': cycle_value}
    if sysparams is not None:
        sysparams2.update(sysparams)
    # 从效率角度考虑，如果股票数量超过日期数量，按股票进行循环；反之，按日期循环。
    field_str = {"'%s'"%name: '%s(%s)'%(func, param) for name, func, param in
                 zip(factor_names, funcs, func_params)}
    if (stocks is None) or (len(stocks) > len(dates)):
        if stocks is None:
            rslt = PanelQuery(field_str, dates=dates, **sysparams2)
        else:
            rslt = PanelQuery(field_str, dates=dates, bk_name="''", stock_list=stocks,
                              code_transfer=False, **sysparams2)
    else:
        rslt = PanelQueryByStocks(field_str, stocks, dates=dates, code_transfer=False,**sysparams2)
    return rslt


def InfoArrayGet(table_id, func_name, secID=None, ticker=None, beginReportDate=None,
                 endReportDate=None, reportDate=None, field='*', baseDate=None):
    """
    数据表信息提取。适用于单季度多条数据，对应天软infoarray()函数
    """
    stocks = _get_secIDs(secID, ticker)
    if field == '*':
        factor_ids = tsl_dict.get_table_columns(table_id)
    else:
        factor_ids = tsl_dict.get_factor_id_by_names(table_id, field)
    if reportDate is None:
        all_dates = get_period_range(beginReportDate, endReportDate)
    else:
        all_dates = [reportDate]
    factor_names = tsl_dict.get_factor_name_by_id(factor_ids)
    factor_eng_names = tsl_dict.get_factor_eng_names_by_id(factor_ids)
    mapping = {x: y for x, y in zip(factor_names, factor_eng_names)}
    baseDate = datetime.strptime(baseDate, "%Y%m%d") if baseDate is not None else datetime.today()

    rslt = [None] * len(all_dates)
    for i, d in enumerate(all_dates):
        field_dict = {"'data'": '%s(%s)' % (func_name, d)}
        if stocks is None:
            data = CsQueryMultiFields(field_dict, baseDate)
        else:
            data = CsQueryMultiFields(field_dict, baseDate, "''", stocks, code_transfer=False)
        rslt[i] = data
    rslt = pd.concat(rslt)
    return rslt[factor_names].rename(columns=mapping)


def InfoArrayGet2(table_id, func_name, secID=None, ticker=None, beginDate=None,
                  endDate=None, tradeDate=None, field='*', baseDate=None):
    stocks = _get_secIDs(secID, ticker)
    if field == '*':
        factor_ids = tsl_dict.get_table_columns(table_id)
    else:
        factor_ids = tsl_dict.get_factor_id_by_names(table_id, field)
    if tradeDate is None:
        all_dates = tc.get_trade_days(beginDate, endDate)
    else:
        all_dates = [tradeDate]
    factor_names = tsl_dict.get_factor_name_by_id(factor_ids)
    factor_eng_names = tsl_dict.get_factor_eng_names_by_id(factor_ids)
    mapping = {x: y for x, y in zip(factor_names, factor_eng_names)}
    baseDate = datetime.strptime(baseDate, "%Y%m%d") if baseDate is not None else datetime.today()

    rslt = [None] * len(all_dates)
    for i, d in enumerate(all_dates):
        field_dict = {"'data'": '%s(%s)' % (func_name, d)}
        if stocks is None:
            data = CsQueryMultiFields(field_dict, baseDate)
        else:
            data = CsQueryMultiFields(field_dict, baseDate, "''", stocks, code_transfer=False)
        data.index = pd.MultiIndex.from_product([[pd.to_datetime(d)], data.index],
                                                names=['date', 'IDs'])
        rslt[i] = data
    rslt = pd.concat(rslt)
    return rslt[factor_names].rename(columns=mapping)


def BaseGet(table_id, secID=None, ticker=None, field='*', baseDate=None, bk=None):
    """对应天软base()函数"""
    stocks = _get_secIDs(secID, ticker)
    if field == '*':
        factor_ids = tsl_dict.get_table_columns(table_id)
    else:
        factor_ids = tsl_dict.get_factor_id_by_names(table_id, field)
    factor_eng_names = tsl_dict.get_factor_eng_names_by_id(factor_ids)
    baseDate = datetime.strptime(baseDate, "%Y%m%d") if baseDate is not None else datetime.today()
    field_dict = {"'%s'"%name: 'base(%d)' % factor for name, factor in zip(factor_eng_names, factor_ids)}
    if stocks is not None:
        return CsQuery(field_dict, baseDate, "''", stocks, code_transfer=False)
    elif bk is not None:
        return CsQuery(field_dict, baseDate, bk, stocks)
    else:
        return CsQuery(field_dict, baseDate)


def UserCrossSectionFuncGet(func_name, beginDate=None, endDate=None, tradeDate=None,
                            colname_used=None, dimension='1D'):
    """执行天软客户端中自定义的函数体
    这个函数体只接受一个时间(Int)参数，返回一个一维数组，
    一维数组的坐标是股票代码，表示在这个时间点的全市场面数据。
    """
    def _getData(func_name, dt, colname_used, dimension):
        data = run_function(func_name, dt)
        if dimension == '1D':
            df = parse1DArray(data, col_name=colname_used)
        elif dimension == '2D':
            df = parse2DArrayWithIDIndex(data)
        else:
            raise NotImplementedError("dimension must be set '1D' or '2D'.")
        return df

    if colname_used is None:
        colname_used = func_name

    if tradeDate is not None:
        if not isinstance(tradeDate, list):
            tradeDate = [tradeDate]
    else:
        tradeDate = tc.get_trade_days(beginDate, endDate)

    l = [None] * len(tradeDate)
    for i, dt in enumerate(tradeDate):
        print("函数执行日期：%s"%dt)
        l[i] = _getData(func_name, dt, colname_used, dimension=dimension)
    df = pd.concat(l, keys=pd.to_datetime(tradeDate, format='%Y%m%d'))
    df.index.names = ['date', 'IDs']
    return df
