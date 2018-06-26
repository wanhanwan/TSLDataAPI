# coding: utf-8
from .utils import read_tableinfo, read_indexnameid
from collections import OrderedDict


table_info = read_tableinfo()
index_name_id = read_indexnameid()


class TableInfo(object):
    def __init__(self):
        self.table_info = table_info
        self.index_nameid = index_name_id

    def get_factor_id_by_names(self, table_id, factor_names):
        table_info = self.table_info[self.table_info.TableID == table_id]
        return table_info.loc[factor_names, 'ID'].tolist()

    def get_table_columns(self, table_name):
        return self.table_info[self.table_info.TableID == table_name]['ID'].tolist()

    def get_factor_eng_names(self, factor_names):
        return self.table_info.loc[factor_names, 'Eng_Name'].tolist()

    def get_factor_eng_names_by_id(self, factor_ids):
        table_info = self.table_info.set_index('ID')
        return table_info.reindex(factor_ids)['Eng_Name'].tolist()

    def get_table_id_by_factor(self, factor_name):
        if factor_name.isalpha():
            return self.table_info[self.table_info.Eng_Name == factor_name].iat[0, 2]
        else:
            return self.table_info.at[factor_name, 'TableID']

    def get_eng_names_of_table(self, table_id):
        return self.table_info[self.table_info.TableID == table_id]['Eng_Name'].tolist()

    def get_note_by_id(self, factor_ids):
        table_info = self.table_info.set_index('ID')
        return table_info.reindex(factor_ids)['Note'].tolist()

    def get_factor_name_by_id(self, factor_ids):
        table_info = self.table_info.reset_index().set_index('ID')
        return table_info.reindex(factor_ids)['Name'].tolist()

    def get_params_by_id(self, factor_ids):
        table_info = self.table_info.set_index('ID')

        rslt = OrderedDict()
        for f_id in factor_ids:
            try:
                p = table_info.at[f_id, 'Params'].split(';')
            except:
                p = ''
            rslt[f_id] = p
        return rslt

    def get_index_id(self, index_names):
        a = self.index_nameid.set_index('Name')
        a = a[~a.index.duplicated(keep='last')]
        return a.reindex(index_names)['ID'].tolist()

    def get_index_id_by_tickers(self, tickers):
        a = self.index_nameid.copy()
        a.index = a['ID'].str[:6]
        return a.reindex(tickers)['ID'].tolist()

    def get_index_name(self, index_ids):
        a = self.index_nameid.set_index('ID')
        return a.reindex(index_ids)['Name'].tolist()


tsl_dict = TableInfo()
