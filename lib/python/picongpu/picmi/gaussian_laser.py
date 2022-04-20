from ..pypicongpu import util
from ..pypicongpu.laser import GaussianLaser

import picmistandard

from typeguard import typechecked


@typechecked
class GaussianLaser(picmistandard.PICMI_GaussianLaser):
    """PICMI object for Gaussian Laser"""

    def get_as_pypicongpu(self) -> GaussianLaser:
        util.unsupported("laser name", self.name)
        util.unsupported("laser zeta", self.zeta)
        util.unsupported("laser beta", self.beta)
        util.unsupported("laser phi2", self.phi2)

        assert 0 == self.focal_position[0] and 0 == self.focal_position[2], \
            "focal position must have x=z=0"
        assert [0, 1, 0] == self.propagation_direction, \
            "only support propagation along Y axis"
        # TODO is this correct?
        assert [0, 0, 0] == self.centroid_position, "centroid must be 0,0,0"

        polarization_by_normal = {
            (1, 0, 0): GaussianLaser.PolarizationType.LINEAR_X,
            (0, 0, 1): GaussianLaser.PolarizationType.LINEAR_Z,
        }
        assert tuple(self.polarization_direction) in polarization_by_normal, \
            "only laser polarization [1, 0, 0] and [0, 0, 1] supported"

        laser = GaussianLaser()
        laser.wavelength = self.wavelength
        laser.waist = self.waist
        laser.duration = self.duration
        laser.focus_pos = self.focal_position[1]
        laser.E0 = self.E0
        laser.phase = 0
        laser.pulse_init = 15
        laser.init_plane_y = 0
        laser.polarization_type = polarization_by_normal[
            tuple(self.polarization_direction)]

        return laser
