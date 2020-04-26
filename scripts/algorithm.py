import json
import requests
import xml.etree.ElementTree as ET
import optparse

parser = optparse.OptionParser()
parser.add_option('-x', '--xml', action="store_true", dest="xml", default=False)
parser.add_option('-t', '--token-text', action="store_true", dest="token_text", default=False)
parser.add_option('-b', '--token-bases', action="store_true", dest="token_bases", default=False)
parser.add_option('-s', '--token-speech', action="store_true", dest="token_speech", default=False)
options, args = parser.parse_args()

def ccl_orths(ccl):
	tree = ET.fromstring(ccl)
	return [orth.text for orth in tree.iter('orth')]

def ccl_bases(ccl):
	tree = ET.fromstring(ccl)
	return [tok.find('./lex/base').text for tok in tree.iter('tok')]

def ccl_poses(ccl):
	tree = ET.fromstring(ccl)
	return [tok.find('./lex/ctag').text.split(":")[0] for tok in tree.iter('tok')]

def ccl_ctag(ccl):
	tree = ET.fromstring(ccl)
	return [tok.find('./lex/ctag').text.split(":") for tok in tree.iter('tok')]

def tableInit(textToSend, weight, personsTable):
    payload = {'text': textToSend, 'lpmn': lpmn, 'user': user_mail}
    headers = {'content-type': 'application/json'}

    r = requests.post(url, data=json.dumps(payload), headers=headers)
    ccl = r.content.decode('utf-8')
    bases = ccl_bases(ccl)
    
    poses = ccl_poses(ccl)

    ctag_attr = ccl_ctag(ccl)
    #print(ctag_attr)
    len_words = len(poses)
    count = []

    for i in range (0, len_words-1):
        if poses[i] == 'subst':
            if ctag_attr[i][3] == 'm1':
                if str(bases[i]) in personsTable:
                    pI = personsTable.index(bases[i])
                    count[pI] = count[pI] + 1
                
                else:
                    personsTable.append(bases[i])
                    count.append(1)

    len_byt = len(personsTable)
    for i in range (0, len_byt):
        print(personsTable[i], ":", count[i])
        
    #robie tablice il byt x il byt
    global table_result
    table_result = [[0 for i in range(len_byt)] for j in range(len_byt)]
    #print(table_result)
    print("tekst: ", text.split("."))

    #tablica osób z całego tekstu
    #byty to są wszystkie osoby

    for i in range (0, len_byt): #byty
        for j in range (0, len_byt):
            if  i == j:
                table_result[i][j] = -1
            else:
                table_result[i][j] += (count[i] * weight) 
                table_result[j][i] += (count[i] * weight)  
                
    #personsTable = byty
    print("nono: ", table_result)
    return table_result

def dependencySearch(textTable, table_result, weight, personsTable):
    textToSend = ""
    for t in textTable:
        textToSend += t + ". "
    
    print("Text do analizy: ", textToSend)
    
    payload = {'text': textToSend, 'lpmn': lpmn, 'user': user_mail}
    headers = {'content-type': 'application/json'}

    r = requests.post(url, data=json.dumps(payload), headers=headers)
    ccl = r.content.decode('utf-8')
    bases = ccl_bases(ccl)
    
    poses = ccl_poses(ccl)

    ctag_attr = ccl_ctag(ccl)
    #print(ctag_attr)
    len_words = len(poses)
    byty = [] 
    count = []

    for i in range (0, len_words-1):
        if poses[i] == 'subst':
            if ctag_attr[i][3] == 'm1':
                if str(bases[i]) in byty:
                    pI = byty.index(bases[i])
                    count[pI] = count[pI] + 1
                
                else:
                    byty.append(bases[i])
                    count.append(1)

    len_byt = len(byty)
    for i in range (0, len_byt):
        print(byty[i], ":", count[i])
        
    print("Wykryte byty w oknie: ", byty)

    for i in range (0, len_byt): #byty
        personIndex = personsTable.index(byty[i])
        for r in range (0, len_byt): 
            if r != i:
                personInRelationIndex = personsTable.index(byty[r])
                strengthOfRelation = (count[i] * weight)
                table_result[personIndex][personInRelationIndex] += strengthOfRelation
                table_result[personInRelationIndex][personIndex] += strengthOfRelation
                #print("wstawienie relacji :[", personIndex, personInRelationIndex, "][", personInRelationIndex, personIndex, "]", byty[i], "-", byty[r], ",", " o wartość :" , count[i] * weight)
                #for d in table_result:
                #    print(d)

def divWindow(text, windowSize, index):
    #biorę windowSize zdań
    textInWindow = ""
    
    for j in range (0, windowSize):
        textInWindow += text[i+j]
    print("Sprawdzany tekst: ", textInWindow, ", w:", windowSize, ", i:", index)
    #odpalam szukanie
    global table_result, personsTable
    dependencySearch(textInWindow.split('.'), table_result, 2**index, personsTable)
    #pomniejszam okno na 2 aż dojdzie do dwóch zdań
    

clarinpl_url = "http://ws.clarin-pl.eu/nlprest2/base"
user_mail = "testo@.test.pl"

url = clarinpl_url + "/process"

# Tag and recognize named entities (coarse-grained categories)
lpmn = 'wcrft2|liner2({"model":"top9"})'

text1 = "Paweł robi zadanie z Przemek.\
Przemek współpracuje z Pawłem.\
Wojtek pisze jutro Kolokwium z angielskiego.\
Przemek pisze kolokwium z Wojtkiem.\
Bartosz zrobił już coś.\
Bartosz zna się tylko z Pawłem.\
Reszta grupy jest nieznana." 

text = "Paweł robi zadanie z Przemek.\
Przemek współpracuje z Pawłem.\
Wojtek pisze jutro Kolokwium z angielskiego.\
Przemek pisze kolokwium z Wojtkiem.\
Bartosz zrobił już coś.\
Bartosz zna się tylko z Pawłem.\
Reszta grupy jest nieznana.\
Mariusz jedzie autem Mariuszem."

#text = ""
#for i in range (0, 100):
#    text += str(i) + ". "


textTable = text.split('.')
dependendencyTable = []
personsTable = []
index = 0
weight = 2**index

#get all dependencies to table, gett all persons in text
dependendencyTable = tableInit(text, weight, personsTable)

print("Osoby znalezione w tekście: ", personsTable)
len_persons = len(personsTable)
print("Tablica zależności: ")
for d in dependendencyTable:
    print(d)


sentencesAmount = len(textTable)
windowSize = 20

for z in range (0, sentencesAmount):
    if int(windowSize/(2**z)) >= 2:
        for i in range (0, sentencesAmount-1, int(windowSize/(2**z))):
            #biorę windowSize zdań
            textInWindow = ""
            
            for j in range (0, int(windowSize/(2**z))):
                if i+j < sentencesAmount:
                    textInWindow += textTable[i+j] 
                    textInWindow += ". "
            print("Sprawdzany tekst: ", textInWindow, ", w:", windowSize, ", i:", 2**z)
            #odpalam szukanie

            dependencySearch(textInWindow.split('.'), table_result, 2**z, personsTable)
            #pomniejszam okno na 2 aż dojdzie do dwóch zdań
    else:
        break
    


index += 1
weight = 2**index
#funkcja dzieląca tekst i ustalająca wagi
#dependencySearch(text1.split('.'), dependendencyTable, weight, personsTable)
print("Tablica zależności po szukaniu w oknie: ")
for d in dependendencyTable:
    print(d)
