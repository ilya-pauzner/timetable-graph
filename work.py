from matplotlib import *
from pylab import *

from html.parser import *
from urllib.request import *
from string import *
from datetime import *
from time import *

import json
# import os

already_know = {}

def load():
    global already_know
    try:
        f = open('data', 'r')
        already_know = json.loads(f.read())
        f.close()
    except:
        pass
    # print(already_know)
    
def dump():
    f = open('data', 'w')
    f.write(json.dumps(already_know))
    f.close()

rail  = {'Дмитровская': 4.4, 'Гражданская': 5.9, 'КрасныйБалтиец': 8.2, 'Ленинградская': 9.9, 'Покровское-Стрешнево': 11.2, 'Тушино': 14.9, 'Трикотажная': 17.8, 'Павшино': 22.3, 'Красногорская': 24.8, 'Опалиха': 29.3}

class BaseParser(HTMLParser):        
    def handle_starttag(self, tag, attrs):
        self.tagstack.append(tag)
        self.attrstack.append(attrs)

    def handle_endtag(self, tag):
        self.tagstack.pop()
        self.attrstack.pop()

    def handle_data(self, data):
        if 'tr' in self.tagstack:
            if ('class', 'select') in self.attrstack[self.tagstack.index('tr')]:
                d1 = ''
                for elem in data:
                    if elem not in whitespace:
                        d1 += elem
                if len(d1) > 2 or d1 == '-':
                    self.s.append(d1)
                    
def parse_train(url):
    if url in already_know:
        # print('here')
        return already_know[url]
    parser = BaseParser()
    parser.tagstack = []
    parser.attrstack = []
    parser.s = []
    sleep(2)
    parser.feed(urlopen(url).read().decode('utf-8'))
    ans = list()
    for elem in parser.s:
        if elem[0] in digits:
            #print(elem)
            try:
                dt = datetime.strptime(elem, '%H:%M')
                ans[-1].append(dt.hour * 60 + dt.minute)
            except:
                ans.pop()
        elif elem[0] == '-':
            ans.pop()
        else:
            ans.append([elem])
    answer1 = list()
    answer2 = list()
    for elem in ans:
        if elem[0] in rail:
            answer2.append(rail[elem[0]])
            answer1.append(elem[1])
    parser.close()
    # print((answer1, answer2))
    if (answer1, answer2) != ([], []):
        already_know[url] = (answer1, answer2)
    return (answer1, answer2)

def plot_train(url):
    (x, y) = parse_train(url)
    plot(x, y, ':H')    
    
class MetaParser(HTMLParser):        
    def handle_starttag(self, tag, attrs):
        self.tagstack.append(tag)
        self.attrstack.append(attrs)

    def handle_endtag(self, tag):
        self.tagstack.pop()
        self.attrstack.pop()

    def handle_data(self, data):
        if '→' in data:
            self.s.append(['https://tutu.ru' + self.attrstack[-1][0][1]])

load()

mp = MetaParser()
mp.tagstack = []
mp.attrstack = []
mp.s = []
mp.feed(urlopen('https://www.tutu.ru/station.php?nnst=35805&list=d5').read().decode('utf-8'))
mp.s.pop()
i = 0
j = 0

#sleep(10)
for elem in mp.s:
    try:
        plot_train(elem[0])
    except:
        j += 1
    i += 1
    if i % 10 == 0:
        print(i // 10)

print(j, 'exceptions')
dump()
show()
