from ..pypicongpu import grid
from ..pypicongpu import util

import picmistandard


class Cartesian3DGrid(picmistandard.PICMI_Cartesian3DGrid):
    def get_as_pypicongpu(self):
        # todo check
        assert [0, 0, 0] == self.lower_bound, "lower bounds must be 0, 0, 0"
        assert self.lower_boundary_conditions == \
            self.upper_boundary_conditions, \
            "upper and lower boundary conditions must be equal " \
            "(can only be chosen by axis, not by direction)"

        util.unsupported("moving window", self.moving_window_velocity)
        util.unsupported("refined regions", self.refined_regions)
        util.unsupported("lower bound (particles)", self.lower_bound_particles)
        util.unsupported("upper bound (particles)", self.upper_bound_particles)
        util.unsupported("lower boundary conditions (particles)",
                         self.lower_boundary_conditions_particles)
        util.unsupported("upper boundary conditions (particles)",
                         self.upper_boundary_conditions_particles)
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
