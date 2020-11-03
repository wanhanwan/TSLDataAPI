# coding: utf-8
"""行情数据"""
from .BaseAPI import QuotaGet


def AShareEodDailyPricesGet(secID=None, ticker=None, beginTradeDate=None, endTradeDate=None,
                            tradeDate=None, field='*', brate=0):
    """
    股票日行情数据 \n
    对应字段包括：开高低收 成交量成交额 涨跌幅 前收盘价

    Parameters:
    ----------------------------------------------
    brate: int
        是否复权, 0：不复权；1：比例复权；2：复杂复权
    """
    if brate != 0:
        params = {'RateDay': -1}
    else:
        params = None
    return QuotaGet(0, secID, ticker, beginTradeDate, endTradeDate, tradeDate, field, rate=brate, sysparams=params)


def AShareMinutelyPricesGet(secID=None, ticker=None, beginTradeDate=None, endTradeDate=None,
                            tradeDate=None, field='*', brate=0, minutes=1):
    """
    股票分钟行情数据 \n
    对应字段包括：开高低收 成交量成交额 涨跌幅 前收盘价

    Parameters:
    ----------------------------------------------
    brate: int
        是否复权
    """
    cycle = 'cy_%dm' % minutes
    return QuotaGet(0, secID, ticker, beginTradeDate, endTradeDate, tradeDate, field, cycle=cycle,
                    rate=brate)


def AShareSecondlyPricesGet(secID=None, ticker=None, beginTradeDate=None, endTradeDate=None,
                          tradeDate=None, field='*', brate=0, seconds=1):
    """
    股票秒行情数据 \n
    对应字段包括：开高低收 成交量成交额 涨跌幅 前收盘价

    Parameters:
    ----------------------------------------------
    brate: int
        是否复权
    """
    cycle = 'cy_%dm' % seconds
    return QuotaGet(0, secID, ticker, beginTradeDate, endTradeDate, tradeDate, field, cycle=cycle,
                    rate=brate)


def AShareWeeklyPricesGet(secID=None, ticker=None, beginTradeDate=None, endTradeDate=None,
                          tradeDate=None, field='*', brate=0):
    """
    股票周行情数据 \n
    对应字段包括：开高低收 成交量成交额 涨跌幅 前收盘价

    Parameters:
    ----------------------------------------------
    brate: int
        是否复权
    """
    cycle = 'cy_week'
    return QuotaGet(0, secID, ticker, beginTradeDate, endTradeDate, tradeDate, field, cycle=cycle,
                    rate=brate)


def AShareMonthlyPricesGet(secID=None, ticker=None, beginTradeDate=None, endTradeDate=None,
                           tradeDate=None, field='*', brate=0):
    """
    股票周行情数据 \n
    对应字段包括：开高低收 成交量成交额 涨跌幅 前收盘价

    Parameters:
    ----------------------------------------------
    brate: int
        是否复权
    """
    cycle = 'cy_month'
    return QuotaGet(0, secID, ticker, beginTradeDate, endTradeDate, tradeDate, field, cycle=cycle,
                    rate=brate)


def AshareEodDerivativeGet(secID=None, ticker=None, beginTradeDate=None, endTradeDate=None,
                           tradeDate=None, field='*', **kwargs):
    """股票估值衍生指标。包括：市盈率、市净率等
    """
    table_id = 0
    return QuotaGet(table_id, secID, ticker, beginTradeDate, endTradeDate, tradeDate,
                    field, **kwargs)