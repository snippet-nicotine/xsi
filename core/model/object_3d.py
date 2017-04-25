'''
Created on 28 mars 2017

@author: nico
'''
from typing import Any, List
from model import preferences
from model.kinematics import Transform
import json


class Serializable(object):

    def serialize(self):  # type: () -> str
        return json.dumps(self.__dict__)

    def deSerialize(self, serialized):  # type: (str) -> None
        obj = json.loads(serialized)
        for attributeName in obj:
            if attributeName in self.__dict__.keys():
                self.__dict__[attributeName] = obj[attributeName]


class Node(Serializable):

    TYPE = "Node"

    def __init__(self, name, parent=None, prefix=None, suffix=None ):
        self._name = name
        self._prefix = prefix
        self._suffix = suffix
        self._parent = parent

        if parent is not None:
            parent.add(self)

        self._children = set([])

    @property
    def name(self):
        name = self._name
        if self._prefix is not None:
            name = self._prefix + preferences.SEPARATOR_NAME + self._name
        if self._suffix is not None:
            name = name + preferences.SEPARATOR_NAME + self._suffix

        return name

    def add(self, child):
        if child != self:
            child._parent = self
            self._children.add(child)
            return child

    def remove(self, child):
        if child in self._children:
            self._children.remove(child)

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return self._children

    @property
    def fullName(self):
        if self._parent is None:
            return self._name
        else:
            return self._parent.fullName + preferences.SEPARATOR_HIERARCHY + self._name


class Parameter(Node):

    TYPE = "Parameter"

    def __init__(self, name, value, paramType, constrainer=None):  # type: (str, Any, str, Node) -> None
        super(Parameter, self).__init__(name)
        self._value = value
        self._type = paramType
        self._constrainer = constrainer

    @property
    def value(self):
        if self.constrainer is None:
            return self._value
        else:
            return self.constrainer.value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def constrainer(self):
        return self._constrainer

    @constrainer.setter
    def constrainer(self, constrainer):
        self._constrainer = constrainer

    def __str__(self):
        return self.name + " = " + str(self.value)


class Property(Node):

    TYPE = "Property"
    
    def __init__(self, name):
        super(Property, self).__init__(name)
        self._parameters = {}  # type: List[Parameter]
    
    @property
    def parameters(self):  # type: () -> List[Parameter]
        return self._parameters

    def addParameter(self, parameter):  # type: (Parameter) -> None
        self._parameters.add(parameter)
    
    def __str__(self):
        params = []
        
        for param in self._parameters:
            params.append(str(self._parameters[param]))
            
        return "{name}\n\t{params}\n".format(name=self.name, params=",".join(params) )


class Transformable(Node):
    
    TYPE = "Transformable"
    
    def __init__(self, name, parent = None):
        super(Transformable, self).__init__(name, parent)

        self._constrainer = None
        self._transform = Transform()

    @property
    def transform(self):
        if self._constrainer is not None:
            return self.constrainer.transform
        else:
            return self._transform
        
    @transform.setter
    def transform(self, transform):
        self._transform = transform
    
    @property
    def isConstrained(self):
        return not self._constrainer is None
    
    def constrainTo(self, constrainer):
        self._constrainer = constrainer

class Model(Transformable):
    TYPE = "Model"

class Container(Node):
    TYPE = "Container"

class Buffer(Node):
    TYPE = "Buffer"     
    
class Controller(Node):
    TYPE = "Controller"   
    
class Fk(Node):
    TYPE = "FK"
