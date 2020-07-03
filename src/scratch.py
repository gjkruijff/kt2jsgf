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
