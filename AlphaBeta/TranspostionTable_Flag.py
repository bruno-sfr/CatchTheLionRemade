from . import HashEntry_Flag
#import HashEntry_Flag
from . import AB_Flag
#import AB_Flag
#import HashEntry

class TranspostionTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * (1 << self.size)
        #self.table = [None] * (2**32)

    def storeEntry(self, entry: HashEntry_Flag.HashEntry):
        hash = entry.getHash()
        index = abs(hash % (1 << self.size))
        #index = abs(hash % (2**32))
        self.table[index] = entry

    def probeEntry(self, hash) -> HashEntry_Flag.HashEntry:
        index = abs(hash % (1 << self.size))
        #index = abs(hash % (2**32))
        result = self.table[index]
        return result

if __name__ == '__main__':
    table = TranspostionTable()
    Flag = AB_Flag.Flag.EXACT
    entry = HashEntry_Flag.HashEntry(12234, 2, 4, AB_Flag.Flag.EXACT)
    table.storeEntry(entry)
    tableentry = table.probeEntry(12234)
    if tableentry != None:
        print(tableentry.Hash)
    tableentry = table.probeEntry(1234)
    if tableentry != None:
        print(tableentry.Hash)
    else:
        print("Hello")
