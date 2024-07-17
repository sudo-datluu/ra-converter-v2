from ..typeinfer import TypeInfer
from .models import DataFile, ColumnInfo
from minio import Minio
from django.conf import settings

import pandas as pd

class RaConvProcess:
    def __init__(self, file, minioClient: Minio, prev_file: DataFile=None):
        self.file = file
        self.minioClient = minioClient
        self.csv_content = pd.read_csv(file)
        self.prev_file = prev_file

    # To do:
    # - user do not need to specify identity of the file
    # - user change the dataframe header
    # - user change the csv/xlsx data extension
    def load_file(self, data_file: DataFile):
        response = self.minioClient.get_object(
            settings.MINIO_BUCKET_NAME,
            data_file.name
        )
        file_content = response.read()
        return pd.read_csv(file_content)

    # compare at the column level
    def getDiff(self, curr_df: pd.Series, prev_df: pd.Series):
        if prev_df:
            diff = curr_df != prev_df
            diff_values = curr_df[diff]
            return diff_values
        return curr_df

    def infer(self, data: pd.Series):
        inferer = TypeInfer()
        conf_rate, inferer_df = inferer.infer(data)
        return conf_rate, inferer_df

    def save(self):
        pass
        
    def exec(self):
        pass