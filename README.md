# doma.in
A generator for short domains with dots. e.g `domain` can become `doma.in`.

## Usage
Before using, you must download the latest list of TLDS using `python domain.py --download-tlds`

Then to generate a domain you can simply use `python domain.py -g YOUR-TEXT-HERE`. You can also use any of the following switches with this command:

- `-d` or `--dns-check` - Only displays domains with a valid A record. This can makle it less tedious to check if a domain is taken, however it will hide some domains that are being resold.
- `--outfile FILENAME` - Outputs the found domains into a text file. The domains are seperated by newlines. A trailing newline is also outputted.
- `--dictionary LENGTH` - Adds all words the english dictionary up to a certain length as a `-g` argument. **Warning:** Using this argument in combination with `-d` takes a long time.

## Disclaimers
- This script may output domains with TLDs unavailable for purchase. (.test, .google ect.)
- This script is unable to generate domains with TLDs made up of non-ascii characters.