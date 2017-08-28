This is a README file.

----------------------------------------
Python 3.6 is used

execute this command install dependencies:
pip3 install -r requirements.txt

File to parse has to be in "PROJECT_ROOT\resources\" folder

usage: bin.run-parser.py [-h] [-f file] [-l]

Parse arguments

optional arguments:
  -h, --help            show this help message and exit
  -f file, --file file  log "file" to parse
  -l, --list-files      show list of files available to parse

Example:
---------------
## Print out list of log files in ~/resources folder (only these files can be parsed):
python -m bin.run-parser.py -l

## Run log parser for a specific file
python -m bin.run-parser.py -f E:\ProjectsPyCharm\LogParser\resources\gobankingrates.com.access.log