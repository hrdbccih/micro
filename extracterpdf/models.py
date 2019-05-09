from django.db import models
import os
from website.settings import BASE_DIR

pre_path_pdfs = os.path.join(BASE_DIR, "static", "extracterpdf")
path_pdfs = os.path.join(pre_path_pdfs, "pdfs_extraidos")

class Destinos(models.Model):
    pdffile = models.FileField(upload_to=path_pdfs)
