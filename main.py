# TODO: implement refraction
# 12.06s 500x400
# 7.38s 400x300

import time
import random
import numpy as np
import matplotlib.pyplot as plt
from utils import normalize, sphere_intersect, nearest_intersected, reflected
from tqdm import tqdm
from benchmark import benchmark, show_stats

random.seed(0)
t0 = time.time()

width = 400
height = 300
camera = np.array([0, 0, 2])
ratio = width / height
screen = (-1, 1 / ratio, 1, -1 / ratio) # left, top, right, bottom
max_reflection = 10

@benchmark
def trace_ray(origin, direction):
    color = np.zeros(3)
    reflection = 1

    for k in range(max_reflection):
        # find intersection between ray and nearest object
        nearest_object, min_distance = nearest_intersected(spheres, origin, direction)
        if nearest_object is None:
            break
        intersection = origin + min_distance * direction
        
        # step-back away from the object to avoid self-intersection
        normal_to_surface = normalize(intersection - nearest_object['center'])
        shifted_point = intersection + 1e-5 * normal_to_surface
        intersection_to_light = normalize(light['position'] - shifted_point)

        # check whether intersection point is illuminated (check for objs between light and intersection)
        _, min_distance = nearest_intersected(spheres, shifted_point, intersection_to_light)
        intersection_to_light_distance = np.linalg.norm(light['position'] - intersection)
        is_shadowed = min_distance < intersection_to_light_distance

        if is_shadowed:
            break # try reducing illumination

        illumination = np.zeros(3)
        illumination += nearest_object['ambient'] * light['ambient']
        illumination += nearest_object['diffuse'] * light['diffuse'] * np.dot(intersection_to_light, normal_to_surface)
        intersection_to_camera = normalize(camera - intersection)
        H = normalize(intersection_to_light + intersection_to_camera)
        illumination += nearest_object['specular'] * light['specular'] * np.dot(normal_to_surface, H) ** (nearest_object['shininess'] / 4)

        # find refraction using fresnel, snell (unimplemented)

        color += reflection * illumination
        reflection *= nearest_object['reflection']

        origin = shifted_point
        direction = reflected(direction, normal_to_surface)
    
    return color

spheres = [
    {
        "center": np.array([-0.5, -0.5, 0.0]),
        "radius": 0.2,
        "ambient": np.array([0.3, 0, 0]),
        "diffuse": np.array([0.8, 0, 0]),
        "specular": np.array([1, 1, 1]),
        "shininess": 100,
        "reflection": 0,
        "refractive_index": 1.5,
    },
    {
        "center": np.array([0.4, -0.5, -1.5]),
        "radius": 1.0,
        "ambient": np.array([0.0, 0.0, 0.0]),
        "diffuse": np.array([0.2, 0.2, 0.2]),
        "specular": np.array([1, 1, 1]),
        "shininess": 100,
        "reflection": 0.8,
        "refractive_index": 1,
    },
    {
        "center": np.array([0.6, -0.5, 0.0]),
        "radius": 0.2,
        "ambient": np.array([0.0, 0.2, 0.2]),
        "diffuse": np.array([0.0, 0.7, 0.7]),
        "specular": np.array([1, 1, 1]),
        "shininess": 100,
        "reflection": 0,
        "refractive_index": 1,
    },
    {
        'center': np.array([0, -9000, 0]),
        'radius': 9000 - 0.7,
        'ambient': np.array([0.1, 0.1, 0.1]),
        'diffuse': np.array([0.7, 0.7, 0.7]),
        'specular': np.array([1, 1, 1]),
        'shininess': 100,
        "reflection": 0,
        "refractive_index": 1,
    }
]

light = {
    "position": np.array([5, 5, 5]),
    "ambient": np.array([1.0, 0.8, 0.8]),
    "diffuse": np.array([1.0, 0.8, 0.8]),
    "specular": np.array([1.0, 0.8, 0.8]),
}

image = np.zeros((height, width, 3))
times = [] # ignore
for i, y in tqdm(enumerate(np.linspace(screen[1], screen[3], height)), total=height):
    for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
        # define ray from camera into pixel of screen
        time_start = time.time() # ignore
        pixel = np.array([x, y, 0])
        origin = camera
        direction = normalize(pixel - origin)

        color = trace_ray(origin, direction)
        image[i, j] = np.clip(color, 0, 1)
        times.append(time.time() - time_start) # ignore

print(f"per pixel: {1000 * sum(times)/len(times):.6f}ms avg\n")
plt.imsave('image.png', image)
show_stats()
print(f"\ntotal: {time.time() - t0:.6f}s")
