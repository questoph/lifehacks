## Write Deckset presentation to .textbundle file

Since 2014, I've been doing almost all of my presentations in Markdown using [Deckset](https://www.deckset.com). Deckset is a wonderful tool, and on MacOS it is document-based, which means you have complete freedom in how you organise your files, e.g., for asset management. However, with the recent introduction of Deckset for iOS, Deckset has switched to using `.textbundle` files due to iOS sandboxing. For this reason, if you are moving presentations from Mac to iPad, you will need to convert your presentations to the `.textbundle` format, also because Deckset does not currently offer an export function for this.

This is what this script does. It takes the name of your presentation file, your asset folder and the desired output file (of type `.textbundle`) and converts your presentation to be compatible with Deckset on iOS. Deckset on MacOS will also work with these files, but for my daily workflow I much prefer to work with open folders and documents.

### Usage

To reorder the notes in your text, simply call the script in your shell.

```Python
python write_Deckset_textbundle.py input_file asset_folder output_file
```

It takes up to three arguments:

- the name of the input file (can be `.txt` or `.md`); this argument is required
- the name of the assets folder (e.g., 'imgs'); defaults to 'imgs' if not provided
- the name of the output file including the `.textbundle` suffix (e.g., 'presentation.textbundle'); defaults to the name of the input_file if not provided.