from ..typeinfer import TypeInfer
from .models import DataFile, ColumnInfo
from minio import Minio
from django.conf import settings
from typing import Tuple

import pandas as pd

class RaConvProcess:
    def __init__(self, file, minioClient: Minio) -> None:
        self.minioClient = minioClient
    
    def load_file(self, data_file: DataFile) -> pd.DataFrame:
        response = self.minioClient.get_object(
            settings.MINIO_BUCKET_NAME,
            data_file.name
        )
        file_content = response.read()
        return pd.read_csv(file_content)

    def getDiff(self, curr_df: pd.DataFrame, prev_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        if prev_df.empty: return curr_df, pd.DataFrame(), pd.DataFrame()

        # Identify columns that are in both dataframes
        common_columns = curr_df.columns.intersection(prev_df.columns)
        
        # Identify added and deleted columns
        added_columns = curr_df.columns.difference(prev_df.columns)
        deleted_columns = prev_df.columns.difference(curr_df.columns)
        
        # Find differences in common columns
        diff_df = pd.DataFrame()
        for col in common_columns:
            diff = curr_df[col] != prev_df[col]
            if diff.any():
                diff_df = pd.concat([diff_df, curr_df.loc[diff, [col]]], axis=1)
        
        # Prepare added and deleted dataframes
        added_df = curr_df[added_columns]
        deleted_df = prev_df[deleted_columns]
        
        return diff_df, added_df, deleted_df 

    def infer(self, data: pd.Series):
        inferer = TypeInfer()
        conf_rate, inferer_df = inferer.infer(data)
        del inferer
        gc.collect()
        return conf_rate, inferer_df

    # Save series to MinIO
    # 3 mode: add, modify, delete
    def save(self, mode: str, datafile: DataFile, col: pd.DataSeries):
        if mode not in ['add', 'modify', 'delete']:
            raise ValueError('Invalid mode')
        
        if mode == 'add':
            column_info = ColumnInfo(
                file=datafile, 
                column_name=col.name, 
                column_type=str(col.dtype)
            )
            column_info.save()
        
        # Modify or delete column info
        column_info = ColumnInfo.objects.get(file=datafile, column_name=col.name)
        if mode == 'modify':
            column_info.column_type = str(col.dtype)
            column_info.save()
        if mode == 'delete': column_info.delete()
        
    def exec(self, data_file: DataFile, prev_file: DataFile = None):
        curr_df = self.load_file(data_file)
        data_file.save()
        prev_df = pd.DataFrame() 
        if prev_file:
            columns = ColumnInfo.objects.filter(file=prev_file)
            for col in columns:
                col.file = data_file
                col.save()
            prev_df = self.load_file(prev_file)
        
        # Get the difference between the current and previous data
        diff_df, added_df, deleted_df = self.getDiff(curr_df, prev_df)

        # Process the data
        exec_entities = [(diff_df, 'modify'), (added_df, 'add'), (deleted_df, 'delete')]
        for data, mode in exec_entities:
            # Save the data to MinIO
            for col in data.columns:
                conf_rate, inferer_df = self.infer(data[col])
                self.save(mode, data_file, data[col])

        # Get rid of the prev_file
        if prev_file: prev_file.delete()