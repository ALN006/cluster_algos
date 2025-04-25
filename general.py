import pylab
import pandas as pd
import random
class point (object):
    """assumes self is a n-dimensional position vector for a point, models self as a array of attributes"""

    def __init__(self, attribute_list = []):
        self.attributes = pylab.array(attribute_list)
    def __str__(self):
        return str(self.attributes)
    def __eq__(self, other):
        if len(self.attributes) != len(other.attributes):
            return False
        for i in range(len(self.attributes)):
            if abs(self.attributes[i] - other.attributes[i]) > 0.0001:
                return False
        return True
    def __repr__(self):
        return str(self.attributes)
    def __add__(self, other):
        return point(self.attributes + other.attributes)
    def __sub__(self, other):
        return point.__add__(self, other.scaled(-1))
    def __mul__(self, other):
        return sum(self.attributes * other.attributes)
    def __len__(self):
        return len(self.attributes)
    
    def manhattan_distance(self, other):
        return sum(abs(self.attributes - other.attributes))#this actually works
    def euclidean_distance(self, other):
        return sum(((self.attributes - other.attributes)**2))**0.5
    def length(self):
        return point.euclidean_distance(self, point([0]*len(self.attributes)))
    
    def get_attributes(self):
        return self.attributes
    def attribute(self, index):
        return self.attributes[index]
    
    def set_attributes(self, attribute_array):
        self.attributes = pylab.array(attribute_array)
    def set_attribute(self, index, value):
        self.attributes[index] = value
    def scaled(self, scalar):
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
        centroid = point([0]*len(self.points[0]))
        for p in self.points:
            centroid = centroid + p
        centroid = centroid.scaled(1/len(self.points))
        return centroid
    def intensive_linkage(self, other,link = "single", distance_function = point.euclidean_distance):
        """returns linkage vector between self and other"""
        link_f = {"single": (lambda x,y: x < y), "complete": (lambda x,y: x > y)}
        d = distance_function(self.points[0],other.points[0])
        ans = self.points[0] - other.points[0]
        for p1 in self.points:
            for p2 in other.points:
                distance = distance_function(p1,p2)
                if link_f[link](distance, d):
                    d = distance
                    ans = p1 - p2
        return ans
    def centroid_linkage(self, other):
        return self.centroid() - (other.centroid())
    def scaled(self, scalar):
        return cluster([p.scaled(scalar) for p in self.points])
    
    def get_points(self):
        return self.points
    
    def append(self, point):
        self.points.append(point)
    def remove(self, point):
        self.points.remove(point)
    def clear(self):
        self.points = []
    def normalized(self):
        points = self.points.copy()
        mins = points[0].get_attributes()
        maxs = points[0].get_attributes()
        n = len(points[0])
        for p in points:
            for i in range(n):
                if p.attribute(i) < mins[i]:
                    mins[i] = p.attribute(i)
                if p.attribute(i) > maxs[i]:
                    maxs[i] = p.attribute(i)
        for p in points:
            p.set_attributes((p.get_attributes() - mins) / (maxs - mins))
        return cluster(points)

class test_point(object):
    
    def __init__(self, trials, dimensions):
        self.dimensions = dimensions
        self.trials = trials

    def get(self):
        for i in range(self.trials):
            L = [random.random() for j in range(self.dimensions)]
            p = point()
            p.set_attributes(L)
            if L != list(p.get_attributes()):
                print(f" get_attributes failed\n p = {p}\n p.get_attributes() = {p.get_attributes()}")
                return False
        return True
    def string(self):
        for i in range(self.trials):
            L = [random.random() for j in range(self.dimensions)]
            p = point(L)
            if not(str(p) == str(pylab.array(L)) == repr(p)):
                print(f"string failed\n p = {p}\n str(p) = {str(p)}\n repr(p) = {repr(p)}")
                return False
        return True
    def add(self):
        for i in range(self.trials):
            L1 = [random.random() for j in range(self.dimensions)]
            L2 = [random.random() for j in range(self.dimensions)]
            p1 = point(L1)
            p2 = point(L2)
            if point((p1 + p2).get_attributes()) != point(pylab.array(L1) + pylab.array(L2)):
                print(f"add failed\n p1 = {p1}\n p2 = {p2}\n p1 + p2 = {p1 + p2}")
                return False
        return True
    def mul(self):
        for i in range(self.trials):
            L1 = [random.random() for j in range(self.dimensions)]
            L2 = [random.random() for j in range(self.dimensions)]
            p1 = point(L1)
            p2 = point(L2)
            if (p1 * p2) != sum(pylab.array(L1) * pylab.array(L2)):
                print(f"mul failed\n p1 = {p1}\n p2 = {p2}\n p1 * p2 = {p1 * p2}")
                return False
        return True
    def len(self):
        for i in range(self.trials):
            L = [random.random() for j in range(self.dimensions)]
            p = point(L)
            if len(p) != len(L):
                print(f"len failed\n p = {p}\n len(p) = {len(p)}\n len(L) = {len(L)}")
                return False
        return True
    def manhattan_distance(self):
        for i in range(self.trials):
            L1 = [random.random() for j in range(self.dimensions)]
            L2 = [random.random() for j in range(self.dimensions)]
            p1 = point(L1)
            p2 = point(L2)
            if p1.manhattan_distance(p2) != sum(abs(pylab.array(L1) - pylab.array(L2))):
                print(f"manhattan_distance failed\n p1 = {p1}\n p2 = {p2}\n p1.manhattan_distance(p2) = {p1.manhattan_distance(p2)}")
                return False
        return True
    def euclidean_distance(self):
        for i in range(self.trials):
            L1 = [random.random() for j in range(self.dimensions)]
            L2 = [random.random() for j in range(self.dimensions)]
            p1 = point(L1)
            p2 = point(L2)
            if p1.euclidean_distance(p2) != sum((pylab.array(L1) - pylab.array(L2))**2)**0.5:
                print(f"euclidean_distance failed\n p1 = {p1}\n p2 = {p2}\n p1.euclidean_distance(p2) = {p1.euclidean_distance(p2)}")
                return False
        return True
    def eq(self):
        for i in range(self.trials):
            L = [random.random() for j in range(self.dimensions)]
            p = point(L)
            p2 = point([L[0]+0.01]+L[1:])
            if p == p2 or p != p:
                print(f"eq failed\n p = {p}\n p2 = {p2}\n p == p2 = {p == p2}\n p != p = {p != p}")
                return False
        return True
    def scaled(self):
        for i in range(self.trials):
            L1 = [random.random() for j in range(self.dimensions)]
            L2 = [random.random() for j in range(self.dimensions)]
            p1 = point(L1)
            p2 = point(L2)
            if p1.scaled(p2.get_attributes()) != point(pylab.array(L1) * pylab.array(L2)):
                print(f"scaled failed\n p1 = {p1}\n p2 = {p2}\n p1.scaled(p2.get_attributes()) = {p1.scaled(p2.get_attributes())}")
                return False
        return True
    def TestAll(self):
        result = True
        tests = [self.get, self.string, self.add, self.mul, self.len, self.manhattan_distance,\
                 self.euclidean_distance, self.eq, self.scaled]
        for t in tests:
            if not t():
                result = False
        return result

        
