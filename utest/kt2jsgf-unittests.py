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

    def test_KeyWordTree_construction(self):
        '''As a developer, I can construct a keyword tree object from a data structure'''
        kwt = kt2jsgf.KeyWordTree()
        ds = kt2jsgf.DataStructure()
        filename = "../data/ruleoneutt.jsgf"
        ds.readFlatJSGF(filename)
        self.assertEqual(len(ds.L),2)
        kwt.construct(ds)
        #print("Root name: "+kwt.rootName)



if __name__ == '__main__':
    unittest.main()
