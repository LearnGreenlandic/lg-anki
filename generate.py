#!/usr/bin/env python3
import argparse
import genanki
import glob
import html
import os
import regex as re
import sys
from collections import defaultdict
from pathlib import Path

uniq_id = 1177320980

class Note_Pronounce(genanki.Note):
	@property
	def guid(self):
		return genanki.guid_for(self.fields[0])

deck = genanki.Deck(uniq_id, 'Learn Greenlandic')

model = genanki.Model(
	uniq_id+1,
	'Pronounce 1',
	fields=[
		{'name': 'Syllables'},
		{'name': 'Hint'},
		{'name': 'Sound'},
	],
	templates=[
		{
			'name': 'Pronounce 1.1',
			'qfmt': '<div style="text-align: center">Pronounce these syllables:<h1>{{Syllables}}</h1><br><a id="btnHint" onclick="document.getElementById(\'hint\').setAttribute(\'style\', \'\');document.getElementById(\'btnHint\').setAttribute(\'style\', \'display: none\');">Hint</a><div id="hint" style="display: none">[{{Hint}}]</div></div>',
			'afmt': '{{FrontSide}}<div style="text-align: center"><hr id="answer">{{Sound}}</div>',
		},
	])

media = []

words = {}
ws = Path('d/lg1/pronounce/words.txt').read_text().strip().split('\n')
for word in ws:
	w = word.split('\t')
	media.append(f'd/lg1/pronounce/{w[0]}.mp3')
	note = Note_Pronounce(model=model, fields=[html.escape(f) for f in [w[0], w[1], f'[sound:{w[0]}.mp3]']])
	deck.add_note(note)

package = genanki.Package(deck)
package.media_files = media
package.write_to_file('Learn Greenlandic.apkg')
