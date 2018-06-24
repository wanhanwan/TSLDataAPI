# coding: utf-8

"""基金数据库"""
from .BaseAPI import InfoArrayGet, QuotaGet, BaseGet
from .utils import get_tsl_fundid


def FundEqyInfoGet(secID=None, ticker=None, beginReportDate=None, endReportDate=None, reportDate=None,
                   field='*', baseDate=None):
    """
    基金持仓明细
    """
    func_name = 'FundHoldInfoGet'
    table_id = 318
    ticker = get_tsl_fundid(secID, ticker)
    raw = InfoArrayGet(table_id, func_name, ticker=ticker, beginReportDate=beginReportDate,
                       endReportDate=endReportDate, reportDate=reportDate, field=field,
                       baseDate=baseDate)
    if 'code' in raw.columns:
        raw['code'] = raw['code'].str.decode('GBK')
    return raw.reset_index()


def FundNavGet(secID=None, ticker=None, beginTradeDate=None, endTradeDate=None, tradeDate=None,
               field='*'):
    """基金净值
    """
    table_id = 1
    cycle = 'cy_day'
    return QuotaGet(table_id, secID, ticker, beginTradeDate, endTradeDate, tradeDate, field, cycle)


def FundBasicInfoGet(secID=None, ticker=None, field='*'):
    """
    基金基本信息
    """
    table_id = 302
    fund = "'上证基金;深证基金;开放式基金'"
    try:
        ticker = get_tsl_fundid(secID, ticker)
    except:
        ticker = None
    to_decode = ['fund_name', 'fund_trd_type', 'fund_manager',
                 'fund_ivst_type', 'fund_style', 'fund_benchmark',
                 'fund_actv_or_indx', 'fund_bchmrk_code']
    raw = BaseGet(table_id, ticker=ticker, field=field, bk=fund)
    df_to_decode = [x for x in raw.columns if x in to_decode]
    raw[df_to_decode] = raw[df_to_decode].apply(lambda x: x.str.decode('GBK'))
    raw = raw.reset_index('date', drop=True)
    return raw





