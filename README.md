This is a README file.

----------------------------------------
Python 3.6 is used

execute this command install dependencies:
pip3 install -r requirements.txt

There is sleep command while executing api call to map ip address to geo data. The reason is "http://ip-api.com/" will
ban ip address with more than 150 requests a min. You can comment line 21 in lib/log-parser.py to make code faster.

File to parse has to be in "PROJECT_ROOT/resources/" folder

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
python -m bin.run-parser.py -f E:/ProjectsPyCharm/LogParser/resources/less_gobankingrates.com.access.log
python -m bin.run-parser.py -f E:/ProjectsPyCharm/LogParser/resources/500_gobankingrates.com.access.log