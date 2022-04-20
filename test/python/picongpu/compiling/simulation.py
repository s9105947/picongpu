import picongpu.pypicongpu

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
        sim.grid.boundary_condition_x = pypicongpu.BoundaryCondition.PERIODIC
        sim.grid.boundary_condition_y = pypicongpu.BoundaryCondition.PERIODIC
        sim.grid.boundary_condition_z = pypicongpu.BoundaryCondition.PERIODIC
        sim.laser = None
        sim.solver = pypicongpu.YeeSolver()
        sim.species = []

        runner = pypicongpu.Runner(sim)
        runner.generate()
        runner.build()
        runner.run()
