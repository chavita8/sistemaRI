#! /usr/bin/python2.7
import os
from bs4 import BeautifulSoup
import random
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Text2Html():
    def convert2Html(self,ruta,nombre):
        self.host = "http://192.168.43.220/"
        soup = BeautifulSoup()
        html = soup.new_tag('html')
        head = soup.new_tag('head')
        title = soup.new_tag('title')
        body = soup.new_tag('body')
        pre = soup.new_tag('pre')
        title.string = ruta
        head.insert(0,title)
        html.insert(0,head)
        archivo = open(ruta)
        buffer_txt = archivo.read()
        pre.string = str(buffer_txt.decode('utf-8'))
        body.insert(0,pre)
        a1 = soup.new_tag('a')
        link_name = 'pagina%s.html'% random.randint(1,62)
        link_name = self.host+link_name
        a1.attrs["href"] = link_name
        a1.string = link_name
        body.insert(1,a1)

        a2 = soup.new_tag('a')
        link_name = 'pagina%s.html'% random.randint(1,62)

        link_name = self.host+link_name
        a2.attrs["href"] = link_name
        a2.string = link_name
        body.insert(2,a2)

        a3 = soup.new_tag('a')
        link_name = 'pagina%s.html'% random.randint(1,62)
        link_name = self.host+link_name
        a3.attrs["href"] = link_name
        a3.string = link_name
        body.insert(3,a3)

        a4 = soup.new_tag('a')
        link_name = 'pagina%s.html'% random.randint(1,62)
        link_name = self.host+link_name
        a4.attrs["href"] = link_name
        a4.string = link_name
        body.insert(4,a4)

        html.insert(1,body)
        insert = html.prettify()#nuevo html generado con la informacion de un archivo de texto dad
        archivo.close()
        print nombre
        new_html = open(nombre,'w')
        new_html.write(insert)
        new_html.close()

        


object1 = Text2Html()
path ='/home/archy/recuperacion_informacion/Retrieval/documentos/'
files = os.listdir(path)
i = 0
for txt in files:
    if not os.path.isdir(path+txt):
        i = i+1
        name = 'pagina%s.html' % str(i)
        #nombre = '/home/archy/sistemaRI/documentos/'+name
        nombre = '/srv/http/'+name
        print("Convirtiendo documento %s" % txt)
        object1.convert2Html(path+txt,nombre)

print "proceso terminado be happy :D TE AMO BEBE :* TE AMO TE DEDICO ESTA PIEZA DE SOFTWARE :* XDXD"



