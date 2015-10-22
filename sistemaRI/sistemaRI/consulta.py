# settings.py
from django.conf import settings
from unidecode import unidecode

settings.configure(

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sistemaRI',
        'USER': 'sistemaRI',
        'PASSWORD': 'teamo_bb',
        'HOST': 'localhost',
        'PORT': '5432',
    }
},
INSTALLED_APPS     = ("ri_models",)
)

from django.db import models
from ri_models.models import *
import django
django.setup()

class Consulta:
    def __init__(self):
        self.nro_docs = len(Documento.objects.all())
        print "nro de documentos"
        print self.nro_docs

    def busqueda_vectorial(self,q):
        stopwords = Stopword.objects.all()
        stop_set = set(s.stopword for s in stopwords)
        consulta = unidecode(q)
        consulta = consulta.lower()
        consulta = consulta.strip()
        terminos = []
        palabras = consulta.split(' ')
        for pal in palabras:
            p = self.eliminarBasura(pal)
            if p not in stop_set:
                terminos.append(p)
        self.gen_matriz(terminos)

    def gen_matriz(self,terminos_q):
        documentos = Documento.objects.all()
        posteos = Posteo.objects.all()
        terminos = Termino.objects.all()
        conjunto_terminos = set(term.termino for term in terminos)
        numero_columnas = len(conjunto_terminos)

        matriz = []
        for i in range(self.nro_docs):
            matriz.append([])
            for j in range(numero_columnas):
                matriz[i].append(0)

        z = 0
        for i,documento in enumerate(documentos):
            posteo_documento = posteos.filter(documento=documento)
            term_list = []
            dic_posteo = {}
            for posteo in posteo_documento:
                dic_posteo['termino'] = posteo.termino.termino
                dic_posteo['freq'] = posteo.frequencia
                term_list.append(dic_posteo)

            print term_list 
            print sorted(term_list, key=lambda dic: dic['termino'])


            for j in range(numero_columnas):
                    if z < len(term_list):
                        print term_list[z]
                        matriz[i][j] = 0
                        z += 1
            z = 0

        print matriz

    def eliminarBasura(self,term):
        clean_word = []
        for c in term:
            clean_word.append(c)
            ascii_number = ord(c)
            if ascii_number < 97 or ascii_number > 122:
                clean_word.remove(c)
        return ''.join(clean_word)



consulta = Consulta()
consulta.busqueda_vectorial("-Cual es el caudal, del rio daNubio")



