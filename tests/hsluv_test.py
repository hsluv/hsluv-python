import unittest
import json
import os.path

from hsluv import (
    hex_to_rgb, rgb_to_hex, hex_to_hsluv, hex_to_hpluv, hpluv_to_hex,
    rgb_to_xyz, xyz_to_rgb, hsluv_to_rgb, hpluv_to_rgb, hsluv_to_hex,
    luv_to_xyz, luv_to_lch, lch_to_hsluv, hsluv_to_lch, lch_to_hpluv,
    xyz_to_luv, lch_to_luv, hpluv_to_lch
)
from itertools import product


rgb_range_tolerance = 1e-11
snapshot_tolerance = 1e-11


class TestHusl(unittest.TestCase):
    def setUp(self):
        # Load snapshot into memory
        name = os.path.join(os.path.dirname(__file__), 'snapshot-rev4.json')
        json_data = open(name)
        self.snapshot = json.load(json_data)
        json_data.close()

    def test_within_rgb_range(self):
        ranges = range(0, 361, 5), range(0, 101, 5), range(0, 101, 5)

        for h, s, l in product(*ranges):
            for func in [hsluv_to_rgb, hpluv_to_rgb]:
                hsl = h, s, l
                rgb = func(hsl)
                for channel in rgb:
                    self.assertLessEqual(-rgb_range_tolerance, channel)
                    self.assertLessEqual(channel, 1+rgb_range_tolerance)

    def test_snapshot(self):
        for hex_color, colors in self.snapshot.items():
            # Test forward functions
            test_rgb = hex_to_rgb(hex_color)
            self.assert_tuples_close(test_rgb, colors['rgb'])
            test_xyz = rgb_to_xyz(test_rgb)
            self.assert_tuples_close(test_xyz, colors['xyz'])
            test_luv = xyz_to_luv(test_xyz)
            self.assert_tuples_close(test_luv, colors['luv'])
            test_lch = luv_to_lch(test_luv)
            self.assert_tuples_close(test_lch, colors['lch'])
            test_hsluv = lch_to_hsluv(test_lch)
            self.assert_tuples_close(test_hsluv, colors['hsluv'])
            test_hpluv = lch_to_hpluv(test_lch)
            self.assert_tuples_close(test_hpluv, colors['hpluv'])

            # Test backward functions
            test_lch = hsluv_to_lch(colors['hsluv'])
            self.assert_tuples_close(test_lch, colors['lch'])
            test_lch = hpluv_to_lch(colors['hpluv'])
            self.assert_tuples_close(test_lch, colors['lch'])
            test_luv = lch_to_luv(test_lch)
            self.assert_tuples_close(test_luv, colors['luv'])
            test_xyz = luv_to_xyz(test_luv)
            self.assert_tuples_close(test_xyz, colors['xyz'])
            test_rgb = xyz_to_rgb(test_xyz)
            self.assert_tuples_close(test_rgb, colors['rgb'])
            self.assertEqual(rgb_to_hex(test_rgb), hex_color)

            # Full test
            self.assertEqual(hsluv_to_hex(colors['hsluv']), hex_color)
            self.assert_tuples_close(hex_to_hsluv(hex_color), colors['hsluv'])
            self.assertEqual(hpluv_to_hex(colors['hpluv']), hex_color)
            self.assert_tuples_close(hex_to_hpluv(hex_color), colors['hpluv'])

    def assert_tuples_close(self, tup1, tup2):
        for a, b in zip(tup1, tup2):
            if abs(a - b) > snapshot_tolerance:
                raise Exception("Mismatch: {} {}".format(a, b))


if __name__ == '__main__':
    unittest.main()
