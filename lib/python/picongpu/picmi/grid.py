"""
This file is part of the PIConGPU.
Copyright 2021-2022 PIConGPU contributors
Authors: Hannes Tröpgen, Brian Edward Marré
License: GPLv3+
"""

from ..pypicongpu import grid
from ..pypicongpu import util

import picmistandard
from typeguard import typechecked
import typing


@typechecked
class Cartesian3DGrid(picmistandard.PICMI_Cartesian3DGrid):
    def __init__(self, n_gpus: typing.Optional[typing.List[int]] = None, *kw):
        """overwriting PICMI init to extract gpu distribution for PIConGPU"""

        # convert input to 3 integer list
        if n_gpus == None:
            self.n_gpus = [1, 1, 1]
        elif len(n_gpus) == 1:
            self.ngpus = [1, n_gpus, 1]
        elif len(n_gpus) == 3:
            self.n_gpus = n_gpus

        # continue with regular init
        super().__init__(**kw)

        # check if gpu distribution fits grid
        # TODO: super_cell_size still hard coded
        self.super_cell_size = [8, 8, 4]
        cells = [self.nx, self.ny, self.nz]
        dim_name = ["x", "y", "z"]
        for dim in range(3):
            assert ((cells[i] // n_gpus[i]) // self.super_cell_size[i]) * n_gpus[i]) * self.super_cell_size[i] == cells[i], \
                "GPU- and/or super-cell-distribution in {} dimension does not match grid size".format(dim_name[i])

    def get_as_pypicongpu(self):
        # todo check
        assert [0, 0, 0] == self.lower_bound, "lower bounds must be 0, 0, 0"
        assert self.lower_boundary_conditions == \
            self.upper_boundary_conditions, \
            "upper and lower boundary conditions must be equal " \
            "(can only be chosen by axis, not by direction)"

        util.unsupported("moving window", self.moving_window_velocity)
        util.unsupported("refined regions", self.refined_regions, [])
        util.unsupported("lower bound (particles)",
                         self.lower_bound_particles,
                         self.lower_bound)
        util.unsupported("upper bound (particles)",
                         self.upper_bound_particles,
                         self.upper_bound)
        util.unsupported("lower boundary conditions (particles)",
                         self.lower_boundary_conditions_particles,
                         self.lower_boundary_conditions)
        util.unsupported("upper boundary conditions (particles)",
                         self.upper_boundary_conditions_particles,
                         self.upper_boundary_conditions)
        util.unsupported("guard cells", self.guard_cells)
        util.unsupported("pml cells", self.pml_cells)

        picongpu_boundary_condition_by_picmi_id = {
            "open": grid.BoundaryCondition.ABSORBING,
            "periodic": grid.BoundaryCondition.PERIODIC,
        }

        assert self.bc_xmin in picongpu_boundary_condition_by_picmi_id, \
            "X: boundary condition not supported"
        assert self.bc_ymin in picongpu_boundary_condition_by_picmi_id, \
            "Y: boundary condition not supported"
        assert self.bc_zmin in picongpu_boundary_condition_by_picmi_id, \
            "Z: boundary condition not supported"

        g = grid.Grid3D()
        g.cell_size_x_si = (self.xmax - self.xmin) / self.nx
        g.cell_size_y_si = (self.ymax - self.ymin) / self.ny
        g.cell_size_z_si = (self.zmax - self.zmin) / self.nz
        g.cell_cnt_x = self.nx
        g.cell_cnt_y = self.ny
        g.cell_cnt_z = self.nz
        g.boundary_condition_x = \
            picongpu_boundary_condition_by_picmi_id[self.bc_xmin]
        g.boundary_condition_y = \
            picongpu_boundary_condition_by_picmi_id[self.bc_ymin]
        g.boundary_condition_z = \
            picongpu_boundary_condition_by_picmi_id[self.bc_zmin]
        return g
