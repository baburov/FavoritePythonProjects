import numpy as np
import tkinter as tk
import random as r
from PIL import Image, ImageTk

# Определение сцены
class Sphere:
    def __init__(self, center, radius, color):
        self.center = np.array(center)
        self.radius = radius
        self.color = np.array(color)

    def intersect(self, ray_origin, ray_direction):
        oc = ray_origin - self.center
        a = np.dot(ray_direction, ray_direction)
        b = 2.0 * np.dot(oc, ray_direction)
        c = np.dot(oc, oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c

        if discriminant > 0:
            t1 = (-b - np.sqrt(discriminant)) / (2.0 * a)
            t2 = (-b + np.sqrt(discriminant)) / (2.0 * a)
            return min(t1, t2) if t1 > 0 else t2
        return None
img_scale = 1.5
width, height = round(450 * img_scale), round(150 * img_scale)
aspect_ratio = width / height
fov = 45
cadr = 1
scale = 2
planets_speed = 30

camera_position = np.array([0, 10, 120])
target_point = np.array([0, 0, 0])
camera_direction = np.array([0, -40, -110])

camera_direction = camera_direction / np.linalg.norm(camera_direction)

colors = [
    (169, 169, 169), (192, 192, 192), (0, 0, 255), 
    (255, 69, 0), (255, 165, 0), (218, 165, 32), 
    (135, 206, 235), (0, 0, 139)
]
radius = [0.4, 0.95, 1, 0.5, 1.5, 1.2, 1, 1]
radius = [x * scale for x in radius]
# Скорости вращения планет (разные для каждой планеты)
speeds = [0.02, 0.015, 0.01, 0.008, 0.005, 0.004, 0.003, 0.0025]
speeds = [x * planets_speed for x in speeds]
# Орбиты планет
orbit_radii = [7, 11, 15, 19, 25, 31, 37, 43]
orbit_radii = [x * scale for x in orbit_radii]

times = []
for i in range(8):
    times.append(r.randint(0, 400))



# Создание окна Tkinter
root = tk.Tk()
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()
def render_scene():
    global times, colors, radius, cadr
    image = Image.new('RGB', (width, height))
    pixels = image.load()

    spheres = [
        Sphere(center=[0, 0, 0], radius=4 * scale, color=[255, 255, 0])  # Солнце
    ]

    for i in range(8):
        x = orbit_radii[i] * np.cos(times[i] * speeds[i])
        y = 0
        z = orbit_radii[i] * np.sin(times[i] * speeds[i]) 
        spheres.append(Sphere(center=[x, y, z], radius=radius[i], color=colors[i]))

    fov_tan = np.tan(np.radians(fov) / 2)
    aspect_ration_with_fov_tan = aspect_ratio * fov_tan
    for y in range(height):
        for x in range(width):
            u = (2 * (x + 0.5) / width - 1) * aspect_ration_with_fov_tan
            v = (1 - 2 * (y + 0.5) / height) * fov_tan

            ray_direction = np.array([u, v, -1])
            ray_direction = ray_direction / np.linalg.norm(ray_direction)

            closest_t = float('inf')
            closest_sphere = None

            for sphere in spheres:
                t = sphere.intersect(camera_position, ray_direction)
                if t and t < closest_t:
                    closest_t = t
                    closest_sphere = sphere

            if closest_sphere:
                color = closest_sphere.color
            else:
                color = [0, 0, 0]

            pixels[x, y] = tuple(color)

    # Обновление изображения на холсте Tkinter
    img_tk = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.image = img_tk

    # Увеличение времени и перерисовка сцены
    times = [x + cadr for x in times]
    root.after(1, render_scene)

# Запуск рендеринга
render_scene()
root.mainloop()