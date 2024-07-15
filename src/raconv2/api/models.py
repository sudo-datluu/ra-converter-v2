from django.db import models

# Create your models here.
class DataFile(models.Model):
    name = models.CharField(max_length=255)
    minio_url = models.CharField(max_length=1024)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ColumnInfo(models.Model):
    file = models.ForeignKey(DataFile, on_delete=models.CASCADE)
    column_name = models.CharField(max_length=255)
    column_type = models.CharField(max_length=255)