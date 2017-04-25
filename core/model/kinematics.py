'''
Created on 30 mars 2017

@author: nico
'''

class Parameter(object):

    def __init__(self, value):
        self._value = value
        self._constrainer = None

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
        return str(self.value)

class Vector(object):
    def __init__(self, x=0, y=0, z=0):
        self._x = Parameter(x)
        self._y = Parameter(y)
        self._z = Parameter(z)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = Parameter(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = Parameter(value)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = Parameter(value)

    def loadFromStr(self, sVector):
        infos = sVector.split(',')
        if len(infos) == 3:
            self.x = float(infos[0])
            self.y = float(infos[1])
            self.z = float(infos[2])

    def __str__(self):
        return "{},{},{}".format(self.x, self.y, self.z)

class Transform(object):
    '''
    classdocs
    '''

    def __init__(self,  scale=None, rotation=None, position=None):
        '''
        Constructor
        '''

        self._scale = Vector(1,1,1) if scale is None else scale
        self._rotation = Vector() if rotation is None else rotation
        self._position = Vector() if position is None else position

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale.x.value = value.x.value
        self._scale.y.value = value.y.value
        self._scale.z.value = value.z.value

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def __str__(self):
        return "scale({}), rotation({}), position({})".format(self.scale, self.rotation, self.position)