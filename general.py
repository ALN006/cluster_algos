import pylab

class point (object):
    """assumes self is a n-dimensional position vector for a point, models self as a array of attributes
    provides methods to calculate the manhattan and euclidean distance between two points"""

    def __init__(self, attribute_array):
        self.attributes = attribute_array
    def __str__(self):
        return str(self.attributes)
    def __eq__(self, other):
        for i in range(len(self.attributes)):
            if self.attributes[i] != other.attributes[i]:
                return False
        return True
    
    def manhattan_distance(self, other):
        return sum(abs(self.attributes - other.attributes))
    def euclidian_distance(self, other):
        return sum(((self.attributes - other.attributes)**2))**0.5
    def plus(self, other):
        return point(self.attributes + other.attributes)
    def minus(self, other):
        return point(self.attributes - other.attributes)
    def dot_product(self, other):
        return sum(self.attributes * other.attributes)
    def scale(self, scalar):
        self.attributes = self.attributes * scalar
    def length(self):
        return sum(self.attributes**2)**0.5
    
    def get_attributes(self):
        return self.attributes
    def get_attribute(self, index):
        return self.attributes[index]
    def get_dimensionality(self):
        return len(self.attributes)
    
    def set_attributes(self, attribute_array):
        self.attributes = attribute_array
    def set_attribute(self, index, value):
        self.attributes[index] = value