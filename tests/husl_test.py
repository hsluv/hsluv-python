import unittest
import json
import os.path

import husl

class TestHusl(unittest.TestCase):

    def setUp(self):
        # Load snapshot into memory
        name = os.path.join(os.path.dirname(__file__), 'snapshot-2.x.x.json')
        json_data = open(name)
        self.snapshot = json.load(json_data)
        json_data.close()

    def test_snapshot(self):
        for h in range(37):
            for s in range(21):
                for l in range(21):
                    H = h * 10.0
                    S = s * 5.0
                    L = l * 5.0

                    test = husl.husl_to_hex(H, S, L)
                    correct = self.snapshot['husl'][h][s][l]
                    self.assertEqual(test, correct)
                    test2 = husl.husl_to_hex(*husl.hex_to_husl(correct))
                    self.assertEqual(test2, correct)

                    test = husl.huslp_to_hex(H, S, L)
                    correct = self.snapshot['huslp'][h][s][l]
                    self.assertEqual(test, correct)
                    test2 = husl.huslp_to_hex(*husl.hex_to_huslp(correct))
                    self.assertEqual(test2, correct)

if __name__ == '__main__':
    unittest.main()