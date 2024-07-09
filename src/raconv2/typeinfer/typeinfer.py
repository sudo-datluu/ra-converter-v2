import numpy as np
import pandas as pd

class TypeInferer:
    def __init__(self, data: pd.Series, threshold:float = 0.8):
        self.data = data
        self.threshold = threshold
    
    '''
    Clean data method
    '''
    def clean(self) -> pd.DataFrame:
        null_val = ["", "none", "null", "n/a", "nan"]
        cleaned_data = self.data.replace(null_val, np.nan)
        cleaned_data = cleaned_data.apply(lambda x: x.strip().lower() if isinstance(x, str) else x)
        return cleaned_data
    
    def get_type(self) -> np.dtype:
        pass