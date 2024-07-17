import numpy as np
import pandas as pd
import re
from datetime import datetime

class Inferer:
    def __init__(self, data: pd.Series, cat_threshold=None):
        self.data = data
        self.cat_threshold = cat_threshold if cat_threshold else self.init_cat_threshold()
        self.na_count = data.isna().sum()

    # decide the threshold for categorical data
    # depend on the length of the data series 
    def init_cat_threshold(self):
        if len(self.data) <= 10: return 0.5
        if len(self.data) <= 100: return 0.7
        return 0.8
    
    def get_confident_rate(self, df_convert):
        # exclude the rows that were already nan
        afterconvert_na = df_convert.isna().sum() - self.na_count
        total_rows_afterconvert = len(df_convert) - self.na_count
        return 1 - (afterconvert_na / total_rows_afterconvert)

    def bool_infer(self):
        # List of possible true and false values
        TRUE_STR = ['true', 't', 'yes', 'y', '1']
        FALSE_STR = ['false', 'f', 'no', 'n', '0']
        
        def convert(x):
            if str(x) in TRUE_STR: return True
            if str(x) in FALSE_STR: return False
            return np.nan

        df_convert = self.data.apply(convert)
        
        return self.get_confident_rate(df_convert), df_convert

    def categorical_infer(self):
        unique_count = self.data.nunique()
        if self.data.dtype != 'object': return 0, self.data # Not a categorical column
        if unique_count / len(self.data) > self.cat_threshold: return 0, self.data # Too many unique values

        df_convert = pd.Categorical(self.data)
        conf_rate = 1 - unique_count / (len(self.data) - self.na_count)

        return conf_rate, df_convert
    
    def complex_infer(self):
        def convert(x):
            # Replace 'i' with 'j' for complex number conversion
            if isinstance(x, str): x = x.replace("i", "j")
            try:
                return complex(x)
            except:
                return np.nan
        df_convert = self.data.apply(convert)
    
        return self.get_confident_rate(df_convert), df_convert

    def time_delta_infer(self):
        def convert(x):
            try:
                # Handle common timedelta string formats
                return pd.to_timedelta(x)
            except ValueError:
                try:
                    # Handle ISO 8601 duration format and other potential formats
                    return pd.Timedelta(x)
                except ValueError:
                    # Custom handling for weeks, months, years, quarters
                    try:
                        match = re.match(r'(\d+)\s*(weeks|months|years|quarters)', x, re.IGNORECASE)
                        if match:
                            value, unit = match.groups()
                            value = int(value)
                            if unit.lower() == 'weeks':
                                return pd.to_timedelta(f'{value * 7} days')
                            elif unit.lower() == 'months':
                                return pd.to_timedelta(f'{value * 30} days')
                            elif unit.lower() == 'years':
                                return pd.to_timedelta(f'{value * 365} days')
                            elif unit.lower() == 'quarters':
                                return pd.to_timedelta(f'{value * 3 * 30} days')
                        return np.nan
                    except Exception:
                        return np.nan
        df_convert = self.data.apply(convert)
        return self.get_confident_rate(df_convert), df_convert

    def numeric_infer(self):
        # clean up data set:
        df_convert = self.data.apply(lambda x: str(x).replace(",", ""))

        # Try converting to float and integer
        df_convert = pd.to_numeric(df_convert, errors='coerce', downcast='float')
        df_convert = pd.to_numeric(df_convert, errors='coerce', downcast='integer')
        return self.get_confident_rate(df_convert), df_convert

    def date_time_infer(self):
        date_formats = ["%d/%m/%Y", "%m/%d/%Y", "%B %d, %Y", "%d-%b-%y", "%Y.%m.%d", "%Y%m%d", "%d-%b-%Y"]
        def convert(x):
            for fmt in date_formats:
                try:
                    return datetime.strptime(x, fmt)
                except Exception:
                    continue
            try:
                return parser.parse(x)
            except Exception:
                return np.nan
        df_convert = self.data.apply(convert)
        df_convert = df_convert.dt.strftime("%Y-%m-%d") #consistent format (e.g., YYYY-MM-DD)
        return self.get_confident_rate(df_convert), df_convert