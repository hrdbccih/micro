from django.db import models
import os
from website.settings import BASE_DIR


#def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    #return 'user_{0}/{1}/{2}/{3}'.format(instance.user.id, filename)

path = os.path.join("micro", "static", "extracterpdf" ,"pdfs_extraidos")

class Destinos(models.Model):
    pdffile = models.FileField(upload_to=path)


