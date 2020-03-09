#!/Users/florian/anaconda3/bin/python

# inspired by https://github.com/DanonX2/A-Vocabulary.com-Vocab-List-TO-Anki-Deck-Converter

import bs4
import requests
import json
import sys
import os.path
import genanki

__doc__ = """
usage: wordlist2anki.py wordlist

creates output.apkg for import into anki
"""



"""
obtain word pos, definition, description and word family from vocabulary.com
"""
def worddef(word):

    URL = "https://www.vocabulary.com/dictionary/{word}".format(word = word)

    response = requests.get(URL)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    _ = [x.strip() for x in soup.find('h3', class_ = 'definition').text.split('\r\n') if x.strip() != '']

    pos = _[0]
    definition = _[1]
    
    #definition = '{word} ({pos}): {definition}'.format(word = word,
    #                                                   pos = pos,
    #                                                   definition = definition)

    _ = soup.find('p', class_ = 'short')
    description = ('' if _ is None else _.text)

    #desc_long = soup.find('p', class_ = 'long').text

    family = soup.find('vcom:wordfamily')['data']
    fp = json.loads(family)
    _ = sorted([(x['word'], x.get('parent', ''),x['type'], x['ffreq']) for x in fp if x.get('parent',word) == word and x.get('hw', False) == True], key = lambda x: x[3], reverse = True)
    wordfamily = [x[0] for x in _]

    return (word, pos, definition, description, wordfamily)



if __name__ == '__main__':

    wordlist =[]
    wordlistfile = sys.argv[1]
    with open(wordlistfile) as fh:
        for line in fh:
            wordlist.append(line.strip())

    items = []
            
    for word in wordlist:
        word, pos, definition, description, wordfamily = worddef(word)
        
        
        print(word, pos, definition, description, wordfamily, sep='\n')

        items.append(("{word} ({pos})".format(word = word, pos = pos),
                      definition,
                      description.replace(word, '____').replace(word.capitalize(), '____'),
                      ' - '.join(wordfamily)))

    

    my_model = genanki.Model(
        1607392324,
        'Vocabulary.com 2',
        fields=[
            {'name': 'word'},
            {'name': 'definition'},
            {'name': 'description'},
            {'name': 'wordfamily'}
        ],
        templates=[
            {
                'name': 'Forward Card',
                'qfmt': '{{word}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{definition}}<br><br>{{description}}<br><br>{{wordfamily}}'
            },
            {
                'name': 'Reverse Card',
                'qfmt': '{{definition}}<br><br>{{description}}',
                'afmt': '{{FrontSide}}<hr>{{word}}<br><br>{{wordfamily}}'
            }
        ])

    my_deck = genanki.Deck(2059400132, "MH Booklet 1")

    for i in items:
        my_deck.add_note(genanki.Note(
            model=my_model,
            fields=i))

    genanki.Package(my_deck).write_to_file('output.apkg')
            
