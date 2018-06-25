# coding: utf-8
"""股票财务数据"""

from .BaseAPI import StatementGet
import pandas as pd


def AShareBalanceSheetGet(secID=None, ticker=None, beginReportDate=None, endReportDate=None,
                          reportDate=None, baseDate=None, field='*'):
    """股票资产负债表"""
    table_id = 44
    data = StatementGet(table_id, '截止日', secID, ticker, beginReportDate, endReportDate, baseDate,
                        reportDate, field)
    data.index = data.index.set_levels(
        [pd.PeriodIndex(data.index.levels[0], freq='D').to_timestamp()],
        level=['date'])
    return data


def AshareIncomeSheetGet(secID=None, ticker=None, beginReportDate=None, endReportDate=None,
                         reportDate=None, baseDate=None, field='*'):
    """股票利润表"""
    table_id = 46
    data = StatementGet(table_id, '截止日', secID, ticker, beginReportDate, endReportDate, baseDate,
                        reportDate, field)
    data.index = data.index.set_levels(
        [pd.PeriodIndex(data.index.levels[0], freq='D').to_timestamp()],
        level=['date'])
    return data


def AshareSQIncomeSheetGet(secID=None, ticker=None, beginReportDate=None, endReportDate=None,
                           reportDate=None, baseDate=None, field='*'):
    """股票单季度利润表"""
    table_id = 46
    func_name = 'LastQuarterData'
    data = StatementGet(table_id, '截止日', secID, ticker, beginReportDate, endReportDate,
                        baseDate, reportDate, field, func_name)
    data.index = data.index.set_levels(
        [pd.PeriodIndex(data.index.levels[0], freq='D').to_timestamp()],
        level=['date'])
    return data


def AshareTTMIncomeSheetGet(secID=None, ticker=None, beginReportDate=None, endReportDate=None,
                            reportDate=None, baseDate=None, field='*'):
    """股票TTM利润表"""
    table_id = 46
    func_name = 'Last12MData'
    data = StatementGet(table_id, '截止日', secID, ticker, beginReportDate, endReportDate,
                        baseDate, reportDate, field, func_name)
    data.index = data.index.set_levels(
        [pd.PeriodIndex(data.index.levels[0], freq='D').to_timestamp()],
        level=['date'])
    return data
