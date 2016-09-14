import glob
import os

import gridtools.resampling as gtr
import netCDF4
import numpy as np

from cablab import BaseStaticCubeSourceProvider
from cablab.util import Config


class WaterMaskProvider(BaseStaticCubeSourceProvider):
    def __init__(self, cube_config, name='water_mask', dir=None):
        super(WaterMaskProvider, self).__init__(cube_config, name)
        if dir is None:
            raise ValueError('dir_path expected')
        if not os.path.isabs(dir):
            self._dir_path = Config.instance().get_cube_source_path(dir)
        else:
            self._dir_path = dir
        self.cube_config.static_data = True

    @property
    def variable_descriptors(self):
        return {
            'water_mask': {
                'source_name': 'wb_class',
                'data_type': np.byte,
                'fill_value': 0,
                'units': '-',
                'standard_name': 'land_cover_lccs',
                'long_name': 'terrestrial or water pixel classification',
            }
        }

    @property
    def dir_path(self):
        return self._dir_path

    def get_dataset_file_path(self, dataset):
        return dataset.filepath

    def open_dataset(self):
        file_paths = glob.glob(os.path.join(self._dir_path, '*.nc'))
        if not file_paths:
            raise ValueError('No *.nc file found in %s' % self._dir_path)
        file = file_paths[0]
        return netCDF4.Dataset(file)

    def get_dataset_image(self, dataset, var_name):
        variable = dataset.variables[var_name]
        if len(variable.shape) == 3:
            var_image = variable[0, :, :]
        elif len(variable.shape) == 2:
            var_image = np.empty((self.cube_config.grid_height, self.cube_config.grid_width))
            chunk_size = 180
            x_index = 1
            y_index = 1
            x_start = 0
            y_start = 0
            x_max = 259200
            y_max = 129600
            while (y_index * chunk_size) < y_max:
                while (x_index * chunk_size) < x_max:
                    chunked = variable[y_start + ((y_index - 1) * chunk_size):(y_index * chunk_size),
                              x_start + ((x_index - 1) * chunk_size):(x_index * chunk_size)]
                    print((x_start + ((x_index - 1) * chunk_size), (x_index * chunk_size)))
                    print((y_start, (y_index * chunk_size)))
                    print((y_index, x_index))
                    var_image[y_index, x_index] = gtr.resample_2d(chunked.astype(float), 1, 1)
                    # gtr.resample_2d(chunked.astype(float), 180, 180)
                    x_index += 1
                y_index += 1
                x_index = 1
        else:
            raise ValueError("unexpected shape for variable '%s'" % var_name)
        return var_image

    def close_dataset(self, dataset):
        dataset.close()
