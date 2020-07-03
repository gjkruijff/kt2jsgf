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
            #elif (line.index('|') > -1):
            #    # ignore this line
            #    pass
            else:
                # create a word list from the utterance
                wl = list(line.split())
                si = 0
                if (wl[0][0] == '/'): si = 1
                # initialize the dictionary and word indices
                wi = 0  # word index in the word list for the utterance
                di = 0  # dictionary index in D
                # iterate over the words in the word list
                for word in wl[si:]:
                    print("wi, di, bfi", wi)
                    if (word != "|"):
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
                            # if just before frontier, continue trunk, shift di and bfi rightwards
                            if (di+1 == bfi):
                                dirNode = (word, di+1)
                                dle.append(dirNode)
                                self.D[di] = dle
                                di =+ 1
                                bfi =+ 1
                                wi =+ 1
                            # if within trunk, branch test given branching window
                            else:
                                wordWindow = wl[wi+1:wi+1+self.branchWindow]
                                contBranch = self.checkBranchingWindow(di,wordWindow)
                                if (contBranch == True):
                                    # extend
                                    dirNode = (word,di+1)
                                    dle.append(dirNode)
                                    self.D[di] = dle
                                    di =+ 1
                                    bfi =+ 1
                                    wi =+ 1
                                else:
                                    dirNode = (word, bfi)
                                    dle.append(dirNode)
                                    self.D[di] = dle
                                    di = bfi
                                    bfi =+ 1
                                    wi =+ 1
                        else:
                            di =+ 1
                            bfi =+ 1
                            wi =+ 1


    """
    The function checkBranchingWindow returns a boolean indicating
    whether the words in the word window list ww appear in that sequence
    in the keyword tree, from the current keyword tree dictionary index di
    """
    def checkBranchingWindow (self, di, wordWindow):
        foundInWindow = True
        i = 1 # di offset into word window
        for ww in wordWindow:
            if (foundInWindow):
                if di+i in self.D:
                    nxtDle = self.D[di+i]
                    wfnd = False
                    for le in nxtDle:
                         if (le[0] == word):
                             wfnd = True
                    if (wfnd == True):
                        i =+ 1 # shift index right
                        # WARNING! in principle di should be updated to follow edge!!
                    else:
                        foundInWindow = False
                else:
                    foundInWindow = False
        return foundInWindow
