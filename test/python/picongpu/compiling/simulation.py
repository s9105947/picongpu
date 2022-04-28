"""
This file is part of the PIConGPU.
Copyright 2021-2022 PIConGPU contributors
Authors: Hannes Tröpgen, Brian Edward Marré
License: GPLv3+
"""

from picongpu import pypicongpu

import unittest


class TestSimulation(unittest.TestCase):
    def test_minimal(self):
        """smallest possible example"""
        sim = pypicongpu.Simulation()
        sim.delta_t_si = 1.39e-16
        sim.time_steps = 1
        sim.grid = pypicongpu.Grid3D()
        sim.grid.cell_size_x_si = 1.776e-07
        sim.grid.cell_size_y_si = 4.43e-08
        sim.grid.cell_size_z_si = 1.776e-07
        sim.grid.cell_cnt_x = 1
        sim.grid.cell_cnt_y = 1
        sim.grid.cell_cnt_z = 1
        sim.grid.boundary_condition_x = \
            pypicongpu.grid.BoundaryCondition.PERIODIC
        sim.grid.boundary_condition_y = \
            pypicongpu.grid.BoundaryCondition.PERIODIC
        sim.grid.boundary_condition_z = \
            pypicongpu.grid.BoundaryCondition.PERIODIC
        sim.laser = None
        sim.solver = pypicongpu.solver.YeeSolver()
        sim.init_manager = pypicongpu.species.InitManager()

        runner = pypicongpu.Runner(sim)
        runner.generate()
        runner.build()
        runner.run()
