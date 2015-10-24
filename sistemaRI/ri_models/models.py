from django.db import models

class Documento(models.Model):
    direccion_url = models.CharField(max_length=255)

class Termino(models.Model):
    termino = models.CharField(max_length=255)

class Posteo(models.Model):
    documento = models.ForeignKey(Documento)
    termino = models.ForeignKey(Termino)
    frequencia = models.IntegerField()

class Stopword(models.Model):
    stopword = models.CharField(max_length=255)



