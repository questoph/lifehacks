# -*- coding: UTF-8 -*-

import os
import shutil
import json
import argparse


def create_textbundle(input_file, assets_from, output_file):
    # Change to directory of input_file
    input_dir = os.path.dirname(os.path.abspath(input_file))
    os.chdir(input_dir)

    # Create the textbundle directory
    textbundle_dir = output_file
    os.makedirs(textbundle_dir, exist_ok=True)

    # Read the first 5 lines of the input file to check for theme information
    theme_info = None
    with open(input_file, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(min(5, len(lines))):
            line = lines[i].strip()
            if line.startswith("theme:"):
                theme_info = line.split(":")[1].strip()
                break

    # Replace the assets_from name with 'assets' in the input file to preserve image links
    updated_lines = []
    search_string = assets_from + '/'
    for line in lines:
        updated_lines.append(line.replace(search_string, 'assets/'))

    # Write the updated lines to the text.md file in the textbundle directory
    with open(os.path.join(textbundle_dir, 'text.md'), 'w', encoding="utf-8") as f:
        f.writelines(updated_lines)

    # Copy the assets folder to the textbundle directory
    assets_to = os.path.join(textbundle_dir, 'assets')
    shutil.copytree(assets_from, assets_to)

    # Create the info.json file
    info_json = {
        "creatorIdentifier" : "mobi.dudek.deckset",
        "transient" : False,
        "type" : "net.daringfireball.markdown", 
        "com.unsignedinteger.deckset" : {
            "presentationIdentifier" : "",
            "themeVariant" : "",
            "themeIdentifier" : ""
        },
        "version" : 2
    }

    # Update the info.json with the theme information if found
    if theme_info:
        theme_parts = theme_info.split(',')
        if len(theme_parts) == 2:
            info_json["com.unsignedinteger.deckset"]["themeIdentifier"] = theme_parts[0].strip()
            info_json["com.unsignedinteger.deckset"]["themeVariant"] = theme_parts[1].strip()

    with open(os.path.join(textbundle_dir, 'info.json'), 'w') as f:
        json.dump(info_json, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a Textbundle from a Markdown file and assets folder.')
    parser.add_argument('input_file', type=str, help='Path to the input Markdown file.')
    parser.add_argument('assets_from', nargs='?', default='imgs', type=str, help='Path to the assets folder: defaults to "imgs"')
    parser.add_argument('output_file', nargs='?', type=str, help='Path to the output Textbundle directory: defaults to the name of the input file.')

    args = parser.parse_args()

    # Set output_file to input_file name if not provided
    if args.output_file is None:
        args.output_file = args.input_file 

    # Ensure the output_file has the .textbundle extension
    if not args.output_file.endswith('.textbundle'):
        args.output_file = os.path.splitext(args.output_file)[0] + '.textbundle'

    create_textbundle(args.input_file, args.assets_from, args.output_file)