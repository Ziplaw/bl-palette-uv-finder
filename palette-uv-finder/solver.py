from vector_math import *
import imageio.v3 as iio


#gradient solver
def evaluate(v1 : Vector, v2 : Vector, v3 : Vector, v4 : Vector, t_1 : float, t_2 : float) -> Vector:
    a = v1 + t_1 * (v2 - v1)
    b = v3 + t_1 * (v4 - v3)
    
    return a + t_2 * (b - a)

def gradient(v1 : Vector, v2 : Vector, v3 : Vector, v4 : Vector, t_1:float, t_2:float) -> tuple[Vector, Vector]:
    _t_1 = (v1 - v2 - v3 + v4) * t_2 - v1 + v2
    _t_2 = (t_1-1)* v1 + v3 - t_1 * (v2 + v3 - v4)
    
    return (_t_1,_t_2)

def solve_with_gradient(v1 : Vector, v2 : Vector, v3 : Vector, v4 : Vector, p : Vector) -> tuple[float,float]:
    
    t_1 = 0.5
    t_2 = 0.5
    epsilon = .1
    max_iterations = 100
        
    iterator = 0
    
    while iterator < max_iterations:
        
        move = gradient(v1,v2,v3,v4,t_1, t_2)
        
        current = evaluate(v1, v2, v3, v4, t_1, t_2)
        target = p        
        
        moved_t2 = current + move[1] * epsilon
        moved_t1 = current + move[0] * epsilon
        moved_t1_negative = current + move[0] * -epsilon
        moved_t2_negative = current + move[1] * -epsilon
        
        current_distance = (target - current).length
        t1_distance = 10000 if t_1 == 1 else (target - moved_t1).length
        t2_distance = 10000 if t_2 == 1 else (target - moved_t2).length
        t1_distance_negative =  10000 if t_1 == 0 else (target - moved_t1_negative).length
        t2_distance_negative =  10000 if t_2 == 0 else (target - moved_t2_negative).length

        if t1_distance < current_distance and t1_distance < t2_distance and t1_distance < t1_distance_negative and t1_distance < t2_distance_negative:
            t_1 = min(1, t_1 + epsilon) 
        elif t2_distance < current_distance and t2_distance < t1_distance and t2_distance < t1_distance_negative and t2_distance < t2_distance_negative:
            t_2 = min(1, t_2 + epsilon)
        elif t1_distance_negative < current_distance and t1_distance_negative < t2_distance and t1_distance_negative < t1_distance and t1_distance_negative < t2_distance_negative:
            t_1 = max(0, t_1 - epsilon)
        elif t2_distance_negative < current_distance and t2_distance_negative < t2_distance and t2_distance_negative < t1_distance_negative and t2_distance_negative < t1_distance:
            t_2 = max(0, t_2 - epsilon)
        else:
            epsilon *= .9

        iterator+=1

    return(t_1,t_2)

