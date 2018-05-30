# -*- coding: utf-8 -*-

import lxml
import lxml.html
from lxml import etree
import xml.etree.ElementTree as ET


from urllib import urlopen
import sys

def check():
    url = 'http://www.eurometeo.ru/russia/ryazanskaya-oblast/ryazan/archive/201605/'
    data = urlopen(url).read(); #TopGear as a test
    return data.decode('utf-8', 'ignore');


doc = lxml.html.document_fromstring(check())
for row in doc.xpath("//table[@class='met8']/tr"):
    th = row.xpath("th")
    if len(th) > 2:
        d1 = th[1].text
        d2 = th[2].text
    if len(row.xpath("td[@alt='Осадки (мм)']".decode('utf-8', 'ignore'))) > 0:
        n = 0
        r = 0.0
        for cell in row.xpath("td[@class!='fs']/em"):
            if cell.
            if (cell.text is not None) and (cell.text != u' '):
                print cell.text
                r += float(cell.text)
            n += 1
            if n == 8:
                print d1, ' : ', r
                r = 0
        print d2, ' : ', r
