import tkinter as tk
from logic import *
from tkinter import messagebox

points1 = []
points2 = []
coef = 0.75
offset = 10
frame_offset = 30

def on_select_points1_listbox(points1_listbox, entry):
    selected_index = points1_listbox.curselection()
    if selected_index:
        entry.delete(0, tk.END)
        entry.insert(0, points1_listbox.get(selected_index[0])[3:])

def on_select_points2_listbox(points2_listbox, entry):
    selected_index = points2_listbox.curselection()
    if selected_index:
        entry.delete(0, tk.END)
        entry.insert(0, points2_listbox.get(selected_index[0])[3:])

def edit_item(points1_listbox, points2_listbox, entry, color1, color2, canvas, maxsize):
    global points1, points2, coef, offset
    selected_index = (points1_listbox.curselection(), 1) if len(points1_listbox.curselection()) != 0 else (points2_listbox.curselection(), 2)
    try:
        if selected_index[0]:
            new_value = entry.get()
            if selected_index[1] == 1:
                points1_listbox.delete(selected_index[0][0])
                points1.pop(selected_index[0][0])
                points1_listbox.insert(selected_index[0][0], str(selected_index[0][0] + 1) + ") " + str(new_value))
                x, y = map(float, new_value.split(' '))
                points1.insert(selected_index[0][0], [x, y])
            else:
                points2_listbox.delete(selected_index[0][0])
                points2.pop(selected_index[0][0])
                points2_listbox.insert(selected_index[0][0], str(selected_index[0][0] + 1) + ") " + str(new_value))
                x, y = map(float, new_value.split(' '))
                points2.insert(selected_index[0][0], [x, y])
            entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные данные для редактирования\nДробные числа вводятся через точку")

    offset = max(get_offset(points1), get_offset(points2))
    coef = min(zooming(points1, maxsize, offset), zooming(points2, maxsize, offset))

    canvas.delete("all")

    draw_points(points1, canvas, coef, color1, offset)
    draw_points(points2, canvas, coef, color2, offset)


#функция для отризовики массива точек
def draw_points(buf, canvas, coef, color, offset):
    points = buf
    points = list(map(lambda x: [x[0], -1 * x[1]], points))
    index = 1
    for point in points:
        x, y = (point[0] + offset) * coef + frame_offset, (point[1] + offset) * coef + frame_offset
        canvas.create_text(x + 9, y + 4, text=str(index) + ")", font=("Arial", 10), fill="black")
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, outlineoffset = "n")
        index += 1

#функция для отризовики  точек треугольника
def draw_points_1(buf, canvas, coef, color, offset):
    points = buf
    points = list(map(lambda x: [x[0], -1 * x[1]], points))
    index = 0
    for point in points:
        x, y = (point[0] + offset) * coef + frame_offset, (point[1] + offset) * coef + frame_offset
        canvas.create_text(x + 40, y + 4, text=str(buf[index][0]) + ", " + str(buf[index][1]), font=("Arial", 10), fill="black")
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, outlineoffset = "n")
        index += 1

#расчет отступа
def get_offset(buf):
    points = buf
    points = list(map(lambda x: [x[0], -1 * x[1]], points))
    return 1 if len(points) == 0 or min(min(points, key=lambda x: x[0])[0], min(points, key=lambda x: x[1])[1]) > 0 else 1 + -1 * (min(min(points, key=lambda x: x[0])[0], min(points, key=lambda x: x[1])[1])) 

#нахождение точек пересечения с прямой
def find_intersection_points(equation, canvas_width, canvas_height, mode):
    m, b = equation
    if mode == 0:
        x1 = 0
        y1 = find_y(x1, equation)

        x2 = canvas_width
        y2 = find_y(x2, equation)
    else:
        x1, x2 = b, b
        y1, y2 = 0, canvas_height
    return (x1, y1), (x2, y2)

#вспомогательная функция для поиска y координаты
def find_y(x, equation):
    m, b = equation
    y = m * x + b
    return y

#расчет коэффициента увеличения
def zooming(buf, maxsize, offset):
    points = buf
    points = list(map(lambda x: [x[0], -1 * x[1]], points))

    if len(points) != 0:
        coef1 = maxsize / (max(points, key=lambda x: x[0])[0] + offset)
        coef2 = maxsize / (max(points, key=lambda x: x[1])[1] + offset)
        coef = 0.75 * min(coef1, coef2)
    else:
        coef = 200000000
    return coef

#расчет уравнения прямой
def find_line_equation(point1, point2):
    error = 0
    x1, y1 = point1
    x2, y2 = point2
    if x2 == x1:
        error = 1
        m = 0
        b = x1
    else:
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
    return m, b, error

