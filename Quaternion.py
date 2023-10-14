# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 17:11:10 2023

@author: Wesni
"""
from math import hypot

class Quaternion:
    def __init__(self,a,b,c,d):
        #a,b,c,d are the coefficients for the scalar and i,j,k imaginary parts respectively
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        
    def __mul__(self,other):
        #Returns the solution to the Hamilton product as a new quaternion object
        return Quaternion(self.a*other.a - self.b*other.b - self.c*other.c - self.d*other.d,
                self.a*other.b + self.b*other.a + self.c*other.d - self.d*other.c, \
                self.a*other.c - self.b*other.d + self.c*other.a + self.d*other.b, \
                self.a*other.d + self.b*other.c - self.c*other.b + self.d*other.a)
    
    def __abs__(self):
        #returns the magnitude of the quaternion
        return hypot(self.a,self.b,self.c,self.d)
    
    def __getitem__(self,index):
        #Allows indexing of a,b,c,d. Returns a list.
        return [self.a,self.b,self.c,self.d][index]
        
    def normalize(self):
        #returns a normalized quaternion
        mag = abs(self)
        return Quaternion(self.a/mag,self.b/mag,self.c/mag,self.d/mag)
        
    def conjugate(self):
        #Returns the conjugate of the quaternion as a new quaternion object
        return Quaternion(self.a,-self.b,-self.c,-self.d)
    
    def rotate(self,other):
        #Performs quaternion rotation. p'=qpq^-1
        qp = other*self #multiply qp
        q_conj = other.conjugate() #find q^-1
        qpq = qp*q_conj #multiply qp by q^-1
        qpq = qpq.normalize() #normalize to unit vector
        return qpq #return new rotated quaternion
        