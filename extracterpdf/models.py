from django.db import models


class Destinos(models.Model):
    pdffile = models.FileField(upload_to="extracterpdf/static/pdfs_extraidos/")
