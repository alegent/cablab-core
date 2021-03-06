import os
import unittest
from datetime import datetime

from cablab import CubeConfig
from cablab.providers.burnt_area import BurntAreaProvider
from test.providers.provider_test_utils import ProviderTestBase
from cablab.util import Config

SOURCE_DIR = Config.instance().get_cube_source_path('BurntArea')


class BurntAreaProviderTest(ProviderTestBase):
    @unittest.skipIf(not os.path.exists(SOURCE_DIR), 'test data not found: ' + SOURCE_DIR)
    def test_source_time_ranges(self):
        provider = BurntAreaProvider(CubeConfig(), dir=SOURCE_DIR)
        provider.prepare()
        source_time_ranges = provider.source_time_ranges
        self.assertEqual(225, len(source_time_ranges))
        self.assert_source_time_ranges(source_time_ranges[0],
                                       datetime(1995, 1, 6, 0, 0),
                                       datetime(1995, 2, 6, 0, 0),
                                       self.get_source_dir_list(SOURCE_DIR) + ['BurntArea.GFED4.1995.nc.gz'],
                                       0)
        self.assert_source_time_ranges(source_time_ranges[1],
                                       datetime(1995, 2, 6, 0, 0),
                                       datetime(1995, 3, 6, 0, 0),
                                       self.get_source_dir_list(SOURCE_DIR) + ['BurntArea.GFED4.1995.nc.gz'],
                                       1)
        self.assert_source_time_ranges(source_time_ranges[6],
                                       datetime(1995, 7, 6, 0, 0),
                                       datetime(1995, 8, 6, 0, 0),
                                       self.get_source_dir_list(SOURCE_DIR) + ['BurntArea.GFED4.1995.nc.gz'],
                                       6)
        self.assert_source_time_ranges(source_time_ranges[224],
                                       datetime(2014, 2, 1, 0, 0),
                                       datetime(2014, 3, 1, 0, 0),
                                       self.get_source_dir_list(SOURCE_DIR) + ['BurntArea.GFED4.2014.nc.gz'],
                                       1)

    @unittest.skipIf(not os.path.exists(SOURCE_DIR), 'test data not found: ' + SOURCE_DIR)
    def test_temporal_coverage(self):
        provider = BurntAreaProvider(CubeConfig(), dir=SOURCE_DIR)
        provider.prepare()
        temporal_coverage = provider.temporal_coverage
        self.assertEqual((datetime(1995, 1, 6, 0, 0),
                          datetime(2014, 3, 1, 0, 0)),
                         temporal_coverage)

    @unittest.skipIf(not os.path.exists(SOURCE_DIR), 'test data not found: ' + SOURCE_DIR)
    def test_get_images(self):
        provider = BurntAreaProvider(CubeConfig(), dir=SOURCE_DIR)
        provider.prepare()
        images = provider.compute_variable_images(datetime(1996, 1, 1), datetime(1996, 1, 9))
        self.assertIsNotNone(images)
        self.assertTrue('burnt_area' in images)
        image = images['burnt_area']
        self.assertEqual((720, 1440), image.shape)

    @unittest.skipIf(not os.path.exists(SOURCE_DIR), 'test data not found: ' + SOURCE_DIR)
    def test_get_high_res_images(self):
        provider = BurntAreaProvider(CubeConfig(grid_width=4320, grid_height=2160, spatial_res=1 / 12), dir=SOURCE_DIR)
        provider.prepare()
        images = provider.compute_variable_images(datetime(1996, 1, 1), datetime(1996, 1, 9))
        self.assertIsNotNone(images)
        self.assertTrue('burnt_area' in images)
        image = images['burnt_area']
        self.assertEqual((2160, 4320), image.shape)
