import pylab
import pandas as pd
import numpy as np
class point (object):
    """assumes self is a n-dimensional position vector for a point, models self as a array of attributes"""

    def __init__(self, attributes):
        self.attributes = np.array(attributes)
    def __repr__(self):
        return str(self.attributes)
    def __eq__(self, other):
        return len(self.attributes) == len(other.attributes) and (abs(self.attributes - other.attributes) > 0.0001).all()
    def __hash__(self):
        return hash(tuple(self.attributes))
    
    def __add__(self, other):
        if isinstance(other, point):
            return point(self.attributes + other.attributes)
        else:
            return point(self.attributes + other)
    def __sub__(self, other):
        return self + other * -1
    def __mul__(self, other):
        if isinstance(other, point):
            return point(self.attributes * other.attributes)
        else:
            return point(self.attributes * other)
    def __truediv__(self, other):  
        if isinstance(other, point):
            return point(self.attributes / other.attributes)
        else:
            return point(self.attributes / other)
    def __pow__(self, other):
        if isinstance(other, point):
            return point(self.attributes ** other.attributes)
        else:
            return point(self.attributes ** other)
    
    def __len__(self):
        return len(self.attributes)
    def __getitem__(self, index):
        return self.attributes[index]
    def __setitem__(self, index, value):
        self.attributes[index] = value
    def __iter__(self): 
        return iter(self.attributes)
    def __contains__(self, item): 
        return item in self.attributes
    
    def length(self):
        return self.euclidean_distance(point([0]*len(self.attributes)))
    def manhattan_distance(self, other):
        return sum(abs(self.attributes - other.attributes))
    def euclidean_distance(self, other):
        return sum((self.attributes - other.attributes)**2)**0.5
    def dot(self, other):
        return sum(self.attributes * other.attributes)
    def copy(self):
        return point(self.attributes)
    
    def get_attributes(self):
        return list(self.attributes)
    def set_attributes(self, attributes):
        self.attributes = np.array(attributes)

class cluster(object): 
    """assumes self is a cluster of points, models self as a list of point objects"""

    def __init__(self, data):
        points = data.values.tolist() if isinstance(data, pd.DataFrame) else data
        self.points= []
        self.d = {}
        for p in points:
            self.points.append(p)
            if p in self.d:
                self.d[p] += 1
            else:
                self.d[p] = 1
    def __repr__(self):
        return str(self.points)
    def __eq__(self, other):
        return self.d == other.d
    
    def __add__(self, other):
        return cluster(self.points + other.points)
    def __sub__(self, other):
        points = []
        for i in self.d:
            count_in_other = other.d.get(i, 0)
            for j in range(self.d[i] - count_in_other if self.d[i] > count_in_other else 0):
                points.append(i)
                
        return cluster(points)
    def __mul__(self, other):
        points = []
        if isinstance(other, cluster):
            for i in range(len(self.points)):
                points.append(self.points[i] * other.points[i])
            return cluster(points)
        else:
            for i in range(len(self.points)):
                points.append(self.points[i] * other)
            return cluster(points)
    def __pow__(self, integer):
        points = []
        for i in range(len(self.points)):
            points.append(self.points[i] ** integer)
        return cluster(points)
    
    def __len__(self):
        return len(self.points)
    def __getitem__(self, index):
        return self.points[index]
    def __setitem__(self, index, value):
        self.points[index] = value
    def __iter__(self): 
        return iter(self.points)
    def __contains__(self, item): 
        return item in self.points
    
    def centroid(self):
        return point(sum(self.points) * (1/len(self.points)))
    def DistanceMatrix(self,other, dist_func = point.euclidean_distance):
        matrix = []
        for i in self.points:
            row = []
            for j in other.points:
                row.append(dist_func(i,j))
            matrix.append(row)
        return matrix
    def intensive_linkage(self, other, type = "single", dist_func = point.euclidean_distance):
        matrix = self.DistanceMatrix(other, dist_func)
        if type == "single":    
            return min([min(i) for i in matrix])
        elif type == "complete":        
            return max([max(i) for i in matrix])
        elif type == "average":                 
            return sum([sum(i) for i in matrix]) / (len(matrix) * len(matrix[0]))
    def centroid_linkage(self, other, dist_func = point.euclidean_distance):
        return dist_func(self.centroid(), other.centroid())
    def normalize(self):
        max_val = self.points[0].copy()
        min_val = self.points[0].copy()
        for i in self.points:
            for j in range(len(self.points[0])):
                if i[j] > max_val[j]:
                    max_val[j] = i[j]
                if i[j] < min_val[j]:
                    min_val[j] = i[j]
        return cluster([(i - min_val)/(max_val - min_val) for i in self.points])
    
    def get_points(self):
        return self.points
    def get_d(self):
        return self.d
    
    def reset(self,points: list[point]):
        self.points= []
        self.d = {}
        for p in points:
            self.points.append(p)
            if p in self.d:
                self.d[p] += 1
            else:
                self.d[p] = 1

import unittest     
import random  
class test_point(unittest.TestCase):

    def setUp(self):
        self.trials = 100
        self.dimensions = 3
        self.points = [[ random.random() for _ in range(self.dimensions)] for __ in range(self.trials)]
    
    def test_string(self):
        for i in self.points:
            self.assertEqual(str(np.array(i)), str(point(i)))
    
if __name__ == '__main__':
    unittest.main()

    
    
