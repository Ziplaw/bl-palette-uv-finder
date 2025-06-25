import pip
pip.main(['install', 'imageio', '--user'])

import sys

#packages_path =  "C:\\Users\\Usuario\\AppData\\Roaming\\Python\\Python311\\Scripts" + "\\..\\site-packages" # the path you see in console

#sys.path.insert(0, packages_path )
import imageio.v3 as iio
import math
from mathutils import Vector

image = iio.imread(r"C:\Users\Usuario\src\repos\bl-uv-plotter-testimages\T_Main_Color_Palette.png")

width = image.shape[1]
height = image.shape[0]

color = Vector((211, 173, 73))
max_iterations = 100

#tetrahedron is point inside:
def same_side(v1, v2, v3, v4, p):
    
    normal = (v2 - v1).cross(v3 - v1)
    dotV4 = (normal).dot(v4 - v1)
    dotP = (normal).dot(p - v1)
    return math.copysign(1,dotV4) == math.copysign(1,dotP)

def point_in_tetrahedron(v1 : Vector, v2 : Vector, v3 : Vector, v4 : Vector, p : Vector):
    return same_side(v1, v2, v3, v4, p) and same_side(v2, v3, v4, v1, p) and same_side(v3, v4, v1, v2, p) and same_side(v4, v1, v2, v3, p)

#rudimentary solver

def evaluate(v1 : Vector, v2 : Vector, v3 : Vector, v4 : Vector, t_1 : float, t_2 : float) -> Vector:
    return ((1 - t_2) * ((1 - t_1) * v1 + v2 * t_1) + ((1 - t_1) * v3 + v4 * t_1) * t_2)

def solve(v1 : Vector, v2 : Vector, v3 : Vector, v4 : Vector, p : Vector) -> tuple[float,float]:

    size = 10
    resolutions = []

    for j in range(size):
        for i in range(size):
            t_1 = i/float(size)
            t_2 = j/float(size)
            i=0
            d=.01

            c7 = evaluate(v1, v2, v3, v4, t_1, 0)
            c8 = evaluate(v1, v2, v3, v4, t_1, 1)
            s = evaluate(v1, v2, v3, v4, t_1, t_2)
            

            last_dot = abs((p-s).normalized().dot((c8-c7).normalized()))
            root_found = False

            while i < max_iterations:
                t_1 += d
                    
                c7 = evaluate(v1, v2, v3, v4, t_1, 0)
                c8 = evaluate(v1, v2, v3, v4, t_1, 1)
                
                s = evaluate(v1, v2, v3, v4, t_1, t_2)

                dot = abs((p - s).normalized().dot((c8 - c7).normalized()))
                if dot < last_dot:
                    d *= -.75
                
                if t_1 > 1 or t_1 < 0:
                    d *= -1

                last_dot = dot
                i+=1

                if dot >= .9999:
                    root_found = True
                    break
                
            t_2 = inverse_lerp(c7, c8, p)

            if t_2 > 0 and t_2 < 1:
                resolutions.append((t_1,t_2))

    max = 0
    max_index = 0

    for i in range(len(resolutions)):
        res = resolutions[i]
        dot = p.dot(lerp(lerp(v1,v2,res[0]),lerp(v3,v4,res[0]),res[1]))

        if dot > max:
            max = dot
            max_index = i


    return (resolutions[max_index][0],resolutions[max_index][1])

    


#lerp

def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b

def lerp(a: Vector, b: Vector, t: float) -> Vector:
    return (1.0 - t) * a + t * b

def inverse_lerp (a : Vector,b: Vector, v : Vector):
    ab = b-a
    av = v-a
    return av.dot(ab) / ab.dot(ab)



for y0 in range(height):
    for x0 in range(width):

        if x0+1 >= width:
            continue
        if y0+1 >= height:
            break

        c1 = tuple([int(i) for i in image[y0,x0]])
        c2 = tuple([int(i) for i in image[y0+1,x0]])
        c3 = tuple([int(i) for i in image[y0,x0+1]])
        c4 = tuple([int(i) for i in image[y0+1,x0+1]])

        if len(set([c1,c2,c3,c4])) != 4:
            continue

        v1 = Vector(c1).xyz
        v2 = Vector(c2).xyz
        v3 = Vector(c3).xyz
        v4 = Vector(c4).xyz

        if point_in_tetrahedron(v1,v2,v3,v4,color):
            print(f"point found inside in {(x0,y0)}")
            t1 = inverse_lerp(v1,v2,color)
            t2 = inverse_lerp(v3,v4,color)

            print(f"t1: {t1}, t2: {t2}")


            if(t1 < 0 or t1 > 1 or t2 < 0 or t2 > 1):
                continue

            values = solve(v1,v2,v3,v4,color)

            v5 = v1.lerp(v2,t1)
            v6 = v3.lerp(v4,t2)

            t3 = inverse_lerp(v5,v6,color)

            l1 = Vector((y0,x0)).lerp(Vector((y0+1,x0)),t1)
            l2 = Vector((y0,x0+1)).lerp(Vector((y0+1,x0+1)),t2)

            l3 = l1.lerp(l2,t3)
            v = l3.x/image.shape[1]
            u = l3.y/image.shape[0]
            print((u,1-v))
            

