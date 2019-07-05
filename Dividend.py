# coding: utf-8
"""分红送股"""
import pandas as pd
from .BaseAPI import StatementGet


def EqyDivGet(ticker=None, secID=None, beginReportDate=None, endReportDate=None, baseDate=None,
              reportDate=None, beginPublishDate=None, endPublishDate=None, field='*'):
    """分红送股数据

    Parameters:
    ===========
    beginReportDate: str, 'yyyymmdd' like.
      起始截止日期，分红对应的财报日期
    endReportDate: str, 'yyyymmdd' like.
      终止截止日期，分红对应的财报日期
    baseDate: str, 'yyyymmdd' like.
      天软pn_date()参数

    Available Fields:
      预案公布日/股东大会日/决案公布日/实施公布日/
      股权登记日/除权除息日/红利比/实得比/送股比/红股比/转赠比/
      分红发放日/送股上市日/预案预披露公布日
    """
    table_id = 18
    if (beginPublishDate is not None) or (endPublishDate is not None):
        if isinstance(field, list) and ('预案公布日' not in field):
            field.append('预案公布日')
    data = StatementGet(table_id, '截止日', secID, ticker, beginReportDate, endReportDate, baseDate, reportDate, field)
    if beginPublishDate is not None:
        data = data[data['s_div_prelanndate'] >= int(beginPublishDate)]
    if endPublishDate is not None:
        data = data[data['s_div_prelanndate'] <= int(endPublishDate)]
    data.index = data.index.set_levels([pd.PeriodIndex(data.index.levels[0],
                                                       freq='D').to_timestamp()],
                                       level=['date'])
    return data


if __name__ == '__main__':
    data = EqyDivGet(ticker=['000001'], beginReportDate='20101231', endReportDate='20171231',
                     field=['红利比', '预案公布日'])
    print(data)
