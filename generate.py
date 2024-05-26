#!/usr/bin/env python3
import base64
import genanki
import glob
import hashlib
import html
import os
import random
import regex as re
import subprocess
from pathlib import Path

media = {}
decks = {}

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)
subprocess.run(['rm', '-rf', 'tmp'])
os.makedirs(f'tmp/media/', exist_ok=True)

_uniq_id = 1177320980
def uniq_id():
	global _uniq_id
	_uniq_id += 1
	return _uniq_id

# Deterministic random
random.seed(_uniq_id)

def hash(s):
    return base64.b64encode(hashlib.sha1(s).digest(), b'Xx').decode('UTF-8').rstrip('=')

def media_uniq(fn):
	global media
	h = hash(Path(fn).read_bytes())[0:8]
	ext = os.path.splitext(fn)[1]
	if h not in media:
		media[h] = f'tmp/media/{h}{ext}'
		os.symlink(f'../../{fn}', media[h])
	return os.path.basename(media[h])

def add_notes(deck, notes):
	random.shuffle(notes)
	for i,note in enumerate(notes):
		note.fields[0] = '{0:0>3}'.format(i+1)
		deck.add_note(note)

class Note_12(genanki.Note):
	@property
	def guid(self):
		return genanki.guid_for(self.fields[1], self.fields[2])

class Note_123(genanki.Note):
	@property
	def guid(self):
		return genanki.guid_for(self.fields[1], self.fields[2], self.fields[3])


### LG1 1 Pronounce
decks[1101] = genanki.Deck(uniq_id(), 'Learn Greenlandic::LG1 101 Pronounce (speak)')
decks[1102] = genanki.Deck(uniq_id(), 'Learn Greenlandic::LG1 102 Pronounce (transcribe)')

model_1101 = genanki.Model(
	uniq_id(),
	'Pronounce 1.1',
	fields=[
		{'name': 'Sort'},
		{'name': 'Syllables'},
		{'name': 'Hint'},
		{'name': 'Sound'},
	],
	sort_field_index=0,
	templates=[
		{
			'name': 'Pronounce 1.1',
			'qfmt': '<div style="text-align: center">Pronounce these syllables:<h1>{{Syllables}}</h1><br>{{hint:Hint}}</div>',
			'afmt': '{{FrontSide}}<div style="text-align: center"><hr id="answer">{{Sound}}</div>',
		},
	])

model_1102 = genanki.Model(
	uniq_id(),
	'Pronounce 1.2',
	fields=[
		{'name': 'Sort'},
		{'name': 'Syllables'},
		{'name': 'Hint'},
		{'name': 'Sound'},
	],
	sort_field_index=0,
	templates=[
		{
			'name': 'Pronounce 1.2',
			'qfmt': '<div style="text-align: center">Transcribe the syllables:<h1>{{Sound}}</h1><br>{{type:Syllables}}<br>{{hint:Hint}}</div>',
			'afmt': '{{FrontSide}}<div style="text-align: center"><hr id="answer"><h1>{{Syllables}}</h1></div>',
		},
	])

notes = []
notes2 = []
ws = Path('d/lg1/pronounce/words.txt').read_text().strip().split('\n')
for word in ws:
	w = word.split('\t')
	m = media_uniq(f'd/lg1/pronounce/{w[0]}.mp3')
	fields = [html.escape(f) for f in ['', w[0], f'[{w[1]}]', f'[sound:{m}]']]

	notes.append(Note_123(model=model_1101, fields=fields))

	fields = fields.copy()
	notes2.append(Note_123(model=model_1102, fields=fields))

add_notes(decks[1101], notes)
add_notes(decks[1102], notes2)


### LG1 2 Sound perception
decks[1201] = genanki.Deck(uniq_id(), 'Learn Greenlandic::LG1 201 Double consonants')
decks[1202] = genanki.Deck(uniq_id(), 'Learn Greenlandic::LG1 202 -r- or no -r-')
decks[1203] = genanki.Deck(uniq_id(), 'Learn Greenlandic::LG1 203 -tt- or -ts- or -t-')

model_1201 = genanki.Model(
	uniq_id(),
	'Perception 1.1',
	fields=[
		{'name': 'Sort'},
		{'name': 'Sound'},
		{'name': 'Word'},
		{'name': 'Consonant'},
	],
	sort_field_index=0,
	templates=[
		{
			'name': 'Perception 1.1',
			'qfmt': '<div style="text-align: center">Does this word contain "<tt>{{Consonant}}{{Consonant}}</tt>" or just "<tt>{{Consonant}}</tt>"?<h1>{{Sound}}</h1><br></div>',
			'afmt': '{{FrontSide}}<div style="text-align: center"><hr id="answer">{{Word}}</div>',
		},
	])

model_1202 = genanki.Model(
	uniq_id(),
	'Perception 1.2',
	fields=[
		{'name': 'Sort'},
		{'name': 'Sound'},
		{'name': 'Word'},
	],
	sort_field_index=0,
	templates=[
		{
			'name': 'Perception 1.2',
			'qfmt': '<div style="text-align: center">Does this word contain "<tt>r</tt>" or not?<h1>{{Sound}}</h1><br></div>',
			'afmt': '{{FrontSide}}<div style="text-align: center"><hr id="answer">{{Word}}</div>',
		},
	])

model_1203 = genanki.Model(
	uniq_id(),
	'Perception 1.3',
	fields=[
		{'name': 'Sort'},
		{'name': 'Sound'},
		{'name': 'Word'},
	],
	sort_field_index=0,
	templates=[
		{
			'name': 'Perception 1.3',
			'qfmt': '<div style="text-align: center">Does this word contain "<tt>tt</tt>", "<tt>ts</tt>", or just "<tt>t</tt>"?<h1>{{Sound}}</h1><br></div>',
			'afmt': '{{FrontSide}}<div style="text-align: center"><hr id="answer">{{Word}}</div>',
		},
	])

notes = []
for f in glob.glob('d/lg1/listening/1/*.mp3'):
	m = media_uniq(f)
	word = os.path.basename(f).replace('.mp3', '')
	cut = word[1:-1]
	for c in ['m', 'p', 'q', 's', 'l', 'k', 'n']:
		if c in cut:
			fields = ['', f'[sound:{m}]', word, c]
			notes.append(Note_123(model=model_1201, fields=fields))

add_notes(decks[1201], notes)

notes = []
for f in glob.glob('d/lg1/listening/2/*.mp3'):
	m = media_uniq(f)
	word = os.path.basename(f).replace('.mp3', '')
	fields = ['', f'[sound:{m}]', word]
	notes.append(Note_12(model=model_1202, fields=fields))

add_notes(decks[1202], notes)

notes = []
for f in glob.glob('d/lg1/listening/3/*.mp3'):
	m = media_uniq(f)
	word = os.path.basename(f).replace('.mp3', '')
	fields = ['', f'[sound:{m}]', word]
	notes.append(Note_12(model=model_1203, fields=fields))

add_notes(decks[1203], notes)

package = genanki.Package(decks.values())
package.media_files = media.values()
package.write_to_file('Learn Greenlandic.apkg')
