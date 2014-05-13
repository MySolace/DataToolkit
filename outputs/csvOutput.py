import csv
import collections
from ctloutput import CTLOutput

class csvOutput(CTLOutput):
    path = './csv/'

    def output(self, data):
        outfile = open(self.path + self.name + '.csv', 'wb')
        writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
        for row in data:
            for newrow in self.flatten(row):
                writer.writerow(newrow)

    '''
    For now, this accepts an array in the format:
    [idx, [['key', value], ['key', value]]]
    '''
    def flatten(self, row):
        baseArray = [row[0]]
        returnArrays = []
        for subarray in row[1]:
            newArray = baseArray[:]
            newArray.extend(subarray)
            returnArrays.append(newArray)
        return returnArrays

    def setPath(self, path):
        self.path = path