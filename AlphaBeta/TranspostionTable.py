from AlphaBeta import HashEntry
#import HashEntry

class TranspostionTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * (1 << self.size)
        #self.table = [None] * (2**32)

    def storeEntry(self, entry: HashEntry.HashEntry):
        hash = entry.getHash()
        index = abs(hash % (1 << self.size))
        #index = abs(hash % (2**32))
        self.table[index] = entry

    def probeEntry(self, hash) -> HashEntry.HashEntry:
        index = abs(hash % (1 << self.size))
        #index = abs(hash % (2**32))
        result = self.table[index]
        return result

if __name__ == '__main__':
    table = TranspostionTable()
    entry = HashEntry.HashEntry(12234, 2, 4)
    table.storeEntry(entry)
    tableentry = table.probeEntry(12234)
    if tableentry != None:
        print(tableentry.Hash)
    tableentry = table.probeEntry(1234)
    if tableentry != None:
        print(tableentry.Hash)
    else:
        print("Hello")
