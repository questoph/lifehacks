## Tweak Skype 8 data export

AS you might know, you can export your chat data from Skype 8. To do so, just log into your [Skype account](https://go.skype.com/export) and request the export file. You can download the fie directly from the page or wait for a notification in the app that the export is ready for download.

Data export in Skype comes as a `.tar` file that contains a file named `messages.json`. So technically, your data is already in a decent format to work with. That is, until you actually open the file. Not only does the data contain a lot of useless markup language and tags, it also contains different versions of every edited message in the data.

To solve this, the script takes the `.tar` file, wranglesthe data in the `.json` archive and spits out clean backup files with your data in `.csv` and `.json` format.

### Usage

To tweak your data, simply call the script in your shell.

```Python
python tweak_skype_export.py
```

Additionally, you can specify up to 4 arguments:

```Python
-i OR --input name_or_path_to_tar_file
```

With this parameter you can specify the name or location of your export file. Currently the script expects the file to have the original name, though, that is, `8_USERNAME_export.tar`.

```Python
-o OR --output name_of_output_file
```

With this parameter you can specify a name of your choice for the output files. By default, the file will be named `Skype_DATE`. Note: Do not add a file extension to the name, this will be done automatically.

```Python
-u OR --user your_name
```

With this parameter you can specify the name to be added to all `from` messages in your chat data. By default, your user handle will be used for this, that is, if you have not renamed the original export file.

```Python
-z OR --zip
```

If you set this parameter, the script will conpress the output files to a `.zip` archive.
