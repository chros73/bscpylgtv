# Output merged options and values into an MD file
# Usage: merge_settings.py C2

from json import JSONDecoder, JSONDecodeError
import json
import re
import sys

NOT_WHITESPACE = re.compile(r'[^\s]')

def read_file(fileName):
    with open(fileName, 'r') as infile:
        data = infile.read()

    return data

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

def get_category_fields(data, field=0):
    mData = []
    for obj in decode_stacked(data):
        categ = obj['category']
        if categ.startswith("picture"):
            res = categ.split('$')
            if len(res) > 1:
                if field == 0:
                    result = res[1].split('.')[0]
                else:
                    res2 = res[1].split('.')
                    if len(res2) > field - 1:
                        result = res2[field - 1]

                if result not in ["" ,"x"] and result not in mData:
                    mData.append(result)

    return sorted(mData)

def get_categories(data, excludeCats):
    catsData = []
    for obj in decode_stacked(data):
        categ = obj['category']
        cat = categ.split('$', 1)[0]
        if cat not in excludeCats and cat not in catsData:
            catsData.append(cat)

    return catsData

def get_merged_options(catsData, data):
    optionData = {}
    for category in catsData:
        mergedData = {}

        for obj in decode_stacked(data):
            if (category == "" and obj['category'] == category) or (category != "" and obj['category'].startswith(category)):
                mergedData = {**obj['value'], **mergedData}

        optionData[category] = mergedData

    return optionData

def get_merged_values(catsData, data):
    valueData = {}
    for category in catsData:
        mergedData = {}

        for obj in decode_stacked(data):
            for record in obj:
                if (category == "" and record['category'] == category) or (category != "" and record['category'].startswith(category)):
                    key = record["key"]
                    if key not in optionData[category]:
                        continue
                    elif "values" not in record:
                        continue
                    elif record["values"] == []:
                        continue
                    elif "file" in record["values"]:
                        continue
                    elif "arrayExt" in record["values"] and record["values"]["arrayExt"] == []:
                        continue
                    elif "arrayExt" in record["values"] and record["values"]["arrayExt"] != []:
                        values = [entry["value"] for entry in record["values"]["arrayExt"]]
                        # do not include trivial values
                        if sorted(values) == ["0", "1"] or sorted(values) == ["off", "on"] or sorted(values) == ["disable", "enable"] or sorted(values) == ["false", "true"] or sorted(values) == [False, True]:
                            continue
                    elif "range" in record["values"]:
                        values = record["values"]["range"]
                    else:
                        values = record["values"]

                    mergedData[key] = values

        valueData[category] = mergedData

    return valueData

def get_system_options(data, key):
    mData = {}
    match = re.search(r'var validSettings = (.*?);', data, re.DOTALL)
    if match:
        json_str = match.group(1).strip()
        # replace JS keys that are without quotes with quoted ones
        json_str = re.sub(r'(\w+)\s*:', r'"\1":', json_str)
        mData = json.loads(json_str)

    return (mData[key] if key in mData else mData)

def write_list(file, items):
    line = ''
    for item in items:
        if len(line) + len(item) + 1 > 90:
            file.write(line + '\n')
            line = item + ', '
        else:
            line += item + ', '
    if line:
        file.write(line.rstrip(', '))


# check for mandatory argument
if len(sys.argv) < 2:
    raise Exception("ERROR: Model number has to be specified as a parameter")

# variables
model = sys.argv[1]
settingsFile = f'defaultSettings-{model}.json'
valuesFile = f'description-{model}.json'
systemFile = f'valid-settings-{model}.js'
outputFile = f'available_settings_{model}.md'
excludeCats = ["dimensionInfo", "pqsettings", "psmModified", "settingsservice"]

# open defaultSettings file to get available options
data = read_file(settingsFile)
# get inputs
inputsData = get_category_fields(data)
# get inputs
presetsData = get_category_fields(data, 2)
# get dynamic range modes
dynmodesData = get_category_fields(data, 3)
# get categories
catsData = get_categories(data, excludeCats)
# get merged options data
optionData = get_merged_options(catsData, data)

# open description file to get available values
data = read_file(valuesFile)
# get merged values data
valueData = get_merged_values(catsData, data)

# open valid-settings file to get available system options
data = read_file(systemFile)
# get setSettings options data
systemSetData = get_system_options(data, "setSettingsValidKeySet")
# get getSettings options data
systemGetData = get_system_options(data, "getSettingsValidKeySet")

# write data into file
if optionData != {}:
    with open(outputFile, 'w') as outfile:
        outfile.write(f'### OLED {model} (year) firmware vx, webOS vx\n')
        outfile.write(f'Available settings per category that can be used with various methods.\n\n')
        # write inputs
        outfile.write(f'#### Inputs\n```\n')
        write_list(outfile, inputsData)
        outfile.write(f"\n```\n\n")
        # write presets
        outfile.write(f'#### Picture modes (presets)\n```\n')
        write_list(outfile, presetsData)
        outfile.write(f"\n```\n\n")
        # write dynamic range modes
        outfile.write(f'#### Dynamic range modes\n```\n')
        write_list(outfile, dynmodesData)
        outfile.write(f"\n```\n\n")
        for cat in optionData:
            # write options
            outfile.write(f'#### `"{cat}"` category - available settings (used by `set_settings` method)\n```json\n')
            json.dump(optionData[cat], outfile, sort_keys=True, indent=4)
            outfile.write(f"\n```\n\n")
            # write values
            if cat in valueData and valueData[cat] != {}:
                outfile.write(f'##### `"{cat}"` category - available non-trivial values\n```json\n')
                json.dump(valueData[cat], outfile, sort_keys=True, indent=4)
                outfile.write(f'\n```\n\n')
        # write system options
        outfile.write(f'#### some of the settings above can also be set via the public API (used by `set_system_settings` method)\n```json\n')
        json.dump(systemSetData, outfile, sort_keys=True, indent=4)
        outfile.write(f"\n```\n\n")
        outfile.write(f'#### some of the settings above can be retrieved by the public API (used by `get_system_settings` method)\n```json\n')
        json.dump(systemGetData, outfile, sort_keys=True, indent=4)
        outfile.write(f"\n```\n\n")


