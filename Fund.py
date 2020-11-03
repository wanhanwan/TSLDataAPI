# coding: utf-8

"""基金数据库"""
from FactorLib.utils.datetime_func import IntDate2Datetime

from .utils import get_tsl_fundid
from .BaseAPI import InfoArrayGet, QuotaGet, BaseGet, PanelQuery, UserTimeSeriesFuncGet


def FundEqyInfoGet(secID=None, ticker=None, beginReportDate=None, endReportDate=None, reportDate=None,
                   field='*', baseDate=None):
    """
    基金持仓明细
    
    基金股票持仓明细
    
    Return:DataFrame
        截至日、代码、占净值比、市值排名、数量(股)、市值(元)
        
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


def FundNavGet(secID=None, ticker=None, beginTradeDate=None, endTradeDate=None, tradeDate=None, field='*'):
    """
    基金净值

    Returns:
    --------
    DataFrame([unit_nav, cum_nav, nav_pctchg, date])
    """
    try:
        ticker = get_tsl_fundid(secID, ticker)
    except:
        ticker = None
    field_dict = {"'unit_nav'": "FundNAWDW()",
                  "'cum_nav'": "FundNAWLJ()",
                  "'nav_pctchg'": "FundNAWZf3()",
                  "'date'": "DateTimeToStr(sp_time())"
    }
    data = PanelQuery(field_dict, start_date=beginTradeDate, end_date=endTradeDate, dates=tradeDate,
                      stock_list=ticker, bk_name="''")
    if field != '*':
        return data[field]
    return data


def FundDailyPricesGet(secID=None, ticker=None, beginTradeDate=None, endTradeDate=None, tradeDate=None, field='*'):
    """
    场内基金日行情

    """
    if tradeDate:
        beginTradeDate = endTradeDate = tradeDate
    prices = UserTimeSeriesFuncGet('FundDailyPricesGet', secID, ticker, beginTradeDate, endTradeDate)
    prices['IDs'] = prices['IDs'].apply(lambda x: x.decode('GBK')[2:])
    prices['date'] = prices['date'].apply(IntDate2Datetime)
    prices = prices.set_index(['date', 'IDs']).sort_index()
    if field != '*':
        prices = prices[field]
    return prices


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





