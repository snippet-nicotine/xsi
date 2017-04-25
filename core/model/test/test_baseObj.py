from unittest import TestCase
from model.object_3d import *


class TestBaseObj(TestCase):
    def test_name(self):
        # Given
        preferences.SEPARATOR_NAME = "_"

        obj = Node("obj")
        obj2 = Node("obj", prefix="prefix", suffix="suffix")
        print(obj2.name)
        self.assertTrue(obj.name == "obj")
        self.assertTrue(obj2.name == "prefix_obj_suffix")

    def test_name_prefix(self):
        #Given
        preferences.SEPARATOR_NAME = "_"

        #When
        obj = Node("obj", prefix="prefix")
        obj2 = Node("obj", prefix="prefix")

        #Then
        self.assertTrue(obj.name == "prefix_obj")
        self.assertTrue(obj.name == "prefix_obj")

    def test_name_suffix(self):
        #Given
        preferences.SEPARATOR_NAME = "_"

        #When
        obj = Node("obj", suffix="suffix")
        obj2 = Node("obj", suffix="suffix")

        #Then
        self.assertTrue(obj.name == "obj_suffix")
        self.assertTrue(obj2.name == "obj_suffix")

    def test_fullName(self):
        obj1 = Node("obj1", prefix="prefix", suffix="suffix")
        obj2 = Node("obj2", prefix="prefix")
        obj3 = Node("obj3", suffix="suffix")
        assert(obj1.name == obj1.fullName)
        assert(obj2.name == obj2.fullName)
        assert(obj3.name == obj3.fullName)