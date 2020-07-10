import unittest
#from importer import read_csv
target = __import__("importer.py")

class ImporterTest(unittest.TestCase):

    def test_csv_invalid_file(self):
        self.assertIsNone(target.read_csv('invalid-file.csv'))

if __name__ == '__main__':
    unittest.main()