#отрисовка треугольников и прямой
def triangles_and_line_plot(label, canvas, maxsize, color1, color2):
    global points1, points2, coef, offset

    canvas.delete("all")
    draw_points(points1, canvas, coef, color1, offset)
    draw_points(points2, canvas, coef, color2, offset)
    try:
        first_triangle, second_triangle, first_point, second_point, max_angle = points_processing(points1, points2)
        first_triangle_after_zooming = list(map(lambda x: [(x[0] + offset) * coef + frame_offset, (-1 * x[1] + offset) * coef + frame_offset], first_triangle))
        second_triangle_after_zooming = list(map(lambda x: [(x[0] + offset) * coef + frame_offset, (-1 * x[1] + offset) * coef + frame_offset], second_triangle))
        first_point = ((first_point[0] + offset) * coef + frame_offset, (-1 *first_point[1] + offset) * coef + frame_offset)
        second_point = ((second_point[0] + offset) * coef + frame_offset, (-1 *second_point[1] + offset) * coef + frame_offset)
    except Exception:
        messagebox.showerror("Ошибка", "Не хватает точек (минимум 3)\nдля построения тупоугольных треугольников")
    draw_points_1(first_triangle, canvas, coef, "blue", offset)
    draw_points_1(second_triangle, canvas, coef, "red", offset)
    canvas.create_polygon(first_triangle_after_zooming[0], first_triangle_after_zooming[1], first_triangle_after_zooming[2], fill="", outline="blue")
    canvas.create_polygon(second_triangle_after_zooming[0], second_triangle_after_zooming[1], second_triangle_after_zooming[2], fill="", outline="red")

    m, b, error = find_line_equation(first_point, second_point)

    start_point, end_point = find_intersection_points((m, b), maxsize, maxsize, error)
    canvas.create_line(start_point, end_point, fill="black")


    label.config(text="Первый треугольник: " + "(" + "), (".join(['; '.join(map(lambda x: str(x), row)) for row in first_triangle]) + ")\n" +
                "Второй треугольник: " +  "(" + "), (".join(['; '.join(map(lambda x: str(x), row)) for row in second_triangle]) + ")\n" +
                "Максимальный угол между прямой, проходящей через вершины\nтупых углов из двух групп точек: " + str(round(max_angle, 2)))

#функция удаления точек
def delete_point(points_listbox, canvas, coef, mode, color1, color2, maxsize):
    global points1, points2, offset
    selected_indexes = list(points_listbox.curselection())
    for i in selected_indexes:
        if mode == 1:
            points1.pop(i)
        else:
            points2.pop(i)
    points_listbox.delete(0, tk.END)
    if mode == 1:
        for i in range(len(points1)):
            points_listbox.insert(i, str(i + 1) + ") " + str(points1[i][0]) + " " + str(points1[i][1]))
    else:
        for i in range(len(points2)):
            points_listbox.insert(i, str(i + 1) + ") " + str(points2[i][0]) + " " + str(points2[i][1]))
    offset = max(get_offset(points1), get_offset(points2))
    coef = min(zooming(points1, maxsize, offset), zooming(points2, maxsize, offset))

    canvas.delete("all")

    draw_points(points1, canvas, coef, color1, offset)
    draw_points(points2, canvas, coef, color2, offset)

#функция удаления точек
def delete_all_point(points1_listbox, points2_listbox, canvas, coef, mode, color1, color2, maxsize):
    global points1, points2, offset
    
    points1_listbox.delete(0, tk.END)
    points2_listbox.delete(0, tk.END)
    points1 = []
    points2 = []

    canvas.delete("all")

#функция добавления точек
def plot_point(points_listbox, entry1, entry2, canvas, maxsize, color1, color2, mode):
    global points1, points2, coef, offset
    coordinates = entry1.get()
    coordinates2 = entry2.get()
    flag1 = True
    flag2 = True
    try:
        if len(coordinates) != 0:
            x, y = map(float, coordinates.split(' '))
        else:
            flag1 = False
        if len(coordinates2) != 0:
            x2, y2 = map(float, coordinates2.split(' '))
        else:
            flag2 = False
        if mode == 1:
            if (flag1 and [x, y] not in points1):
                points1.append([x, y])
                points_listbox.delete(0, tk.END)
                for i in range(len(points1)):
                    points_listbox.insert(i, str(i + 1) + ") " + str(points1[i][0]) + " " + str(points1[i][1]))
        else:
            if (flag2 and [x2, y2] not in points2):
                points2.append([x2, y2])
                points_listbox.delete(0, tk.END)
                for i in range(len(points2)):
                    points_listbox.insert(i, str(i + 1) + ") " + str(points2[i][0]) + " " + str(points2[i][1]))
        offset = max(get_offset(points1), get_offset(points2))
        coef = min(zooming(points1, maxsize, offset), zooming(points2, maxsize, offset))

        canvas.delete("all")

        draw_points(points1, canvas, coef, color1, offset)
        draw_points(points2, canvas, coef, color2, offset)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные координаты\nДробные числа вводятся через точку")




