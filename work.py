from matplotlib import *
from pylab import *

from html.parser import *
from urllib import *
from string import *
from datetime import *
from time import *
# import os

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
    parser = BaseParser()
    parser.tagstack = []
    parser.attrstack = []
    parser.s = []
    sleep(1)
    parser.feed(urlopen(url).read().decode('utf-8'))
    ans = list()
    for elem in parser.s:
        if elem[0] in digits:
            dt = datetime.strptime(elem, '%I:%M')
            ans[-1].append(dt.hour * 60 + dt.minute)
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


mp = MetaParser()
mp.tagstack = []
mp.attrstack = []
mp.s = []
mp.feed(urlopen('https://www.tutu.ru/station.php?nnst=35805&list=d5').read().decode('utf-8'))
mp.s.pop()
i = 0
j = 0
print(mp.s)
sleep(10)
for elem in mp.s:
    try:
        plot_train(elem[0])
    except:
        j += 1
    i += 1
    print(i)
print(j)
show()
#plot_train('https://www.tutu.ru/view.php?np=947c0499')
#plot_train('https://www.tutu.ru/view.php?np=fea997bb')
#show()

#f = open('F:\out.html', 'w', encoding='utf-8')
#f.write(s)
#f.close()
#os.chdir('C:\Program Files (x86)\Mozilla Firefox')
#os.system('firefox.exe F:\out.html')
