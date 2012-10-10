import unittest
from husl import HuslConverter

class TestHusl(unittest.TestCase):

    def test_random(self):
        conv = HuslConverter()
        rgb = conv.rgbPrepare(conv.HUSLtoRGB(200, 80, 50))
        self.assertEqual(rgb, [55.0, 130.0, 135.0])

if __name__ == '__main__':
    unittest.main()