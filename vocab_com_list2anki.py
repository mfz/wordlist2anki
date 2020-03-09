#!/Users/florian/anaconda3/bin/python

import bs4
import requests
import genanki
import sys


URL = sys.argv[1]

response = requests.get(URL)

soup = bs4.BeautifulSoup(response.text, "html.parser")


items = []

for li in soup.find_all('li', class_ = 'entry'):
    word = li.find('a', class_ = 'word').text
    definition = li.find('div', class_ = 'definition').text
    _ = li.find('div', class_ = 'example')
    if _ is None:
        example = ''
    else:
        example = _.text
    example = example.replace('\n', '').replace(word, '____')
    items.append((word, definition, example))

my_model = genanki.Model(
  1607392319,
  'Simple Model',
  fields=[
    {'name': 'word'},
    {'name': 'definition'},
    {'name': 'example'},
  ],
  templates=[
      {
          'name': 'Forward Card',
          'qfmt': '{{word}}',
          'afmt': '{{FrontSide}}<hr id="answer">{{definition}}<br><br>{{example}}',
      },
      {
          'name': 'Reverse Card',
          'qfmt': '{{word}}<br><br>{{example}}',
          'afmt': '{{FrontSide}}<hr>{{definition}}'
      }
  ])

my_deck = genanki.Deck(2059400110, "MH Booklet 1")

for i in items:
    my_deck.add_note(genanki.Note(
        model=my_model,
        fields=i))

genanki.Package(my_deck).write_to_file('output.apkg')
    
