import numpy as np
import unittest     
import random  



class point (object):
    """assumes self is a n-dimensional position vector for a point, models self as a array of attributes"""
 
    #basic properties
    def __init__(self: "point", attributes: list) -> None:
        self.attributes = np.array(attributes)

    def __repr__(self: "point") -> str:
        return str(self.attributes)
    
    def __eq__(self: "point", other:"point") -> bool:
        if len(self.attributes) != len(other.attributes):
            return False 
        ans = True
        for i in (abs(self.attributes - other.attributes) < 0.0001):
            ans &= i
        return ans
    
    def __abs__(self: "point") -> "point":
        return point(abs(self.attributes))
    
    def __len__(self: "point") -> int:
        return len(self.attributes)
    
    def __hash__(self: "point") -> int:
        return hash(tuple(np.round(self.attributes, decimals=2))) #its only 2 places cause of cluster hashing
    

    #amazingly this works for points, numbers and floats cause np.array(point) works and np.array(a number) = that number
    def __add__(self: "point", other: "point") -> "point":
        return (point(self.attributes + np.array(other)))
    
    def __sub__(self: "point", other: "point") -> "point":
        return self + other * -1
    
    def __mul__(self: "point", other: "point") -> "point":
        return (point(self.attributes * np.array(other)))
    
    def __truediv__(self: "point", other: "point") -> "point":  
        return (point(self.attributes / np.array(other)))
    
    def __pow__(self: "point", other: "point") -> "point":
        return (point(self.attributes ** np.array(other)))
    

    #item retrival, assignment and iteration 
    def __getitem__(self: "point", index: int) -> float:
        return self.attributes[index]
    
    def __setitem__(self: "point", index: int, value: float) -> None:
        self.attributes[index] = value

    def __iter__(self: "point"): 
        return iter(self.attributes)
    
    def __contains__(self: "point", item: float) -> bool: 
        return item in self.attributes
    

    #relational opperators, basically works the same as for a list
    def __ge__(self: "point",other: "point") -> bool:
        return list(self.attributes) >= list(other.attributes)
    
    def __gt__(self: "point",other: "point") -> bool:
        return list(self.attributes) > list(other.attributes)
    
    def __lt__(self: "point",other: "point") -> bool:
        return list(self.attributes) < list(other.attributes)
    
    def __le__(self: "point",other: "point") -> bool:
        return list(self.attributes) <= list(other.attributes)
    

    #non dunder methods
    def length(self: "point") -> float:
        return self.euclidean_distance(point([0]*len(self.attributes)))
    
    def manhattan_distance(self: "point", other: "point") -> float:
        return sum(abs(self.attributes - other.attributes))
    
    def euclidean_distance(self: "point", other: "point") -> float:
        return sum((self.attributes - other.attributes)**2)**0.5
    
    def dot(self: "point", other: "point") -> float:
        return sum(self.attributes * other.attributes)
    
    def copy(self: "point") -> "point":
        return point(self.attributes)
    

    #getter and setter methods
    def get_attributes(self: "point") -> list:
        return list(self.attributes)
    
    def set_attributes(self: "point", attributes: list) -> None:
        self.attributes = np.array(attributes)



class test_point(unittest.TestCase):

    def setUp(self):
        self.trials = 100
        self.dimensions = 3
        self.points = [[ random.random() for _ in range(self.dimensions)] for __ in range(self.trials)]
    
    def test_string(self):
        for i in self.points:
            self.assertEqual(str(np.array(i)), str(point(i)))
    def test_eq(self):
        for i in self.points:
            self.assertEqual(point(i), point(i))
            self.assertNotEqual(point(i), point(i + [0]))
            self.assertNotEqual(point(i), point([j + 0.01 for j in i]))
            p = point(i)
            p[0] += 0.1
            self.assertNotEqual(p,point(i))
    def test_hash(self):
        for i in self.points:
            self.assertTrue(isinstance(hash(point(i)),int))
            self.assertNotEqual(hash(point(i)), hash(point([j + 0.01 for j in i])))
    def test_op_num(self):
        r = random.random() + 0.01
        for i in self.points:
            self.assertEqual(((point(i) +r) - r), point(i))
            self.assertEqual(((point(i)*r)/r),point(i))
            self.assertEqual(((point(i)**r)**(1/r)), point(i))
    def test_len(self):
        for i in self.points:
            self.assertEqual(len(i),len(point(i)))
    def test_item_access(self):
        for i in self.points:
            p = point(i)
            p[0] = p[0] + 1
            self.assertNotEqual(i[0],p[0])
    def test_iter_contain(self):
        ans =True
        for i in self.points:
            for j in point(i):
                ans &= j in point(i)
        self.assertTrue(ans)
    def test_euclidean_dist(self):
        for i in range(1,len(self.points)):
            d1 = point(self.points[i-1]).euclidean_distance(point(self.points[i]))
            d2 = (sum((np.array(self.points[i-1]) - np.array(self.points[i]))**2))**0.5
            self. assertAlmostEqual(d1,d2)
    def test_manhattan_dist(self):
        for i in range(1,len(self.points)):
            d1 = point(self.points[i-1]).manhattan_distance(point(self.points[i]))
            d2 = sum(abs(np.array(self.points[i-1]) - np.array(self.points[i])))
            self. assertAlmostEqual(d1,d2)
    def test_dot(self):
        for i in range(1,len(self.points)):
            a = point(self.points[i-1]).dot(point(self.points[i]))
            b = sum(np.array(self.points[i-1])*np.array(self.points[i]))
            self.assertEqual(a,b)
    def test_copy(self):
        for i in self.points:
            a = point(i)
            b = a
            c = a.copy()
            a[0] += 1
            self.assertEqual(a,b)
            self.assertNotEqual(a,c)
    def test_get_set(self):
        for i in self.points:
            p = point(i)
            p.set_attributes(i)
            self.assertEqual(point(i).get_attributes(), i)