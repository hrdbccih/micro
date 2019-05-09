from django.db import models
import os
from website.settings import BASE_DIR


class Destinos(models.Model):
    pdffile = models.FileField(upload_to=os.path.join(BASE_DIR, "static", "extracterpdf" ,"pdfs_extraidos"))
