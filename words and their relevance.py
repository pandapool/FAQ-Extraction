import json

import pandas as pd
import requests

question_bank = pd.read_csv("C:/Users/hp/Desktop/Sorted Questions 29.12.18.csv",header = -1)
question_bank.rename({0:'question'},axis =1,inplace=True)
question_bank['question'] = question_bank['question'].apply(lambda x: ''.join([" " if ord(i) < 32 or ord(i) > 126 else i for i in x]))
question_bank['Key'] = None


#using IBM NLU API
x =0
headers = {
    'Content-Type': 'application/json',
}

params = (
    ('version', '2018-11-16'),
)
l =0
superdict = {}
while l < len(question_bank):
    qst = question_bank.question[l]
    print l
    data = {  "text": qst ,  "features": {  "keywords": {}  }}
    response = requests.post('https://gateway-lon.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2018-11-16', headers=headers, data=json.dumps(data), auth=('apikey', 'Lx2p1c8OuwYfFdK-dYLaZn58JZfrmyJH9de7uS9lt5m1'))
    b = response.text.encode('utf9')
    while b.find('"text"')!= -1:
        x = b.find('"text"')
        x = x+9
        text = ''
        while b[x] != '"' :
            text = text + b[x]
            x=x+1
        b=b.replace('"text"', ' ', 1)
        new_text=  '"' +text+'"'
        text = text.split(' ')
        while '' in text:
              text.remove('')
        text = ' '.join(text)
        b=b.replace(new_text, ' ', 1)
        x = b.find('"relevance"')
        x = x + 13
        rel =''
        while b[x] != ',':
            rel = rel + b[x]
            x = x+1
        b = b.replace('"relevance"', ' ', 1)
        b = b.replace(rel, ' ', 1)
        x = b.find('"count"')
        x = x+9
        count = ''
        while b[x] != '\n':
            count = count + b[x]
            x = x+1
        b = b.replace('"count"', ' ', 1)
        if question_bank.Key[l] == None:
            question_bank.Key[l] = {}
        question_bank.Key[l].update({text: [rel, count]})
        if text not in superdict.keys():
            superdict.update({text:float(count)})
        else:
            superdict[text]=superdict[text] + float(count)
    l = l+1

#segregating uni tri and bigrams

question_bank['bi']=[[] for _ in range(len(question_bank))]
question_bank['tri']=[[] for _ in range(len(question_bank))]
question_bank['uni']=[[] for _ in range(len(question_bank))]
question_bank['poly']=[[] for _ in range(len(question_bank))]

def extract_second(ele):
    return ele[1]

x = 0

while x<len(question_bank):
    l = question_bank.Key[x].keys()
    for y in l:
        g = [y,question_bank.Key[x][y][0],question_bank.Key[x][y][1]]
        if y.count(' ') == 0:
            question_bank.uni[x].append(g)
        elif y.count(' ') == 1:
            question_bank.bi[x].append(g)
        elif y.count(' ') == 2:
            question_bank.tri[x].append(g)
        else:
            question_bank.poly[x].append(g)
    x = x+1

x = 0
while x < len(question_bank):
    question_bank.uni[x].sort(key=extract_second,reverse=True)
    question_bank.bi[x].sort(key=extract_second,reverse=True)
    question_bank.tri[x].sort(key=extract_second,reverse=True)
    question_bank.poly[x].sort(key=extract_second,reverse=True)
    x = x+1

