import pylab
import pandas as pd

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
    def __repr__(self):
        return str(self.attributes)
    def __add__(self, other):
        return point(self.attributes + other.attributes)
    def __sub__(self, other):
        return point(self.attributes - other.attributes)
    def __mul__(self, other):
        return point(self.attributes * other.attributes)
    
    def manhattan_distance(self, other):
        return sum(abs(self.attributes - other.attributes))#this actually works
    def euclidian_distance(self, other):
        return sum(((self.attributes - other.attributes)**2))**0.5
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
    def scale(self, scalar):
        return point(self.attributes * scalar)

class cluster(object):
    """assumes self is a cluster of points, models self as a list of point objects"""
    def __init__(self, points = []):
        self.points = points
    def __str__(self):
        s = ""
        for p in self.points:
            s += str(p)
        return s
    def __eq__(self, other):
        if len(self.points) != len(other.points):
            return False
        for i in range(len(self.points)):
            if self.points[i] != other.points[i]:
                return False
        return True
    def __repr__(self):
        return str(self)
    def __add__(self, other):
        return cluster(self.points + other.points)
    def __sub__(self, other):
        """returns a new cluster with all points in self that are not in other"""
        return cluster([p for p in self.points if p not in other.points])
    
    def centroid(self):
        """returns the centroid of self as a point object"""
        centroid = point([0]*self.points[0].dimensionality())
        for p in self.points:
            centroid = centroid.plus(p)
        centroid = centroid.scale(1/len(self.points))
        return centroid
    def intensive_linkage(self, other,link = "single", distance_function = point.euclidian_distance):
        """returns linkage vector between self and other"""
        link_f = {"single": (lambda x,y: x < y), "complete": (lambda x,y: x > y)}
        d = distance_function(self.points[0],other.points[0])
        ans = self.points[0].minus(other.points[0])
        for p1 in self.points:
            for p2 in other.points:
                distance = distance_function(p1,p2)
                if link_f[link](distance, d):
                    d = distance
                    ans = p1.minus(p2)
        return ans
    def centroid_linkage(self, other):
        return self.centroid().minus(other.centroid())
    def scale(self, scalar):
        L = []
        for p in self.points:
            L += [p.scale(scalar)]
        return cluster(L)
    
    def get_points(self):
        return self.points
    
    def append(self, point):
        self.points.append(point)
    def remove(self, point):
        self.points.remove(point)
    def clear(self):
        self.points = []
    def normalize(self):
        pass