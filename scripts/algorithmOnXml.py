import json
import requests
import xml.etree.ElementTree as ET
import optparse
import math

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

def getTextInf(textToSend):
    payload = {'text': textToSend, 'lpmn': lpmn, 'user': user_mail}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    
    ccl = r.content.decode('utf-8')
    bases = ccl_bases(ccl)
    poses = ccl_poses(ccl)
    ctag_attr = ccl_ctag(ccl)
    
    return [ccl, bases, poses, ctag_attr];

def tableInit(xml, bases, poses, ctag_attr, weight):
    len_words = len(poses)
    count = []
    personsTable = []

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
        
    global table_result
    table_result = [[0 for i in range(len_byt)] for j in range(len_byt)]

    for i in range (0, len_byt): #byty
        for j in range (0, len_byt):
            if  i == j:
                table_result[i][j] = -1
            else:
                table_result[i][j] += (count[i] * weight) 
                table_result[j][i] += (count[i] * weight)  
                
    return [table_result, personsTable]

def div2method(sentencesAmount, windowSize):
    #wykorzystanie globalnej tablicy result i info
    for z in range (0, sentencesAmount):
        if int(windowSize/(2**z)) >= 1:
            weight = 2**z
            for i in range (0, sentencesAmount-1, int(windowSize/(2**z))):
                personsFromWindow = findPersonInWindow(i, i+int(windowSize/(2**z)), sentencesAmount)
                increaseConnections(personsFromWindow, weight)
        else:
            break

def findPersonInWindow(indexStart, indexStop, max):
    stop = indexStop
    start = indexStart
    
    if indexStop > max:
        stop = max
    
    #pusta tablica licznika wystąpień postaci i postaci
    global info
    bases = info[1]
    poses = info[2]
    ctag_attr = info[3]
    
    len_words = len(poses)
    byty = [] 
    count = []
    isInWindow = False
    dotCount = 1
    
    for i in range (0, len_words-1):
        #print(poses[i], bases[i]) 
        #brev', 'interp
        if poses[i] == 'interp' and poses[i-1] != 'brev':
            dotCount += 1
        
        if start <= dotCount:
            isInWindow = True
        if stop < dotCount:
            isInWindow = False
            break
        
        if isInWindow:
            if poses[i] == 'subst':
                if ctag_attr[i][3] == 'm1':
                    if str(bases[i]) in byty:
                        pI = byty.index(bases[i])
                        count[pI] = count[pI] + 1
                    
                    else:
                        byty.append(bases[i])
                        count.append(1)
    return [byty, count]
    #zwracam obie tablice

def increaseConnections(personsFromWindowWithCnt, weight):
    #print(personsFromWindowWithCnt, weight)
    global dependendencyTable, personsTable
    
    byty = personsFromWindowWithCnt[0]
    count = personsFromWindowWithCnt[1]
    len_byt = len(byty)
    #for i in range (0, len_byt):
        #print(byty[i], ":", count[i])
        
    #print("Wykryte byty w oknie: ", byty)

    for i in range (0, len_byt): #byty
        personIndex = personsTable.index(byty[i])
        for r in range (0, len_byt): 
            if r != i:
                personInRelationIndex = personsTable.index(byty[r])
                strengthOfRelation = (count[i] * weight)
                dependendencyTable[personIndex][personInRelationIndex] += strengthOfRelation
                dependendencyTable[personInRelationIndex][personIndex] += strengthOfRelation
    
    
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
Np. Bartosz zna się tylko z Pawłem.\
Reszta grupy jest nieznana.\
Mariusz jedzie autem Mariuszem."


#pobieram sobie całego xmla 
info = getTextInf(text)
#print("xml: ")
#print(info[0])
#print("\n")
#print("bases: ")
#print(info[1])
#print("\n")
#print("poses: ")
#print(info[2])
#print("\n")
#print("ctag: ")
#print(info[3])
#print("\n")

dependendencyTable = []
index = 0
weight = 2**index
sentencesAmount = len(text.split('.')) - 1 #-1 bo split ma na końcu jeszcze ''
windowSize = 20

#robie tablice osób w całym tekście
table = tableInit(info[0], info[1], info[2], info[3], weight)
dependendencyTable = table[0]
personsTable = table[1]

for i in dependendencyTable:
    print(i)

#analizuje tekst pod kątem okien
div2method(sentencesAmount, windowSize)

print(personsTable)
i = 0
for r in dependendencyTable:
    #print(personsTable[i], r)
    print(r)
    i+=1
