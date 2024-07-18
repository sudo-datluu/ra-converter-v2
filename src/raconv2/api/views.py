from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from .models import DataFile, ColumnInfo
from .serializers import DataFileSerializer, ColumnInfoSerializer

from minio import Minio
import pandas as pd
from django.conf import settings

minioClient = Minio(
    settings.MINIO_STORAGE_ENDPOINT,
    access_key=settings.MINIO_STORAGE_ACCESS_KEY,
    secret_key=settings.MINIO_STORAGE_SECRET_KEY,
    secure=settings.MINIO_STORAGE_USE_HTTPS
)

class UploadCSV(APIView):
    def post(self, request):
        file = request.FILES['file']
        file_name = file.name
        minioClient.put_object('DataFiles', file_name, file, len(file.read()), 'application/csv')
        file_url = minioClient.presigned_get_object('DataFiles', file_name)
        csv_file = DataFile.objects.create(name=file_name, minio_url=file_url)
        
        # Process CSV to determine columns
        # to do: 
        # install redis, celery to handle the file
        # mark the file is draft
        df = pd.read_csv(file)
        for column in df.columns:
            ColumnInfo.objects.create(file=csv_file, column_name=column, column_type=df[column].dtype)
        
        return Response(DataFileSerializer(csv_file).data, status=status.HTTP_201_CREATED)

class DataFileList(generics.ListAPIView):
    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer

class ColumnInfoList(generics.ListAPIView):
    serializer_class = ColumnInfoSerializer

    def get_queryset(self):
        file_id = self.kwargs['file_id']
        return ColumnInfo.objects.filter(file_id=file_id)

class UpdateColumnType(APIView):
    def post(self, request, pk):
        try:
            column_info = ColumnInfo.objects.get(pk=pk)
            column_info.column_type = request.data['column_type']
            column_info.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except ColumnInfo.DoesNotExist:
            return Response({'error': 'Column not found'}, status=status.HTTP_404_NOT_FOUND)