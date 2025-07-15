from mathutils import Vector
import math

#lerp
def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b

def lerp(a: Vector, b: Vector, t: float) -> Vector:
    return (1.0 - t) * a + t * b

def inverse_lerp (a : Vector,b: Vector, v : Vector):
    ab = b-a
    av = v-a
    return av.dot(ab) / ab.dot(ab)

#gamma correction
def linearVector(a : Vector) -> Vector:
    return Vector((linear(abs(a.x)) * math.copysign(1,a.x),linear(abs(a.y)) * math.copysign(1,a.y),linear(abs(a.z)) * math.copysign(1,a.z)))

def linear(f : float) -> float:
    return ((f)**(1/2.2))

def srgbVector(a : Vector) -> Vector:
    return Vector((srgb(a.x),srgb(a.y),srgb(a.z)))

def srgb(f : float) -> float:
    return ((f)**2.2)

#tetrahedron is point inside:
def same_side(v1, v2, v3, v4, p):
    
    normal = (v2 - v1).cross(v3 - v1)
    dotV4 = (normal).dot(v4 - v1)
    dotP = (normal).dot(p - v1)
    return math.copysign(1,dotV4) == math.copysign(1,dotP)

def point_in_tetrahedron(v1 : Vector, v2 : Vector, v3 : Vector, v4 : Vector, p : Vector):
    return same_side(v1, v2, v3, v4, p) and same_side(v2, v3, v4, v1, p) and same_side(v3, v4, v1, v2, p) and same_side(v4, v1, v2, v3, p)
