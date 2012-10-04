#!/usr/bin/env python
import sys
import json

def extract_character_speech(data, characters):
    characters = set(characters)
    for url, dialogue in data.iteritems():
        for name, speech in dialogue:
            if name in characters or '*' in characters:
                yield speech

def main():
    data = json.load(sys.stdin)
    characters = [name.decode('utf8') for name in sys.argv[1:]]
    for speech in extract_character_speech(data, characters):
        print speech.encode('utf8')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main()
    else:
        print 'Usage: character_corpus.py NAME [NAME ...] < data.json'

