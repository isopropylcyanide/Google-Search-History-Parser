"""
Python program to view the relevant google searches along with the timestamp
from the vast, verbose and convoluted json that google archive provides.
Author : Aman Garg
"""

import os
import json
import time


class query:
    """A google query is a piece of text along with its timestamp"""

    def __init__(self, text, timestamp):
        self.text = text
        self.timestamp = timestamp

    def __repr__(self):
        return '%s : %s' % (self.timestamp, self.text.encode('utf-8'))


def epochToReadable(timestamp):
    """Convert an epoch timestamp in usec to human readable"""
    timestamp = float(timestamp)
    return time.strftime("%Z - %Y/%m/%d, %H:%M:%S",
                         time.localtime(timestamp / pow(10, 6)))


def parseArchive():
    """Parses all json files in the extacted archive and creates an out file"""

    allQueries = []

    def generateFiles():
        """Return the json files in the current directory"""
        files = [f for f in os.listdir(
            '.') if os.path.isfile(f) and f.endswith('.json')]
        files.sort()
        return files

    for my_json in generateFiles():
        with open(my_json) as f:
            j_data = json.load(f)

        for i in j_data['event']:
            text = i['query']['query_text']
            time_s = i['query']['id'][0]['timestamp_usec']
            new_query = query(text, epochToReadable(time_s))
            allQueries.append(new_query)

    return allQueries


def writeResultToFile(results, filename='all_searches.txt'):
    """Writes google results to file"""
    with open(filename, 'w') as f:
        for query in results:
            f.writelines(query.__repr__() + '\n')

if __name__ == '__main__':
    writeResultToFile(parseArchive())
