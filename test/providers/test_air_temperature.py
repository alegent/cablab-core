import os
import unittest
from datetime import datetime

from cablab import CubeConfig
from cablab.providers.air_temperature import AirTemperatureProvider
from test.providers.provider_test_utils import ProviderTestBase
from cablab.util import Config

SOURCE_DIR = Config.instance().get_cube_source_path("T2m-ECMWF/low/")


class AirTemperatureProviderTest(ProviderTestBase):
    @unittest.skipIf(not os.path.exists(SOURCE_DIR), 'test data not found: ' + SOURCE_DIR)
    def test_source_time_ranges(self):
        provider = AirTemperatureProvider(CubeConfig(end_time=datetime(2001, 12, 31, 23, 0)), dir=SOURCE_DIR)
        provider.prepare()
        source_time_ranges = provider.source_time_ranges
        self.assertEqual(730, len(source_time_ranges))
        self.assert_source_time_ranges(source_time_ranges[0],
                                       datetime(2001, 1, 1, 0, 0),
                                       datetime(2001, 1, 1, 12, 0),
                                       self.get_source_dir_list(SOURCE_DIR) + ['t2m_2001_01.nc'],
                                       0)
        self.assert_source_time_ranges(source_time_ranges[6],
                                       datetime(2001, 1, 4, 0, 0),
                                       datetime(2001, 1, 4, 12, 0),
                                       self.get_source_dir_list(SOURCE_DIR) + ['t2m_2001_01.nc'],
                                       6)
        self.assert_source_time_ranges(source_time_ranges[729],
                                       datetime(2001, 12, 31, 12, 0),
                                       datetime(2002, 1, 1, 0, 0),
                                       self.get_source_dir_list(SOURCE_DIR) + ['t2m_2001_12.nc'],
                                       61)

    @unittest.skipIf(not os.path.exists(SOURCE_DIR), 'test data not found: ' + SOURCE_DIR)
    def test_temporal_coverage(self):
        provider = AirTemperatureProvider(CubeConfig(end_time=datetime(2001, 12, 31, 23, 0)), dir=SOURCE_DIR)
        provider.prepare()
        self.assertEqual((datetime(2001, 1, 1, 0, 0), datetime(2002, 1, 1, 0, 0)),
                         provider.temporal_coverage)

    @unittest.skipIf(not os.path.exists(SOURCE_DIR), 'test data not found: ' + SOURCE_DIR)
    def test_get_images(self):
        provider = AirTemperatureProvider(CubeConfig(end_time=datetime(2001, 6, 1, 0, 0)), dir=SOURCE_DIR,
                                          resampling_order="space_first")
        provider.prepare()
        images = provider.compute_variable_images(datetime(2001, 1, 1), datetime(2001, 1, 9))
        self.assertIsNotNone(images)
        self.assertTrue('air_temperature_2m' in images)
        image = images['air_temperature_2m']
        self.assertEqual((720, 1440), image.shape)

    @unittest.skipIf(not os.path.exists(SOURCE_DIR), 'test data not found: ' + SOURCE_DIR)
    def test_get_high_res_images(self):
        provider = AirTemperatureProvider(CubeConfig(grid_width=4320, grid_height=2160, spatial_res=1 / 12,
                                                     end_time=datetime(2001, 6, 1, 0, 0)), dir=SOURCE_DIR)
        provider.prepare()
        images = provider.compute_variable_images(datetime(2001, 1, 1), datetime(2001, 1, 9))
        self.assertIsNotNone(images)
        self.assertTrue('air_temperature_2m' in images)
        image = images['air_temperature_2m']
        self.assertEqual((2160, 4320), image.shape)
