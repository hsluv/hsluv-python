import unittest
import json
import os.path

import husl


class TestHusl(unittest.TestCase):

    def setUp(self):
        # Load snapshot into memory
        name = os.path.join(os.path.dirname(__file__), 'snapshot-rev2.json')
        json_data = open(name)
        self.snapshot = json.load(json_data)
        json_data.close()
    
    def test_within_rgb_range(self):
        for H in range(0, 361, 5):
            for S in range(0, 101, 5):
                for L in range(0, 101, 5):
                    RGB = husl.husl_to_rgb(H, S, L)
                    for channel in RGB:
                        assert channel >= -0.00000001 and channel <= 1.00000001
                    RGB = husl.huslp_to_rgb(H, S, L)
                    for channel in RGB:
                        assert channel >= -0.00000001 and channel <= 1.00000001
    
    def test_snapshot(self):
        for hex_color, colors in self.snapshot.items():
            
            # Test forward functions
            test_rgb = husl.hex_to_rgb(hex_color)
            self.assertTuplesClose(test_rgb, colors['rgb'])
            test_xyz = husl.rgb_to_xyz(test_rgb)
            self.assertTuplesClose(test_xyz, colors['xyz'])
            test_luv = husl.xyz_to_luv(test_xyz)
            self.assertTuplesClose(test_luv, colors['luv'])
            test_lch = husl.luv_to_lch(test_luv)
            self.assertTuplesClose(test_lch, colors['lch'])
            test_husl = husl.lch_to_husl(test_lch)
            self.assertTuplesClose(test_husl, colors['husl'])
            test_huslp = husl.lch_to_huslp(test_lch)
            self.assertTuplesClose(test_huslp, colors['huslp'])

            # Test backward functions
            test_lch = husl.husl_to_lch(colors['husl'])
            self.assertTuplesClose(test_lch, colors['lch'])
            test_lch = husl.huslp_to_lch(colors['huslp'])
            self.assertTuplesClose(test_lch, colors['lch'])
            test_luv = husl.lch_to_luv(test_lch)
            self.assertTuplesClose(test_luv, colors['luv'])
            test_xyz = husl.luv_to_xyz(test_luv)
            self.assertTuplesClose(test_xyz, colors['xyz'])
            test_rgb = husl.xyz_to_rgb(test_xyz)
            self.assertTuplesClose(test_rgb, colors['rgb'])
            self.assertEqual(husl.rgb_to_hex(test_rgb), hex_color)

            # Full test
            self.assertEqual(husl.husl_to_hex(*colors['husl']), hex_color)
            self.assertTuplesClose(husl.hex_to_husl(hex_color), colors['husl'])
            self.assertEqual(husl.huslp_to_hex(*colors['huslp']), hex_color)
            self.assertTuplesClose(husl.hex_to_huslp(hex_color), colors['huslp'])

    def assertTuplesClose(self, tup1, tup2):
        for a, b in zip(tup1, tup2):
            if abs(a - b) > 0.00000001:
                raise Exception("Mismatch: {} {}".format(a, b))
    

if __name__ == '__main__':
    unittest.main()
