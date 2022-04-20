from picongpu.pypicongpu.grid import Grid3D, BoundaryCondition

import unittest


class TestGrid3D(unittest.TestCase):
    def setUp(self):
        self.g = Grid3D()
        self.g.cell_size_x_si = 1.2
        self.g.cell_size_y_si = 2.3
        self.g.cell_size_z_si = 4.5
        self.g.cell_cnt_x = 6
        self.g.cell_cnt_y = 7
        self.g.cell_cnt_z = 8
        self.g.boundary_condition_x = BoundaryCondition.PERIODIC
        self.g.boundary_condition_y = BoundaryCondition.ABSORBING
        self.g.boundary_condition_z = BoundaryCondition.PERIODIC

    def test_basic(self):
        g = self.g
        self.assertEqual(1.2, g.cell_size_x_si)
        self.assertEqual(2.3, g.cell_size_y_si)
        self.assertEqual(4.5, g.cell_size_z_si)
        self.assertEqual(6, g.cell_cnt_x)
        self.assertEqual(7, g.cell_cnt_y)
        self.assertEqual(8, g.cell_cnt_z)
        self.assertEqual(BoundaryCondition.PERIODIC, g.boundary_condition_x)
        self.assertEqual(BoundaryCondition.ABSORBING, g.boundary_condition_y)
        self.assertEqual(BoundaryCondition.PERIODIC, g.boundary_condition_z)

    def test_types(self):
        g = self.g
        with self.assertRaises(TypeError):
            g.cell_size_x_si = "54.3"
        with self.assertRaises(TypeError):
            g.cell_size_y_si = "2"
        with self.assertRaises(TypeError):
            g.cell_size_z_si = "126"
        with self.assertRaises(TypeError):
            g.cell_cnt_x = 11.1
        with self.assertRaises(TypeError):
            g.cell_cnt_y = 11.412
        with self.assertRaises(TypeError):
            g.cell_cnt_z = 16781123173.12637183
        with self.assertRaises(TypeError):
            g.boundary_condition_x = "open"
        with self.assertRaises(TypeError):
            g.boundary_condition_y = 1
        with self.assertRaises(TypeError):
            g.boundary_condition_z = {}

    def test_mandatory(self):
        # check that mandatory arguments can't be none
        g = self.g
        with self.assertRaises(TypeError):
            g.cell_size_x_si = None
        with self.assertRaises(TypeError):
            g.cell_size_y_si = None
        with self.assertRaises(TypeError):
            g.cell_size_z_si = None
        with self.assertRaises(TypeError):
            g.cell_cnt_x = None
        with self.assertRaises(TypeError):
            g.cell_cnt_y = None
        with self.assertRaises(TypeError):
            g.cell_cnt_x = None
        with self.assertRaises(TypeError):
            g.boundary_condition_x = None
        with self.assertRaises(TypeError):
            g.boundary_condition_y = None
        with self.assertRaises(TypeError):
            g.boundary_condition_z = None

    def test_get_rendering_context(self):
        """object is correctly serialized"""
        # automatically checks against schema
        context = self.g.get_rendering_context()
        self.assertEqual(1.2, context["cell_size"]["x"])
        self.assertEqual(2.3, context["cell_size"]["y"])
        self.assertEqual(4.5, context["cell_size"]["z"])
        self.assertEqual(6, context["cell_cnt"]["x"])
        self.assertEqual(7, context["cell_cnt"]["y"])
        self.assertEqual(8, context["cell_cnt"]["z"])

        # boundary condition translated to numbers for cfgfiles
        self.assertEqual("1", context["boundary_condition"]["x"])
        self.assertEqual("0", context["boundary_condition"]["y"])
        self.assertEqual("1", context["boundary_condition"]["z"])


class TestBoundaryCondition(unittest.TestCase):
    def test_cfg_translation(self):
        p = BoundaryCondition.PERIODIC
        a = BoundaryCondition.ABSORBING
        self.assertEqual("0", a.get_cfg_str())
        self.assertEqual("1", p.get_cfg_str())
