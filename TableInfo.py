# coding: utf-8
from .utils import read_tableinfo


table_info = read_tableinfo()


class TableInfo(object):
    def __init__(self):
        self.table_info = table_info

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


tsl_dict = TableInfo()
