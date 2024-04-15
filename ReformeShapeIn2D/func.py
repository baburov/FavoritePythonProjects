from complex_shape import *
from tkinter import messagebox
import copy
def scale_button(canvas, entry_center, entry_coef, stack):
    try:
        value1, value2 = float(entry_center.get().split()[0]), float(entry_center.get().split()[1])
        value3, value4 = float(entry_coef.get().split()[0]), float(entry_coef.get().split()[1])
        figure = copy.deepcopy(stack.get())
        figure.scale(Point(value1, value2), value3, value4)
        figure.draw(canvas)
        stack.push(figure)
    except Exception:
        messagebox.showinfo("Ошибка", "Ошибка ввода данных.\nЦентр и коэффициенты масштабирования вводить через пробел\nДробные числа вводить через точку")
        stack.push(ComplexShape())

def turn_button(canvas, entry_center, entry_angle, stack):
    try:
        value1, value2 = float(entry_center.get().split()[0]), float(entry_center.get().split()[1])
        value3 = -1 * float(entry_angle.get())
        figure = copy.deepcopy(stack.get())
        figure.turn(Point(value1, value2), radians(value3))
        figure.draw(canvas)
        stack.push(figure)
    except Exception:
        messagebox.showinfo("Ошибка", "Ошибка ввода данных.\nЦентр поворота вводить через пробел\nДробные числа вводить через точку")
        stack.push(ComplexShape())

def move_button(canvas, entry_center, stack):
    try:
        value1, value2 = float(entry_center.get().split()[0]), float(entry_center.get().split()[1])
        figure = copy.deepcopy(stack.get())
        figure.move(Point(value1, value2))
        figure.draw(canvas)
        stack.push(figure)
    except Exception:
        messagebox.showinfo("Ошибка", "Ошибка ввода данных.\nСмещение вводить через пробел\nДробные числа вводить через точку")
        stack.push(ComplexShape())

def undo(canvas, stack):
    try:
        stack.pop()
        figure = stack.get()
        figure.draw(canvas)
    except Exception:
        messagebox.showinfo("Ошибка", "Список совершенных действий подошел к концу")
        stack.push(ComplexShape())

def show(canvas, stack):
    try:
        stack.stack = []
        stack.push(ComplexShape())
        figure = stack.get()
        figure.draw(canvas)
    except Exception:
        messagebox.showinfo("Ошибка", "Ошибка отрисовки изначальной фигуры")
        stack.push(ComplexShape())