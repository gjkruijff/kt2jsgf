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

    D = {}
    rootName = ""

    ''' Initialize object'''
    def __init__(self):
        self.D = {}
        self.rootName = ""


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
                            # cycle over vertices and check whether word is present, else add vertex
                            for vertex in vl:
                                if vertex[0] == word:
                                    # set i to the kwt node index pointed to
                                    i = vertex[1]
                                else:
                                    # word not found, so add vertex, point to next position
                                    vertex = (word,i+1)
                                    vl.append(vertex)
                                    self.D[i] = vl
                                    i = i +1
                        else:
                            # there is no list of vertices at this position, so initialize one with new vertex
                            vertex = (word, i+1)
                            vl.append(vertex)
                            self.D[i] = vl
                            i = i +1
