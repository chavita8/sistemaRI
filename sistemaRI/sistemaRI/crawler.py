#! /usr/bin/python2.7
from bs4 import BeautifulSoup
from indexador import Indexador
import urllib2

class Crawler:
    def __init__(self):
        self.count = 0
        self.indexador = Indexador()

    def mostrarConfig(self):
        print "Direccion url: "
        print self.url
        print "Profundidad: "
        print self.profundidad

    def recuperarInf(self,url,prof):
        html = self.obtenerHtml(url)
        soup = BeautifulSoup(html,'html.parser')
        nombre_doc = soup.title.string
        print nombre_doc

        if prof == 0:
            data = soup.get_text()
            self.indexador.indexar(data,nombre_doc,url)
            self.count += 1

        if prof > 0:
            data = soup.get_text() 
            self.indexador.indexar(data,nombre_doc,url)
            self.count += 1
            paginas = self.obtenerPag(soup)
            for pagina in paginas:
                niv = prof
                self.recuperarInf(pagina,niv-1)

    def obtenerPag(self,soup):
        res = []
        for url in soup.find_all('a'):
            res.append(url.get('href'))
        return res


    def obtenerHtml(self,url):
        html = str(urllib2.urlopen(url).read()) 
        return html






