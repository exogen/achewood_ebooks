#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import json
import HTMLParser
from collections import defaultdict
from bs4 import BeautifulSoup

replace_names = {
    'Teodor': u'Téodor',
    'T?Odor': u'Téodor',
    'T Odor': u'Téodor',
    'Tedor': u'Téodor',
    'Tedoor': u'Téodor',
    'Teodore': u'Téodor',
    'Beef': 'Roast Beef',
    'Roastbeef': 'Roast Beef',
    'Mr. Bear': 'Cornelius',
    'Mr Bear': 'Cornelius',
    'Cornelius Bear': 'Cornelius',
    'Lie-Bot': 'Lie Bot',
    'Lie Bott': 'Lie Bot',
    'Mrs Smuckles': 'Mrs. Smuckles',
    "Ray's Mother": 'Mrs. Smuckles',
    "Ray's Mom": 'Mrs. Smuckles',
    'Phillippe': 'Philippe',
    'Phillipe': 'Philippe',
    'Phillip': 'Philippe',
    'Philippie': 'Philippe',
    'Raymond': 'Ray',
    'Ray Smuckles': 'Ray',
    'Ramses': 'Ramses Luther Smuckles',
    'Ramses Luther': 'Ramses Luther Smuckles',
    'Rod': 'Rod Huggins',
    'Lil Nephew': 'Little Nephew',
    'Nightlife': 'Nightlife Mingus',
    'Pete': 'Nice Pete',
    'Pat Reynolds': 'Pat',
}

replace_speech = {
    'Teodor': u'Téodor',
    'TEODOR': u'TÉODOR',
    'T?odor': u'Téodor',
    'T?ODOR': u'TÉODOR',
}

def scrape_all(filenames):
    data = {}
    characters = defaultdict(list)
    for filename in filenames:
        for row, url, dialogue in scrape_file(open(filename)):
            data[url] = dialogue
            for name, speech in dialogue:
                characters[name].append(speech)

    return data

def unescape(s):
    p = HTMLParser.HTMLParser()
    return p.unescape(s)

def normalize(s):
    s = s.replace(u'‘', "'").replace(u'’', "'") # Dumb down smart single quotes.
    s = s.replace(u'“', '"').replace(u'”', '"') # Dumb down smart double quotes.
    s = re.sub(r'[ ]+', ' ', s) # Condense multiple spaces.
    return s

def normalize_name(name):
    name = name.title()
    name = name.replace("'S ", "'s ")
    name = name.replace(' Thinks', '').replace(' Thinking', '')
    name = name.replace(' Types', '').replace(' Typing', '')
    return replace_names.get(name, name)

def normalize_speech(text):
    for key, value in replace_speech.iteritems():
        text = text.replace(key, value)
    return text

def scrape_file(fileobj):
    s = fileobj.read()
    try:
        html = s.decode('utf8')
    except UnicodeDecodeError:
        html = s.decode('iso-8859-1')

    rows = re.findall('<td valign="top" align="left">(.*?)</td>', html)
    for row in rows:
        parts = row.split('<div class="tinylink">')
        text = normalize(unescape(parts[0]))
        if len(parts) > 1:
            url = parts[1].split('</div>')[0]
            dialogue = list(parse_transcription(text))
            yield (row, url, dialogue)

def remove_meta(text):
    text = re.sub(r'(\[.*?\]+)', '', text)
    text = re.sub(r'(\{.*?\}+)', '', text)
    text = re.sub(r'(<.*?>+)', '', text)
    return text

def remove_speech_meta(text):
    text = re.sub(r'^(\s*\([^)]*\)\s*)', '', text)
    text = re.sub(r'(\s*\([^)]*\)\s*)$', '', text)
    return text

def parse_transcription(text):
    lines = [line.strip() for line in text.split(' / ')]
    for original_line in lines:
        line = remove_meta(original_line).strip()
        match = re.match(r"([\w?][\w?'. -]*)[^:]*:(.*)", line, re.UNICODE)
        if match:
            name = normalize_name(match.group(1).strip())
            speech = normalize_speech(remove_speech_meta(match.group(2).strip()))
            if name and len(name) < 30 and speech:
                yield (name, speech)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print json.dumps(scrape_all(sys.argv[1:]))
    else:
        print "Usage: parse_transcriptions.py file [file ...]"

