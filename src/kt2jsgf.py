"""
Module for constructing a compact JSGF-format grammar that describes the structures observable in a set of utterances.

:author  GJ Kruijff
:email   gj.kruijff@gmail.com
:version 0.1
:date    July 2 2020
"""

class DataStructure:

    """
    DataStructure provides an in-memory structure for accessing utterance data
    """

    '''Internal structure'''
    L = []


    '''Initialize object'''
    def __init__(self):
        self.L = []

    '''Construct data structure from data stored in a file in flat JSGF format'''
    def readFlatJSGF (self,fn):
        file = open(fn)
        try:
            for line in file:
                self.L.append(line)
        finally:
            file.close()


class KeyWordTree:

    """
    KeyWordTree implements a keyword-tree with links between branches.
    The keyword tree is encoded as a dictionary, using node-IDs as keys, and lists of directed edges as value.
    A directed edge is a structure including a word, and a node-ID

    If the data structure includes a rulename as root (first line), then this is used to set the rootName variable.

    """

    ''' The dictionary used for encoding/storing the keyword tree'''
    D = {}
    ''' The rootname for a dictionary based on a rule name'''
    rootName = ""
    ''' The window size for determining whether to branch off '''
    branchWindow = 1

    ''' Initialize object'''
    def __init__(self):
        self.D = {}
        self.rootName = ""
        self.branchWindow = 1



    """
    Construct the keyword tree from the data structure

    Loop over the lines in the data structure ds,
    then for each line that is an utterance,
    add its words (in sequence) to the keyword tree Dictionary,
    and create a chain by linking word (key) to next word (value)

    """
    def tree(self,ds):
        self.D = {'*START*': []}
        for line in ds.L:
            if (line[0] != "<"):
                wl = list(line.split())
                si = 0
                if (wl[0][0] == '/'): si = 1 # ignore frequency labels for now
                prevWord = "*START*"
                for word in wl[si:]:
                    if (word != "|"):
                        dle = self.D[prevWord]
                        if (word not in dle):
                            dle.append(word)
                        self.D[prevWord] = dle
                        if (word not in self.D):
                            self.D[word] = []
                        prevWord = word

    """
    Construct a compact grammar from this keyword tree
    """

    def tree2grm(self):
        print("Constructing grammar")
        chainGraph = {}
        for word in self.D:
            cls = self.chainLinkSet(word)
            chainGraph[word] = cls
        return chainGraph



    """
    Construct longest non-looping chain

    Recursive function that descends down a keyword tree,
    starting at a word w, constructing a chain of words (nodes)
    accessible from that word (recursively) until an edge
    is encountered that would point to a word already on
    the chain.
    """

    def constructNonLoopingChain(self, w, chain):
        cnt = False
        wl = self.D[w]
        for successor in wl:
            if successor in chain:
                cnt = False
            else:
                cnt = True
                chain.append(successor)
                chain = constructNonLoopingChain(self,successor,chain)
        return (cnt, chain)


    """
    Construct chain link set for a given word

    A chain link set for a word R is a set of tuples (w, W)
    whereby w is in self.D[R] and W = self.D[w]

    """

    def chainLinkSet (self,root):
        cls = []
        wl = self.D[root]
        for w in wl:
            W = self.D[w]
            cls = cls + [(w,W)]
        return cls

    """
    Test utterances against keyword tree

    An utterance passes if we can construct a path from *START* to [] for the entire word list

    The function returns a tuple of a boolean value (True: passes, False: no full path) and the path (list) thru the tree
    """

    def testUttInTree(self, wl):
        parse = []
        pwl = ["*START*"] + wl
        nextKey = ""
        for word in pwl:
            if (word in self.D):
                nextKey = self.D[word]
                parse = parse + [word]
        return (wl == parse[1:], parse)
