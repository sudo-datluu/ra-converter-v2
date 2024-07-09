import numpy as np
import pandas as pd

class Inferer:
    def __init__(self, data: pd.Series):
        self.data = data
        self.na_count = data.isna().sum()

    def bool_infer(self):
        TRUE_STR = ['true', 't', 'yes', 'y', '1']
        FALSE_STR = ['false', 'f', 'no', 'n', '0']
        
        def convert(x):
            if str(x) in TRUE_STR: return True
            if str(x) in FALSE_STR: return False
            return np.nan

        df_convert = self.data.apply(convert)

        afterconvert_na = df_convert.isna().sum() - self.na_count
        total_rows_afterconvert = len(df_convert) - self.na_count
        
        return 1 - (afterconvert_na / total_rows_afterconvert), df_convert

    def categorical_infer(self):
        unique_count = self.data.nunique()
        if self.data.dtype != 'object': return 0 # Not a categorical column
        if unique_count / len(self.data) > 0.8: return 0 # Too many unique values

        df_convert = pd.Categorical(self.data)

        return 1 - unique_count / len(self.data), df_convert
    
    def complex_infer(self):
        pass

    def time_delta_infer(self):
        pass

    def numeric_infer(self):
        pass

    def text_infer(self):
        pass

    def date_time_infer(self):
        pass