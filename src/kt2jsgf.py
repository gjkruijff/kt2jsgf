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

    ''' Construct the object from a data structure'''
    def construct(self,ds):
        self.D = {}
        for line in ds.L:
            if (line[0] == '<'):
                self.rootName = line[1:line.index('>')]
            else:
                # create word list from line
                wl = list(line.split())
                # initialize word and split index
                i = 0
                si = 0
                # check whether first item is a frequency label of the form /f/; frequency is ignored right now
                if (wl[0][0] == '/'): si = 1




                # iterate over the words in the word list
                for word in wl[si:]:
                    if word != "|":
                        # initialize vertex list
                        vl = []
                        # check whether position exists in KWT dictionary and retrieve vertex list. if not, create
                        if i in self.D:
                            vl = self.D[i]
                        else:
                            self.D[i] = vl
                        # check whether the word is included in a non-empty vertex list
                        if len(vl) > 0:
                            found = False
                            for vertex in vl:
                                if vertex[0] == word:
                                    found = True
                                    # set i to the kwt node index pointed to
                                    i = vertex[1]
                            if found != True:
                                # check whether to branch; this determines the pointed-to index



                                # add vertex
                                vertex = (word,i+1)
                                print("Not found in VL so adding ",vertex)
                                vl.append(vertex)
                                self.D[i] = vl
                                i = i +1
                        else:
                            vertex = (word, i+1)
                            vl.append(vertex)
                            print("Zero VL adding ",vertex)
                            self.D[i] = vl
                            i = i +1


    """
    Construct a keyword tree from the data structure

    Loop over the lines in the data structure ds,
    then for each line that is an utterance,
    add its words (in sequence) to the keyword tree Dictionary.

    A new branch is created when the next word in the utterance,
    is not covered in the list of directed labeled edges at the next position in the dictionary.
    A branch is then added from the branch frontier index onwards.

    """
    def tree(self,ds):
        self.D = {}
        bfi = 1 # branch frontier index
        # Cycle over the lines in the data structure ds
        for line in ds.L:
            # if it is the rule name, set the root name for the tree
            if (line[0] == '<'):
                self.rootName = line[1:line.index('>')]
            else if (line.index('|') > -1):
                # ignore this line
                pass
            else:
                # create a word list from the utterance
                wl = list(line.split())
                # initialize the dictionary and word indices
                wi = 0  # word index in the word list for the utterance
                di = 0  # dictionary index in D
                # iterate over the words in the word list
                for word in wl:
                    dle = []
                    # check whether there is a directed labeled edge list dnl at di, else initialize new
                    if di in self.D:
                        dle = self.D[di]
                    else:
                        self.D[di] = dle
                    # check whether word is in dle
                    fnd = False
                    for labeledEdge in dle:
                        if (labeledEdge[0] == word):
                              fnd = True
                              di = labeledEdge[1] # set the dictionary index following the edge
                    # if not found, added new directed edge -- with branch check
                    if (fnd != True):
                        
