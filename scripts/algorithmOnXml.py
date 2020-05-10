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
                
    return table_result

def findPersonInWindow(indexStart, indexStop, textInfo):
    
    
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
sentencesAmount = len(text)
windowSize = 20

#robie tablice osób w całym tekście
dependendencyTable = tableInit(info[0], info[1], info[2], info[3], weight)

for i in dependendencyTable:
    print(i)

#analizuje tekst pod kątem okien
for z in range (0, sentencesAmount):
    if int(windowSize/(2**z)) >= 2:
        for i in range (0, sentencesAmount-1, int(windowSize/(2**z))):
            dependencySearch(textInWindow.split('.'), table_result, (z**z), personsTable)
    else:
        break


    #pobieram listę bytów z ilośći zdań, licze kropki
