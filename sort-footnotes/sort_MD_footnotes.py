# -*- coding: UTF-8 -*-

import re
import sys
import os

file_name = sys.argv[1]

# Collect the text, footnotes and footnote order in separate lists
text_by_lines = []
footnotes = []
fnotes_order = []

# Go over file, look for markup for footnotes and sort to lists
with open(file_name, 'r') as fi:
    ilines = fi.readlines()
    for line in ilines:
        if re.findall(r'^\[\^.+\]:', line):
            footnotes.append((re.match(r'\[\^(.+?)\]', line).group(1),
                              re.sub(r'^\[\^.+\]: ', '', line).strip()))
        else:
            text_by_lines.append(line.strip())
            fnotes = re.findall(r'\[\^(.+?)\]', line)
            if fnotes is not None:
                fnotes_order.extend(fnotes)

# Sort the footnotes by number
footnotes.sort(key=lambda x: fnotes_order.index(x[0]))

formatted = []
inlinecount = 1

# Replace the old footnote markers with the new ones
for line in text_by_lines:
    if re.search(r'\[\^.+\]', line):
        line_ = line.split()
        for word in line_:
            if re.search(r'\[\^.+\]', word):
                inword = re.sub(r'\[\^.+\]', r'[^{}]' .format(inlinecount), word)
                line_ = [inword if item == word else item for item in line_]
                inlinecount += 1
        line = ' '.join(line_)
    formatted.append(line)

# Write formatted text and footnotes to file
base, suffix = os.path.splitext(file_name)
outname = base + "_ordered" + suffix

with open(outname, 'w') as fo:
    for line in formatted:
        fo.write(line + '\n')
    for note in footnotes:
        fnote = f'[^{footnotes.index(note) + 1}]: {note[1]}'
        fo.write(fnote + '\n')
