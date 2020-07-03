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
