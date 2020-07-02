import unittest
import kt2jsgf

"""
Unit tests for kt2jsgf package
"""

class TestDataStructure(unittest.TestCase):

    def test_DataStructure_object(self):
        '''As a developer, I can construct a data structure object'''
        ds = kt2jsgf.DataStructure()
        self.assertEqual(len(ds.L),0)

    def test_DataStructure_constructFromFile(self):
        '''As a developer, I can construct a data structure object from a file'''
        ds = kt2jsgf.DataStructure()
        filename = "../data/frequtts.txt"
        ds.readFlatJSGF(filename)
        self.assertEqual(len(ds.L),45)



class TestKeyWordTree(unittest.TestCase):

    def test_KeyWordTree_object(self):
        '''As a developer, I can construct a keyword tree object'''
        kwt = kt2jsgf.KeyWordTree()
        self.assertEqual(len(kwt.D),0)

    def test_KeyWordTree_constructionOneUtterance(self):
        '''As a developer, I can construct a keyword tree object from a data structure with 1 utterance'''
        kwt = kt2jsgf.KeyWordTree()
        ds = kt2jsgf.DataStructure()
        filename = "../data/ruleoneutt.jsgf"
        ds.readFlatJSGF(filename)
        self.assertEqual(len(ds.L),2)
        kwt.construct(ds)
        #print("KWT dictionary:", kwt.D)
        self.assertEqual(len(kwt.D),8)

    def test_KeyWordTree_constructionTwoUtterance(self):
        '''As a developer, I can construct a keyword tree object from a data structure with 2 utterances'''
        kwt = kt2jsgf.KeyWordTree()
        ds = kt2jsgf.DataStructure()
        filename = "../data/ruletwoutt.jsgf"
        ds.readFlatJSGF(filename)
        self.assertEqual(len(ds.L),4)
        kwt.construct(ds)
        print("KWT dictionary:", kwt.D)
        self.assertEqual(len(kwt.D),8)

    def test_KeyWordTree_constructionThreeUtterance(self):
        '''As a developer, I can construct a keyword tree object from a data structure with 3 utterances'''
        kwt = kt2jsgf.KeyWordTree()
        ds = kt2jsgf.DataStructure()
        filename = "../data/rulethreeutt.jsgf"
        ds.readFlatJSGF(filename)
        self.assertEqual(len(ds.L),6)
        kwt.constructTree(ds)
        print("KWT dictionary:", kwt.D)
        self.assertEqual(len(kwt.D),9)





if __name__ == '__main__':
    unittest.main()
