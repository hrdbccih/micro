from django.db import models
from django.urls import reverse


class Cultura(models.Model):
    filename = models.CharField(max_length=250)
    nome = models.CharField(max_length=250, blank=True, null=True)
    prot = models.CharField(max_length=250, blank=True, null=True)
    medico = models.CharField(max_length=250, blank=True, null=True)
    data = models.DateTimeField(blank=True, null=True)
    unid = models.CharField(max_length=250, blank=True, null=True)
    coleta = models.DateTimeField(blank=True, null=True)
    material = models.CharField(max_length=250, blank=True, null=True)
    mat_especifico = models.CharField(max_length=250, blank=True, null=True)
    resultado = models.CharField(max_length=250, blank=True, null=True)
    tipo = models.CharField(max_length=250, blank=True, null=True)
    testes = models.CharField(max_length=250, blank=True, null=True)
    falha = models.CharField(max_length=250, blank=True, null=True)
    ami = models.CharField(max_length=250, blank=True, null=True)
    amp = models.CharField(max_length=250, blank=True, null=True)
    asb = models.CharField(max_length=250, blank=True, null=True)
    atm = models.CharField(max_length=250, blank=True, null=True)
    caz = models.CharField(max_length=250, blank=True, null=True)
    cip = models.CharField(max_length=250, blank=True, null=True)
    cli = models.CharField(max_length=250, blank=True, null=True)
    cpm = models.CharField(max_length=250, blank=True, null=True)
    cro = models.CharField(max_length=250, blank=True, null=True)
    ctn = models.CharField(max_length=250, blank=True, null=True)
    eri = models.CharField(max_length=250, blank=True, null=True)
    ert = models.CharField(max_length=250, blank=True, null=True)
    gen = models.CharField(max_length=250, blank=True, null=True)
    imi = models.CharField(max_length=250, blank=True, null=True)
    lin = models.CharField(max_length=250, blank=True, null=True)
    mer = models.CharField(max_length=250, blank=True, null=True)
    nit = models.CharField(max_length=250, blank=True, null=True)
    nor = models.CharField(max_length=250, blank=True, null=True)
    oxa = models.CharField(max_length=250, blank=True, null=True)
    pen = models.CharField(max_length=250, blank=True, null=True)
    pol = models.CharField(max_length=250, blank=True, null=True)
    ppt = models.CharField(max_length=250, blank=True, null=True)
    str = models.CharField(max_length=250, blank=True, null=True)
    sut = models.CharField(max_length=250, blank=True, null=True)
    tei = models.CharField(max_length=250, blank=True, null=True)
    tet = models.CharField(max_length=250, blank=True, null=True)
    van = models.CharField(max_length=250, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('biao:detail', kwargs={'pk': self.pk})
