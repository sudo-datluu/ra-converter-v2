from django.urls import path
from .views import UploadCSV, UpdateColumnType, DataFileList, ColumnInfoList, ColumnInfoList

urlpatterns = [
    path('upload/', UploadCSV.as_view(), name='upload-csv'),
    path('files/', DataFileList.as_view(), name='csv-file-list'),
    path('columns/<int:file_id>/', ColumnInfoList.as_view(), name='column-info-list'),
    path('update-column-type/<int:pk>/', UpdateColumnType.as_view(), name='update-column-type'),
]
