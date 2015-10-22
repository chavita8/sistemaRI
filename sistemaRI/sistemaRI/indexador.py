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
class Indexador:

    def importar_stopwords(self,ruta):
        archivo_stopwords = open(ruta)
        texto = archivo_stopwords.read()
        texto = unidecode(texto) #eliminiacion de acentos
        palabras = texto.split('\r\n')#obtenemos la lista de stopwords en un arreglo
        count = 0
        for palabra in palabras:
            if palabra != '':
                stopword = Stopword(stopword=palabra)
                stopword.save()
                count +=1
        print "Se insertaron %s stopwords en base de datos" %str(count)

    def indexar(self,inf,nombre_doc,doc_url):
        name_stop = unidecode(nombre_doc)
        name_stop = name_stop.lower()
        name_stop = name_stop.strip()
        name_stop = self.eliminarBasura(name_stop)
        stop_name = Stopword(stopword=name_stop)
        stop_name.save()
        stopwords = Stopword.objects.all()
        stop_set = set(s.stopword for s in stopwords)
        terminos = []
        data = unidecode(inf)
        data = data.lower()
        data = data.strip()
        data_list = data.split('\n')
        for data in data_list:
            sub = data.split(' ')
            for term in sub:
                t = self.eliminarBasura(term)
                if t not in stop_set:
                    terminos.append(t)
        print terminos
        doc = Documento(titulo=nombre_doc,direccion_url=doc_url)
        doc.save()
        for termino in terminos:
            if termino != '':
                term = Termino(termino=termino)
                term.save()
                posteos = Posteo.objects.all()
                posteo_repetido = []
                for posteo in posteos:
                    if posteo.documento.titulo == doc.titulo and posteo.termino.termino == term.termino:
                        print 'repetido'
                        print posteo
                        posteo_repetido.append(posteo)
                        
                if len(posteo_repetido) > 0 :
                    print posteo_repetido
                    print "actualizar"
                    posteo = posteo_repetido[0]
                    posteo.frequencia += 1
                    posteo.save()
                else:
                    new_posteo = Posteo(documento=doc,termino=term,frequencia=1)
                    new_posteo.save()

                


                """
                if posteo:
                    freq = posteo.frequencia
                    new_freq = freq + 1
                    posteo.frequencia = new_freq
                else:
                    new_posteo = Posteo(documento=doc,termino=term,frequencia=1)
                    new_posteo.save()
                """

    def eliminarBasura(self,term):
        clean_word = []
        for c in term:
            clean_word.append(c)
            ascii_number = ord(c)
            if ascii_number < 97 or ascii_number > 122:
                clean_word.remove(c)
        return ''.join(clean_word)




"""
indexador = Indexador()
indexador.importar_stopwords('/home/archy/Downloads/diccionario_negativo.txt')
"""

