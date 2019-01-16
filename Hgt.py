# coding: utf-8
# author: wamhanwan

"""沪港通数据
沪港通数据目前支持北上资金持有A股的数量和持股比例，十大成交活跃股，每日成交统计等。
更新频率为每日更新
"""

from .BaseAPI import InfoArrayGet2


def HGT_Hold_Position_Get(secID=None, ticker=None, beginTradeDate=None, endTradeDate=None, tradeDate=None,
                          field='*', baseDate=None):
    """北上资金持有A股数量和占总股本比例(%)

    可选 field： 1. 股数(shares_hold)
                2. 占总股本比例(%)(ratio_hold)
    """
    func_name = 'HGT_Hold_Position_Get'
    table_id = 132

    raw = InfoArrayGet2(table_id, func_name, secID=secID, ticker=ticker, beginDate=beginTradeDate,
                        endDate=endTradeDate, tradeDate=tradeDate, field=field, baseDate=baseDate)
    if 'code' in raw.columns:
        raw['code'] = raw['code'].str.decode('GBK')
    return raw


def HGT_Ten_Active_Stocks_Get(secID=None, beginTradeDate=None, endTradeDate=None, tradeDate=None, field='*',
                              baseDate=None):
    """沪深港通每日十大成交活跃股

    secID 可选: 1. 000002.HG(沪股通) 2. 000004.HG(深股通)
    filed 可选  1. 买入金额(amt_buy)
                2. 卖出金额(amt_sell)
                3. 买入及卖出金额(amt_trade)
                4. 排名(rank)
                5. 股票名称(stock_name)
    """
    func_name = 'HGT_Ten_Active_Stocks_Get'
    table_id = 131

    if field != '*' and '股票代码' not in field:
        field.append('股票代码')
    raw = InfoArrayGet2(table_id, func_name, secID=secID, beginDate=beginTradeDate,
                        endDate=endTradeDate, tradeDate=tradeDate, field=field, baseDate=baseDate)
    if 'stock_id' in raw.columns:
        raw['stock_id'] = raw['stock_id'].str.decode('GBK')
        raw['stock_id'] = raw['stock_id'].str[2:]
    if 'stock_name' in raw.columns:
        raw['stock_name'] = raw['stock_name'].str.decode('GBK')
    raw = raw.reset_index('IDs', drop=True).set_index('stock_id', append=True).rename_axis(['date', 'IDs'])
    return raw


def HGT_Trade_Description_Get(secID=None, beginTradeDate=None, endTradeDate=None, tradeDate=None, field='*',
                              baseDate=None):
    """北上资金成交统计
    secID 可选: 1. 000002.HG(沪股通) 2. 000004.HG(深股通)
    filed 可选  1. 买入成交额(元)(amt_buy)
                2. 卖出成交额(元)(amt_sell)
                3. 买入及卖出成交额(元)(amt_trade)
                4. 买入成交数目
                5. 卖出成交数目
                6. 买入及卖出成交数目
    """
    func_name = 'HGT_Trade_Description_Get'
    table_id = 130

    raw = InfoArrayGet2(table_id, func_name, secID=secID, beginDate=beginTradeDate,
                        endDate=endTradeDate, tradeDate=tradeDate, field=field, baseDate=baseDate)

    return raw
