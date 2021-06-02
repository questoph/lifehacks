# -*- coding: UTF-8 -*-

import argparse
import datetime
import glob
import html
import json
import logging
import os
import re
import sys
import tarfile
import zipfile
from collections import OrderedDict

import pandas as pd

# Set directory name for script
dirname = os.path.dirname(__file__)

# Set up argparse
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', required=False, help='Infile name', nargs='?')
ap.add_argument('-o', '--output', help='Outfile name', nargs='?', default=f'Skype_{datetime.date.today()}')
ap.add_argument('-u', '--user', required=False, help='User handle', nargs='?')
ap.add_argument('-z', '--zip', required=False, help='Zip files', action='store_true')

args = vars(ap.parse_args())

# Look for tar file in directory if --input is not set
if args['input']:
    infile = args['input']
else:
    infile = glob.glob('*_export.tar')[0]

# Set user name for message "from" handling
if args['user']:
    handle = args['user']
else:
    handle = re.sub('_export.tar$', '', infile)

try:
    export = tarfile.open(infile, 'r:tar')
    export.extractall()
    export.close()
    with open('messages.json', encoding='utf-8') as input:
        msgs = json.load(input)
    os.remove('messages.json')
    os.remove(infile)
except:
    logging.exception('Exception while reading input file:')
    sys.exit(1)

# Collect messages in an ordered dict
history = {}
userId = msgs['userId']

for conv in msgs['conversations']:

    # Extract conversationid, displayName, messagetype, content, originalarrivaltime, id (time in ms)
    for msg in conv['MessageList']:

        # Set time stamp for messages
        timestamp = int(int(msg['id']) / 1000)
        dt_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        if msg['content']:
            msg['content'] = re.sub('\\r(?!\\n)', '\\n', msg['content'])
            msg['content'] = html.unescape(msg['content'])

        if msg['displayName']:
            msg['displayName'] = msg['displayName']
        elif msg['from'] == userId:
            msg['displayName'] = handle

        # Write content to dict
        history[timestamp] = OrderedDict([('date', dt_time), ('conversationid', msg['conversationid']),
                                          ('displayName', msg['displayName']), ('id', msg['id']),
                                          ('content', msg['content'])])

# Collect keys for edited messages in list (the original version, not the edited one)
edited = set()
for k, v in history.items():
    if '<e_m a=' in v['content']:
        for ka, vau in history.items():
            if vau['content'] == v['content'] and vau['id'] != v['id']:
                if v['date'] < vau['date']:
                    edited.add(k)
                elif v['date'] > vau['date']:
                    edited.add(ka)

# Filter history by removing the duplicates of edited messages
# Clip the edit tag info along the way
clean_hist = {}
for k, v in history.items():
    if k in edited:
        pass
    else:
        if '<e_m a=' in v['content']:
            v['content'] = v['content'].split('<e_m a=', 1)[0]
        clean_hist[k] = v

# Convert to dataframe and write to CSV
df = pd.DataFrame(clean_hist).transpose()
df.sort_values(by=['conversationid', 'id'], ascending=[True, True], inplace=True)
df.to_csv(args['output'] + '.csv', index=False)
df.to_json(args['output'] + '.json', orient="index")

# Zip to file if specified
if args['zip']:
    archive = zipfile.ZipFile(args['output'] + '.zip', mode='w', compression=zipfile.ZIP_DEFLATED)
    archive.write(args['output'] + '.csv')
    archive.write(args['output'] + '.json')
    archive.close()
    os.remove(args['output'] + '.json')
    os.remove(args['output'] + '.csv')
