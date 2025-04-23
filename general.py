import pylab

class point (object):
    """assumes self is a n-dimensional position vector for a point, models self as a array of attributes"""

    def __init__(self, attribute_list):
        self.attributes = pylab.array(attribute_list)
    def __str__(self):
        return str(self.attributes)
    def __eq__(self, other):
        if len(self.attributes) != len(other.attributes):
            return False
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
    def dot(self, other):
        return sum(self.attributes * other.attributes)
    def scale(self, scalar):
        self.attributes = self.attributes * scalar
    def length(self):
        return sum(self.attributes**2)**0.5
    def dimensionality(self):
        return len(self.attributes)
    
    def get_attributes(self):
        return self.attributes
    def attribute(self, index):
        return self.attributes[index]
    
    def set_attributes(self, attribute_array):
        self.attributes = pylab.array(attribute_array)
    def set_attribute(self, index, value):
        self.attributes[index] = value

class cluster(object):
    """assumes self is a cluster of points, models self as a list of point objects"""
    def __init__(self, points):
        self.points = points
    def __str__(self):
        return str(self.points)
    def __eq__(self, other):
        if len(self.points) != len(other.points):
            return False
        for i in range(len(self.points)):
            if self.points[i] != other.points[i]:
                return False
        return True
    
    def centroid(self):
        """returns the centroid of self as a point object"""
        centroid = point([0]*self.points[0].dimensionality())
        for p in self.points:
            centroid = centroid.plus(p)
        centroid.scale(1/len(self.points))
        return centroid
    def single_linkage(self, other, distance_function = point.euclidian_distance):
        """returns shortest distance between self and other"""
        min_distance = distance_function(self.points[0],other.points[0])
        ans = self.points[0].minus(other.points[0])
        for p1 in self.points:
            for p2 in other.points:
                distance = distance_function(p1,p2)
                if distance < min_distance:
                    min_distance = distance
                    ans = p1.minus(p2)
        return ans
    def complete_linkage(self, other, distance_function = point.euclidian_distance):
        """returns longest distance between self and other"""
        max_distance = distance_function(self.points[0],other.points[0])
        ans = self.points[0].minus(other.points[0])
        for p1 in self.points:
            for p2 in other.points:
                distance = distance_function(p1,p2)
                if distance > max_distance:
                    max_distance = distance
                    ans = p1.minus(p2)
        return ans
    def centroid_linkage(self, other):
        """returns distance between centroids of self and other"""
        return self.centroid().minus(other.centroid())
    def scale(self, scalar):
        """scales all points in self by scalar"""
        for p in self.points:
            p.scale(scalar)
        return self
    
    def add(self, point):
        self.points.append(point)
    def remove(self, point):
        self.points.remove(point)
    def merge(self, other):
        self.points.extend(other.points)
    def clear(self):
        self.points = []
    
    def points(self):
        return self.points