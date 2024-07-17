import numpy as np
import pandas as pd
from typing import Tuple
from .inferer import Inferer

class TypeInferer:
    def __init__(self, threshold:float = 0.8):
        self.threshold = threshold
    
    '''
    Clean data method
    '''
    def clean(self, data: pd.Series) -> pd.Series:
        null_val = ["", "none", "null", "n/a", "nan"]
        cleaned_data = data.replace(null_val, np.nan)
        cleaned_data = cleaned_data.apply(lambda x: x.strip().lower() if isinstance(x, str) else x)
        return cleaned_data
    

    def infer(self, data: pd.Series) -> Tuple[float, pd.Series]:
        cleaned_data = self.clean(data=data)
        inferer = Inferer(cleaned_data)

        bool_rate, bool_df = inferer.bool_infer()
        cat_rate, cat_df = inferer.categorical_infer()
        complex_rate, complex_df = inferer.complex_infer()
        time_delta_rate, time_delta_df = inferer.time_delta_infer()
        numeric_rate, numeric_df = inferer.numeric_infer()
        date_time_rate, date_time_df = inferer.date_time_infer()

        if bool_rate > self.threshold: return bool_rate, bool_df
        if cat_rate > self.threshold: return cat_rate, cat_df
        if numeric_rate > self.threshold: return numeric_rate, numeric_df
        if date_time_rate > self.threshold: return date_time_rate, date_time_df
        if time_delta_rate > self.threshold: return time_delta_rate, time_delta_df
        if complex_rate > self.threshold: return complex_rate, complex_df

        # If no confident rate is above the threshold
        # The data will be defined as string
        return 1, cleaned_data