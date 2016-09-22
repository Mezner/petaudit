import urllib2
import json
import argparse

parser = argparse.ArgumentParser(description='Produces a CSV of all pets')
parser.add_argument('api_key', metavar='A', help='API token key')
parser.add_argument('realm', metavar='R', help='Realm of cahracter (e.g. Garona)')
parser.add_argument('char', metavar='C', help='Character name')

args = parser.parse_args()
all_pets_request_uri = 'https://us.api.battle.net/wow/pet/?locale=en_US&apikey={}'.format(args.api_key)
user_pets_request_uri = 'https://us.api.battle.net/wow/character/{}/{}?fields=pets&locale=en_US&apikey={}'.format(args.realm, args.char, args.api_key)
response = urllib2.urlopen(all_pets_request_uri)
pet_json = json.loads(response.read())
all_pets = pet_json['pets']
response = urllib2.urlopen(user_pets_request_uri)
pet_json = json.loads(response.read())
user_pets = pet_json['pets']['collected']
has_pets = {}

for user_pet in user_pets:
	has_pets[user_pet['creatureId']] = True

with open('types') as f:
	types = f.readlines()

types = [t.rstrip() for t in types]

weak_against_headers = ['weak against ' + t for t in types]
strong_against_headers = ['strong against ' + t for t in types]

print 'Have?,Name,Wowhead,Family,{},{}'.format(','.join(strong_against_headers), ','.join(weak_against_headers))

for pet in all_pets:
	name = pet['name'].replace(',', '')
	name_link = 'http://www.wowhead.com/search?q={}'.format(name)
	family = pet['family']
        weak_against = pet['weakAgainst']
	strong_against = pet['strongAgainst']
	has_pet = has_pets.has_key(pet['creatureId'])
        weak_flags = [str(t in weak_against) for t in types]
	strong_flags = [str(t in strong_against) for t in types]
	print '{},{},{},{},{},{}'.format(has_pet, name, name_link, family, ','.join(strong_flags), ','.join(weak_flags))
	
