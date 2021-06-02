## Sort markdown footnotes

Over the last years I have developed a workflow for text production that almost completely runs on Markdown. Even longer papers or book projects live in Markdown files, at least at draft stage. And while I certainly love Markdown for its flexibility and ease of use, I sometimes run into situations that require a bit of text processing.

This is the case for working with footnotes, for example, especially in longer texts. Technically, Markdown parsers don't care about the numerical order in which you enter the footnotes in your text. 1 can be followed by 6, by 3 and then by 15. You will always end up with the correct numbering and order once you export your file to another file format.

However, in some cases I find it useful to bring the footnotes in a text in the correct top to bottom order to better keep track of the text structure. And that is what this script does.

### Usage

To reorder your text, simply call the script in your shell.

```Python
python sort_MD_footnotes.py name_or_path_to_text_file
```

It takes one parameter, that is, the name or path of the file you want to reorganize. Out of the box, the script works with `.md` and `.txt` files.
