from picongpu import picmi

import unittest


class TestCartesian3DGrid(unittest.TestCase):

    def setUp(self):
        """default setup"""
        self.grid = picmi.Cartesian3DGrid(
            number_of_cells=[192, 2048, 12],
            lower_bound=[0, 0, 0],
            upper_bound=[3.40992e-5, 9.07264e-5, 2.1312e-6],
            lower_boundary_conditions=['open', 'open', 'periodic'],
            upper_boundary_conditions=['open', 'open', 'periodic'])

    def test_basic(self):
        """simple translation"""
        grid = self.grid
        grid.get_as_pypicongpu()

    def test_typo_ngpus(self):
        """test common typo ngpus instead of n_gpus"""
        with self.assertRaisesRegex(TypeError, "Unexpected keyword argument: \"\[\'ngpus\'\]\""):
            grid = picmi.Cartesian3DGrid(
                number_of_cells=[192, 2048, 12],lower_bound=[0, 0, 0],
                upper_bound=[3.40992e-5, 9.07264e-5, 2.1312e-6],
                lower_boundary_conditions=['open', 'open', 'periodic'],
                upper_boundary_conditions=['open', 'open', 'periodic'],
                ngpus=None) # common typo ngpus instead of n_gpus

    def test_n_gpus_type(self):
        """test wrong input type for n_gpus"""
        for not_ngpus_type in [1, 1., 1.2, "abc", tuple([1])]:
            with self.assertRaisesRegex(TypeError, ".*type of argument \"n_gpus\" must be one of \(List\[int\], NoneType\).*"):
                grid = picmi.Cartesian3DGrid(
                    number_of_cells=[192, 2048, 12],lower_bound=[0, 0, 0],
                    upper_bound=[3.40992e-5, 9.07264e-5, 2.1312e-6],
                    lower_boundary_conditions=['open', 'open', 'periodic'],
                    upper_boundary_conditions=['open', 'open', 'periodic'],
                    n_gpus=not_ngpus_type)

    def test_n_gpus_asserts(self):
        """test too many GPUs for grid"""
        for not_ngpus_dist in [[1,1,2], [5,1,1], [1,512,1]]:
            with self.assertRaisesRegex(Exception, ".*GPU- and/or super-cell-distribution.*"):
                grid = picmi.Cartesian3DGrid(
                    number_of_cells=[192, 2048, 12],lower_bound=[0, 0, 0],
                    upper_bound=[3.40992e-5, 9.07264e-5, 2.1312e-6],
                    lower_boundary_conditions=['open', 'open', 'periodic'],
                    upper_boundary_conditions=['open', 'open', 'periodic'],
                    n_gpus=not_ngpus_dist)
                grid.get_as_pypicongpu()

    def test_n_gpus_wrong_numbers(self):
        """test negativ numbers or zero as number of gpus"""
        for not_ngpus_dist in [[0], [1,1,0], [-1], [-1,1,1], [-7]]:
            with self.assertRaisesRegex(Exception, ".*number of gpus must be positive integer.*"):
                grid = picmi.Cartesian3DGrid(
                    number_of_cells=[192, 2048, 12],lower_bound=[0, 0, 0],
                    upper_bound=[3.40992e-5, 9.07264e-5, 2.1312e-6],
                    lower_boundary_conditions=['open', 'open', 'periodic'],
                    upper_boundary_conditions=['open', 'open', 'periodic'],
                    n_gpus=not_ngpus_dist)
                grid.get_as_pypicongpu()
