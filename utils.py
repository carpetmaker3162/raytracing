import numpy as np
from functools import reduce
from benchmark import *

# length-1 vector to represent length
@benchmark
def normalize(vector):
    return vector / np.linalg.norm(vector)

# find closest intersection between a circle and ray
@benchmark
def sphere_intersect(center, radius, ray_origin, ray_direction):
    # find t for which the ray intersects the sphere
    # ||ray(t) - Center||^2 = r^2
    # ||Camera + Direction*t - Center||^2 = r^2                                                     (plug in ray equation)
    # dot(Direction*t + Camera - Center, Direction*t + Camera - Center) = r^2                       (express as dot)
    # ||Direction||^2 * t^2 + 2t * dot(Direction, Camera - Center) + ||Camera - Center||^2 = r^2    (expand dot product)

    # a = ||d||^2 = 1
    # b = 2 * dot(Direction, Camera - Center)
    # c = ||Camera - Center||^2 - r^2

    b = 2 * np.dot(ray_direction, ray_origin - center)
    c = np.linalg.norm(ray_origin - center)**2 - radius**2
    delta = b**2 - 4*c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    else:
        return None

# get sphere that intersects earliest with ray
@benchmark
def nearest_intersected(spheres, ray_origin, ray_direction):
    distances = [sphere_intersect(obj["center"], obj["radius"], ray_origin, ray_direction) for obj in spheres]
    nearest = None
    min_dist = np.inf
    
    for i, dist in enumerate(distances):
        if dist is not None and dist < min_dist:
            min_dist = dist
            nearest = spheres[i]
    
    return nearest, min_dist

# reflected ray
# vector: unit vector of ray to be reflected
# axis: unit vector of axis of reflection (aka normal to the surface)
@benchmark
def reflected(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis
