from unittest import TestCase

import model.preferences as preferences
from model.object_3d import Node


class TestObj3D(TestCase):

    def test_init_with_obj3D_as_parent_must_increment_children(self):
        # Given
        parent = Node("parent")
        # Then
        self.assertEquals(0, len(parent.children))
        # When
        Node("child", parent)
        # Then
        self.assertEquals(1, len(parent.children))


    def test_add_a_3dObj_as_parent_should_increment_children(self):
        #Given
        parent = Node("parent")
        #Then
        self.assertEquals(0, len(parent.children))
        #When
        parent.add(Node("child"))
        #Then
        self.assertEquals(1, len(parent.children))

    def test_add_with_self_as_parent_should_fail(self):
        # Given
        parent = Node("parent")
        # Then
        self.assertEquals(0, len(parent.children))
        # When
        parent.add(parent)
        # Then
        self.assertEquals(0, len(parent.children))


    def test_remove_a_child_should_decrement_children(self):
        parent = Node("parent")
        child = Node("child", parent)
        self.assertEqual(len(parent.children), 1)
        parent.remove(child)
        self.assertEqual(len(parent.children), 0)

    def test_remove_a_non_child_should_do_nothing(self):
        parent = Node("parent")
        child = Node("child", parent)
        nochild = Node("nochild")
        self.assertEqual(len(parent.children), 1)
        parent.remove(nochild)
        self.assertEqual(len(parent.children), 1)

    def test_fullName(self):
        #Given
        preferences.SEPARATOR_HIERARCHY = "."
        parent = Node("parent")
        child = Node("child")
        child2 = Node("child2", parent)
        child3 = Node("child3", child2)
        #When
        parent.add(child)
        #Then
        self.assertEquals("parent.child", child.fullName)
        self.assertEquals("parent.child2", child2.fullName)
        self.assertEquals("parent.child2.child3", child3.fullName)