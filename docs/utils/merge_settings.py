from json import JSONDecoder, JSONDecodeError
import json
import re

NOT_WHITESPACE = re.compile(r'[^\s]')

def decode_stacked(document, pos=0, decoder=JSONDecoder()):
    while True:
        match = NOT_WHITESPACE.search(document, pos)
        if not match:
            return
        pos = match.start()
        
        try:
            obj, pos = decoder.raw_decode(document, pos)
        except JSONDecodeError:
            # do something sensible if there's some error
            raise
        yield obj


# C8 , CX , C1, C2
model = 'C2'
# categories: picture , aiPicture , option , other
category = 'picture'

mainCat = 'picture$hdmi1.expert2'


mergedData = {}

with open(f'defaultSettings-{model}.json', 'r') as infile:
    data = infile.read()

for obj in decode_stacked(data):
    if obj['category'].startswith(category):
        if category == 'picture' and not obj['category'].startswith(mainCat):
            continue
        else:
            mergedData = {**obj['value'], **mergedData}

with open(f'{category}-{model}.json', 'w') as outfile:
    json.dump(mergedData, outfile, sort_keys=True, indent=4)


