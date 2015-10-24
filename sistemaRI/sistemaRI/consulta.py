# settings.py
from django.conf import settings
from unidecode import unidecode
from math import log10

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
        stopwords = Stopword.objects.all() # recuperamos todos los obj stopwords de la bd
        stop_set = set(s.stopword for s in stopwords) #ponemos todos los terminos de los stopwords en un conjunto
        consulta = unidecode(q) #quitamos acentos y caracteres extranios de la consulta
        consulta = consulta.lower() #convertimos a minuscula todas las palabras de la consulta
        consulta = consulta.strip() #eliminamos espacios de los extremos
        terminos = []   #vector terminos
        palabras = consulta.split(' ') # obtenemos lista palabras, cortando las palabras de la consulta que estan separadas por espacio 
        for pal in palabras: 
            p = self.eliminarBasura(pal) #eliminamos caracteres basura en la palabra
            if p not in stop_set:        
                terminos.append(p)       # solo insertamos en el vector termino las palabras que no sean stopwords
        matriz = self.gen_matriz(terminos)   #generamos la matriz pasando como parametro los terminos de la consulta
        numero_terminos = len(self.lista_terminos)  #numero de terminos
        print self.lista_terminos
        print matriz
        pesos_terminos = []
        values = []
        #Calculo de pesos
        for c in range(numero_terminos):
            peso=0.0
            for f in range(self.nro_docs):
                if matriz[f][c] > 0:
                    peso+=1
            values.append(peso)
            log_inv = log10(self.nro_docs/peso)
            pesos_terminos.append(log_inv)
        print values
        print pesos_terminos
        for c in range(numero_terminos):
            for f in range(self.nro_docs+1):
                if matriz[f][c] > 0:
                    matriz[f][c] = pesos_terminos[c]
        print matriz
        pesos = []
        for f in range(self.nro_docs):
            multi = []
            vec_doc = matriz[f]
            pos_q = len(matriz)-1
            vec_q = matriz[pos_q]
            for e in range(numero_terminos):
                multi.append(vec_doc[e]*vec_q[e])

            sumatoria = 0;
            for m in multi:
                sumatoria += m
            pesos.append(sumatoria)
        for i,peso in enumerate(pesos):
            documentos = Documento.objects.all()
            print documentos[i].direccion_url
            print peso
            

    def gen_matriz(self,terminos_q):
        documentos = Documento.objects.all()
        posteos = Posteo.objects.all()
        terminos = Termino.objects.all()
        conjunto_terminos = set(term.termino for term in terminos)
        self.lista_terminos = []
        for t in conjunto_terminos:
            self.lista_terminos.append(t)
        numero_terminos = len(self.lista_terminos)
        matriz = []

        for doc in documentos:
            posteo_doc = posteos.filter(documento=doc)
            vector_termino = []
            for i in range(numero_terminos):
                vector_termino.append(0)
            for posteo in posteo_doc:
                pos = self.lista_terminos.index(posteo.termino.termino)
                vector_termino[pos] = posteo.frequencia

            matriz.append(vector_termino)

        vector_consulta = []
        for i in range(numero_terminos):
            vector_consulta.append(0)

        for t in terminos_q:
            pos = self.lista_terminos.index(t)
            vector_consulta[pos] = 1
        matriz.append(vector_consulta)
        return matriz

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



