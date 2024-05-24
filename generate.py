#!/usr/bin/env python3
import argparse
import genanki
import glob
import html
import os
import random
import regex as re
import sys
from collections import defaultdict
from pathlib import Path

_uniq_id = 1177320980
def uniq_id():
	global _uniq_id
	_uniq_id += 1
	return _uniq_id

# Deterministic random
random.seed(_uniq_id)
def rand_id():
	return '{0:0>4X}'.format(random.randint(1, (1 << 16) - 1))

class Note_12(genanki.Note):
	@property
	def guid(self):
		return genanki.guid_for(self.fields[1], self.fields[2])

class Note_123(genanki.Note):
	@property
	def guid(self):
		return genanki.guid_for(self.fields[1], self.fields[2], self.fields[3])

media = []
decks = {}


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
	templates=[
		{
			'name': 'Pronounce 1.2',
			'qfmt': '<div style="text-align: center">Transcribe the syllables:<h1>{{Sound}}</h1><br>{{type:Syllables}}<br>{{hint:Hint}}</div>',
			'afmt': '{{FrontSide}}<div style="text-align: center"><hr id="answer"><h1>{{Syllables}}</h1></div>',
		},
	])

ws = Path('d/lg1/pronounce/words.txt').read_text().strip().split('\n')
for word in ws:
	w = word.split('\t')
	media.append(f'd/lg1/pronounce/{w[0]}.mp3')
	fields = [html.escape(f) for f in [rand_id(), w[0], f'[{w[1]}]', f'[sound:{w[0]}.mp3]']]

	note = Note_123(model=model_1101, fields=fields)
	decks[1101].add_note(note)

	fields = fields.copy()
	fields[0] = rand_id()
	note = Note_123(model=model_1102, fields=fields)
	decks[1102].add_note(note)


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
	templates=[
		{
			'name': 'Perception 1.3',
			'qfmt': '<div style="text-align: center">Does this word contain "<tt>tt</tt>", "<tt>ts</tt>", or just "<tt>t</tt>"?<h1>{{Sound}}</h1><br></div>',
			'afmt': '{{FrontSide}}<div style="text-align: center"><hr id="answer">{{Word}}</div>',
		},
	])

for f in glob.glob('d/lg1/listening/1/*.mp3'):
	media.append(f)
	word = os.path.basename(f).replace('.mp3', '')
	cut = word[1:-1]
	for c in ['m', 'p', 'q', 's', 'l', 'k', 'n']:
		if c in cut:
			fields = [rand_id(), f'[sound:{word}.mp3]', word, c]
			note = Note_123(model=model_1201, fields=fields)
			decks[1201].add_note(note)

for f in glob.glob('d/lg1/listening/2/*.mp3'):
	media.append(f)
	word = os.path.basename(f).replace('.mp3', '')
	fields = [rand_id(), f'[sound:{word}.mp3]', word]
	note = Note_12(model=model_1202, fields=fields)
	decks[1202].add_note(note)

for f in glob.glob('d/lg1/listening/3/*.mp3'):
	media.append(f)
	word = os.path.basename(f).replace('.mp3', '')
	fields = [rand_id(), f'[sound:{word}.mp3]', word]
	note = Note_12(model=model_1203, fields=fields)
	decks[1203].add_note(note)

package = genanki.Package(decks.values())
package.media_files = media
package.write_to_file('Learn Greenlandic.apkg')
