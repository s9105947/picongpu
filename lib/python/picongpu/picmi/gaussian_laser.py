from ..pypicongpu import util, laser

import picmistandard

from typeguard import typechecked


@typechecked
class GaussianLaser(picmistandard.PICMI_GaussianLaser):
    """PICMI object for Gaussian Laser"""

    def get_as_pypicongpu(self) -> laser.GaussianLaser:
        util.unsupported("laser name", self.name)
        util.unsupported("laser zeta", self.zeta)
        util.unsupported("laser beta", self.beta)
        util.unsupported("laser phi2", self.phi2)
        # unsupported: fill_in (do not warn, b/c we don't know if it has been
        # set explicitly, and always warning is bad)

        assert 0 == self.focal_position[0] and 0 == self.focal_position[2], \
            "focal position must have x=z=0"
        assert [0, 1, 0] == self.propagation_direction, \
            "only support propagation along Y axis"
        # TODO is this correct?
        assert [0, 0, 0] == self.centroid_position, "centroid must be 0,0,0"

        polarization_by_normal = {
            (1, 0, 0): laser.GaussianLaser.PolarizationType.LINEAR_X,
            (0, 0, 1): laser.GaussianLaser.PolarizationType.LINEAR_Z,
        }
        assert tuple(self.polarization_direction) in polarization_by_normal, \
            "only laser polarization [1, 0, 0] and [0, 0, 1] supported"

        pypicongpu_laser = laser.GaussianLaser()
        pypicongpu_laser.wavelength = self.wavelength
        pypicongpu_laser.waist = self.waist
        pypicongpu_laser.duration = self.duration
        pypicongpu_laser.focus_pos = self.focal_position[1]
        pypicongpu_laser.E0 = self.E0
        pypicongpu_laser.phase = 0
        pypicongpu_laser.pulse_init = 15
        pypicongpu_laser.init_plane_y = 0
        pypicongpu_laser.polarization_type = polarization_by_normal[
            tuple(self.polarization_direction)]

        return pypicongpu_laser
