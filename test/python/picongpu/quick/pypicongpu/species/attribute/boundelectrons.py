from picongpu.pypicongpu.species.attribute import BoundElectrons, Attribute

import unittest


class TestPosition(unittest.TestCase):
    def test_is_attr(self):
        """is an attribute"""
        self.assertTrue(isinstance(BoundElectrons(), Attribute))

    def test_basic(self):
        be = BoundElectrons()
        self.assertNotEqual("", be.PICONGPU_NAME)
