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

clarinpl_url = "http://ws.clarin-pl.eu/nlprest2/base"
user_mail = "testo@.test.pl"

url = clarinpl_url + "/process"

# Tag and recognize named entities (coarse-grained categories)
lpmn = 'wcrft2|liner2({"model":"top9"})'

text = "Paweł robi zadanie z Przemek.\
Przemek współpracuje z Pawłem.\
Wojtek pisze jutro Kolokwium z angielskiego.\
Przemek pisze kolokwium z Wojtkiem.\
Bartosz zrobił już coś.\
Bartosz zna się tylko z Pawłem.\
Reszta grupy jest nieznana."

payload = {'text': text, 'lpmn': lpmn, 'user': user_mail}
headers = {'content-type': 'application/json'}

r = requests.post(url, data=json.dumps(payload), headers=headers)
ccl = r.content.decode('utf-8')

# The simplest use case
if (options.xml):
	print(ccl)

# Print a list of token text forms
if (options.token_text):
	orths = ccl_orths(ccl)
	print(orths)

# Print a list of token bases
if (options.token_bases):
	bases = ccl_bases(ccl)
	print(bases)

# Print a list of token part of speech tags
if (options.token_speech):
	poses = ccl_poses(ccl)
	print(poses)


