import sys
import marshal
import csv
from datetime import datetime
from subprocess import Popen, PIPE

def preprocess_fields(record):
    for datefield in ['Update', 'Access']:
        if record[datefield]:
            record[datefield] = datetime.fromtimestamp(int(record[datefield]))

# Run p4 passing in the option for marshalled python output
# and then the rest of the command line arguments
pipe = Popen(["p4", "-G"] + sys.argv[1:], stdout=PIPE).stdout

records = []
try:
    while 1:
        record = marshal.load(pipe)
        preprocess_fields(record)
        records.append(record)
except EOFError:
    pass

pipe.close()

# convert stdout to binary for windows
if sys.platform == "win32":
    import os, msvcrt
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

# output records as CSV
fields = set().union(*records)
output = csv.DictWriter(sys.stdout, fields)
output.writeheader()
for record in records:
    output.writerow(record)
