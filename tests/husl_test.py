import unittest
import json
import os.path

from husl import HuslConverter

class TestHusl(unittest.TestCase):

    def setUp(self):
        # Load snapshot into memory
        name = os.path.join(os.path.dirname(__file__), 'snapshot-2.x.x.json')
        json_data = open(name)
        self.snapshot = json.load(json_data)
        json_data.close()

    def test_snapshot(self):
        conv = HuslConverter()
        for h in range(37):
            for s in range(21):
                for l in range(21):
                    print h, s, l
                    test = conv.HUSLtoHex(h * 10.0, s * 5.0, l * 5.0)
                    correct = self.snapshot['husl'][h][s][l]
                    self.assertEqual(test, correct)

if __name__ == '__main__':
    unittest.main()