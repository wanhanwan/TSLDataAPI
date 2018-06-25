# coding: utf-8
"""
指数数据库
"""
from FactorLib.data_source.tsl_data_source import TSLDBOnline
from .BaseAPI import get_period_range, tsl_dict, QuotaGet
from datetime import datetime
from FactorLib.data_source.tsl_data_source import encode_datetime, run_script
import pandas as pd


tsl_db = TSLDBOnline()


def IndexConstituentGet(bk_name, startTradeDate=None, endTradeDate=None,
                        tradeDate=None):
    """指数成分股提取

    Parameters:
    ---------------------------
    bk_name: str
        板块的中文名称。如：沪深300、中证500、中证800
    """
    if tradeDate is not None:
        tradeDate = [tradeDate]
    return tsl_db.get_index_members(bk_name,
                                    start_date=startTradeDate,
                                    end_date=endTradeDate,
                                    dates=tradeDate)


def IndexWeightGet(bk_id, startTradeDate=None, endTradeDate=None,
                   tradeDate=None):
    """指数成分股权重提取
    Parameters:
    ---------------------------
    bk_id: str
        板块的代码。如：SH000300, SH000905, SH000906
    """
    if tradeDate is not None:
        tradeDate = [tradeDate]
    return tsl_db.get_index_weight(bk_id,
                                   start_date=startTradeDate,
                                   end_date=endTradeDate,
                                   dates=tradeDate)


def IndexFinancialDerivativeGet(bk_name, field='*', startReportDate=None,
                                endReportDate=None, reportDate=None, baseDate=None,
                                **kwargs):
    """指数财务衍生指标
    根据天软板块数据专家中一系列的板块财务函数计算。

    Parameters:
    --------------------------------------------
    bk_name: str
     板块名称，如：沪深300、中证500、中证800
    field: str or list of str
        字段名称
    weight_type: int
        加权方式。0：总股本加权；1：流通股本加权；4：算术平均
    stock_type: int
        股票类型。0：全部；1：只考虑A股；2：只考虑B股
    sample_type: int
        样本股选择 0：所有个股参与计算；1：剔除每股收益<0的股票
    cal_type: int
       计算类型。 0：平均值；1：合计 一般用于财务基本指标，如净利润合计或净利润平均值
    eps_criterion: float
        绩差股标准。
    """
    def _create_script(func_name, func_params, report_date):
        s = "SetSysParam(pn_bk(),'%s'); data:="%bk_name + func_name + '('
        for f in func_params:
            if f == 'report_date':
                s += (report_date + ',')
            else:
                s += (str(kwargs.get(f, 0))+',')
        s = s.strip(',') + ');'
        s += 'return data;'
        return s

    table_id = 2
    if field == "*":
        field = tsl_dict.get_table_columns(table_id)
    else:
        field = tsl_dict.get_factor_id_by_names(table_id, field)
    if reportDate is not None:
        dates = [reportDate]
    else:
        dates = get_period_range(startReportDate, endReportDate)
    baseDate = datetime.strptime(baseDate, "%Y%m%d") if baseDate is not None else datetime.today()
    funcs = tsl_dict.get_note_by_id(field)
    eng_names = tsl_dict.get_factor_eng_names_by_id(field)
    dt_encoded = encode_datetime(baseDate)
    sysparams = {'CurrentDate': dt_encoded}

    rslt = pd.DataFrame(index=[int(x) for x in dates],
                        columns=eng_names)
    for i, i_field in enumerate(field):
        func_params = tsl_dict.get_params_by_id([i_field])
        for report_date in dates:
            script = _create_script(funcs[i], func_params[i_field], report_date)
            data = run_script(script, sysparams)
            data = data[1]
            rslt.at[int(report_date), eng_names[i]] = data
    rslt.index.name = 'report_date'
    return rslt


def IndexValuationGet(bk_name, beginTradeDate=None, endTradeDate=None, tradeDate=None,
                      field='*', **kwargs):
    """板块的估值指标
    
    Parameters:
    --------------------------------------------
    bk_name: str
     板块名称，如：沪深300、中证500、中证800
    field: str or list of str
        字段名称
    weight_type: int
        加权方式。0：总股本加权；1：流通股本加权；4：算术平均
    stock_type: int
        股票类型。0：全部；1：只考虑A股；2：只考虑B股
    sample_type: int
        样本股选择 0：所有个股参与计算；1：剔除每股收益<0的股票
    cal_type: int
       计算类型。 0：平均值；1：合计 一般用于财务基本指标，如净利润合计或净利润平均值
    eps_criterion: float
        绩差股标准。
    """
    table_id = 4
    sysparam = {'CurrentBkName': bk_name}
    bk_id = ['000300.SH']
    return QuotaGet(table_id, secID=bk_id, beginTradeDate=beginTradeDate,
                    endTradeDate=endTradeDate, tradeDate=tradeDate, field=field,
                    sysparams=sysparam, **kwargs).reset_index('IDs', drop=True)


def IndexEodPricesGet(secID=None, beginTradeDate=None, endTradeDate=None,
                      tradeDate=None, field='*', cycle='cy_day', **kwargs):
    """指数行情"""
    table_id = 3
    return QuotaGet(table_id, secID=secID, beginTradeDate=beginTradeDate,
                    endTradeDate=endTradeDate, tradeDate=tradeDate, field=field,
                    cycle=cycle, **kwargs)