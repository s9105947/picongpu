from picongpu import picmi

import unittest
from picongpu import pypicongpu
from math import sqrt


class TestPicmiGaussianLaser(unittest.TestCase):
    def test_basic(self):
        """full laser example"""
        picmi_laser = picmi.GaussianLaser(
            wavelength=1,
            waist=2,
            duration=3,
            focal_position=[.5, 4, .5],
            centroid_position=[.5, 0, .5],
            E0=5,
            propagation_direction=[0, 1, 0],
            polarization_direction=[0, 0, 1],
            picongpu_laguerre_modes=[2.0, 3.0],
            picongpu_laguerre_phases=[4.0, 5.0])

        pypic_laser = picmi_laser.get_as_pypicongpu()
        # translated
        self.assertEqual(1, pypic_laser.wavelength)
        self.assertEqual(2, pypic_laser.waist)
        self.assertEqual(3, pypic_laser.duration)
        self.assertEqual(4, pypic_laser.focus_pos)
        self.assertEqual(5, pypic_laser.E0)
        self.assertEqual(pypicongpu.GaussianLaser.PolarizationType.LINEAR_Z,
                         pypic_laser.polarization_type)
        self.assertEqual([2.0, 3.0], pypic_laser.laguerre_modes)
        self.assertEqual([4.0, 5.0], pypic_laser.laguerre_phases)

        # defaults
        self.assertEqual(0, pypic_laser.phase)
        self.assertEqual(15, pypic_laser.pulse_init)
        self.assertEqual(0, pypic_laser.init_plane_y)

    def test_values_focal_pos(self):
        """only y of focal pos can be varied"""
        # x, z checked against centroid pos

        # difference in x
        picmi_laser = picmi.GaussianLaser(
            1, 2, 3,
            focal_position=[0, 7, .5],
            centroid_position=[.5, 0, .5],
            E0=0)
        with self.assertRaisesRegex(Exception, ".*foc(us|al).*[xX].*"):
            picmi_laser.get_as_pypicongpu()

        # difference in z
        picmi_laser = picmi.GaussianLaser(
            1, 2, 3,
            focal_position=[.5, 2, 500],
            centroid_position=[.5, 0, .5],
            E0=0)
        with self.assertRaisesRegex(Exception, ".*foc(us|al).*[zZ].*"):
            picmi_laser.get_as_pypicongpu()

        # all ok (difference in y)
        picmi_laser = picmi.GaussianLaser(
            1, 2, 3,
            focal_position=[.5, -5, .5],
            centroid_position=[.5, 0, .5],
            E0=0)
        self.assertEqual(-5, picmi_laser.get_as_pypicongpu().focus_pos)

        picmi_laser = picmi.GaussianLaser(
            1, 2, 3,
            focal_position=[.5, 0, .5],
            centroid_position=[.5, 0, .5],
            E0=0)
        self.assertEqual(-5, picmi_laser.get_as_pypicongpu().focus_pos)

    def test_values_propagation_direction(self):
        """only propagation in y+ permitted"""
        invalid_propagation_vectors = [
            [1, 2, 3],
            [0, 0, 1],
            [1, 0, 0],
            [sqrt(2), sqrt(2), 0],
            [0, 0, 0],
            [0, -1, 0],
        ]

        for invalid_propagation_vector in invalid_propagation_vectors:
            picmi_laser = picmi.GaussianLaser(
                1, 2, 3,
                focal_position=[.5, 0, .5],
                centroid_position=[.5, 0, .5],
                propagation_direction=invalid_propagation_vector,
                E0=0)
            with self.assertRaisesRegex(Exception, ".*propagation.*"):
                picmi_laser.get_as_pypicongpu()

        # positive y direction works
        picmi_laser = picmi.GaussianLaser(
            1, 2, 3,
            focal_position=[.5, 0, .5],
            centroid_position=[.5, 0, .5],
            propagation_direction=[0, 1, 0],
            E0=0)


    def test_values_polarization(self):
        """only polarization x & z permitted"""

    def test_values_centroid_position(self):
        """centroid position is fixed for given bounding box"""

    def test_laguerre_modes_types(self):
        """laguerre type-check before translation"""
        with self.assertRaises(TypeError):
            picmi.GaussianLaser(
                1, 2, 3,
                focal_position=[0, 0, 0],
                centroid_position=[0, 0, 0],
                propagation_direction=[0, 1, 0],
                E0=0,
                picongpu_laguerre_modes=["not float"])

        with self.assertRaises(TypeError):
            picmi.GaussianLaser(
                1, 2, 3,
                focal_position=[.5, 0, .5],
                centroid_position=[.5, 0, .5],
                propagation_direction=[0, 1, 0],
                E0=0,
                picongpu_laguerre_phases=set(2.0))
    
    def test_laguerre_modes_optional(self):
        """laguerre modes are optional"""
        # allowed: not given at all
        picmi_laser = picmi.GaussianLaser(
            wavelength=1,
            waist=2,
            duration=3,
            focal_position=[0, 0, 0],
            centroid_position=[0, 0, 0],
            E0=5,
            propagation_direction=[0, 1, 0])
        pypic_laser = picmi_laser.get_as_pypicongpu()
        self.assertEqual([1.0], pypic_laser.laguerre_modes)
        self.assertEqual([0.0], pypic_laser.laguerre_phases)

        # allowed: explicitly None
        picmi_laser = picmi.GaussianLaser(
            wavelength=1,
            waist=2,
            duration=3,
            focal_position=[0, 0, 0],
            centroid_position=[0, 0, 0],
            E0=5,
            propagation_direction=[0, 1, 0],
            picongpu_laguerre_modes=None,
            picongpu_laguerre_phases=None)
        pypic_laser = picmi_laser.get_as_pypicongpu()
        self.assertEqual([1.0], pypic_laser.laguerre_modes)
        self.assertEqual([0.0], pypic_laser.laguerre_phases)

        # not allowed: only phases (or only modes) given
        with self.assertRaisesRegex(Exception, ".*[Ll]aguerre.*"):
            picmi.GaussianLaser(
                wavelength=1,
                waist=2,
                duration=3,
                focal_position=[0, 0, 0],
                centroid_position=[0, 0, 0],
                E0=5,
                propagation_direction=[0, 1, 0],
                picongpu_laguerre_modes=[1.0, 2.0],
                picongpu_laguerre_phases=None)
            
        with self.assertRaisesRegex(Exception, ".*[Ll]aguerre.*"):
            picmi.GaussianLaser(
                wavelength=1,
                waist=2,
                duration=3,
                focal_position=[0, 0, 0],
                centroid_position=[0, 0, 0],
                E0=5,
                propagation_direction=[0, 1, 0],
                picongpu_laguerre_phases=[1.0, 2.0])
