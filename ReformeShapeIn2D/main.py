import tkinter as tk
from tkinter import ttk
from func import *
from logic import *
from complex_shape import *

stack = Stack(ComplexShape())

root = tk.Tk()
root.title("Image reforming")

label_move = tk.Label(root, text="Введите параметры перемещения (x y)")
label_move.grid(column=1, row=0, columnspan=2, sticky="nsew", ipadx=0, ipady=0)
canvas = tk.Canvas(width=750, height=750, bg='white')
canvas.grid(column=0, rowspan=30)
figure = stack.get()
figure.draw(canvas)
entry_move = tk.Entry(root, width=20)
entry_move.grid(column=1, row=1, sticky="nsew", ipadx=0, ipady=0, columnspan=2)
button_move = tk.Button(root, text="Переместить", command=lambda: move_button(canvas, entry_move, stack))
button_move.grid(column=1, row=2, sticky="nsew", ipadx=0, ipady=0, columnspan=2)


label_scale = tk.Label(root, text="Введите параметры масштабирования")
label_scale.grid(column=1, row=3, columnspan=2, sticky="nsew")
label_scale_center = tk.Label(root, text="Центр (x y)")
label_scale_center.grid(column=1, row=4, sticky="nsew")
entry_scale = tk.Entry(root, width=20)
entry_scale.grid(column=2, row=4, sticky="nsew")
label_scale_coef = tk.Label(root, text="Коэффициент (x y)")
label_scale_coef.grid(column=1, row=5, sticky="nsew")
entry_scale_coef = tk.Entry(root, width=20)
entry_scale_coef.grid(column=2, row=5, sticky="nsew")
button_scale = tk.Button(root, text="Масштабировать", command=lambda: scale_button(canvas, entry_scale, entry_scale_coef, stack))
button_scale.grid(column=1, row=6, sticky="nsew", columnspan=2)

label_turn = tk.Label(root, text="Введите параметры поворота")
label_turn.grid(column=1, row=7, columnspan=2, sticky="nsew")
label_turn_center = tk.Label(root, text="Центр (x y)")
label_turn_center.grid(column=1, row=8, sticky="nsew")
entry_turn = tk.Entry(root, width=20)
entry_turn.grid(column=2, row=8, sticky="nsew")
lable_turn_angle = tk.Label(root, text="Угол")
lable_turn_angle.grid(column=1, row=9, sticky="nsew")
entry_turn_angle = tk.Entry(root, width=20)
entry_turn_angle.grid(column=2, row=9, sticky="nsew")
button_turn = tk.Button(root, text="Повернуть", command=lambda: turn_button(canvas, entry_turn, entry_turn_angle, stack))
button_turn.grid(column=1, row=10, sticky="nsew", columnspan=2)

button_undo = tk.Button(root, text="Отменить последнее действие", command=lambda: undo(canvas, stack))
button_undo.grid(column=1, row=11, sticky="nsew", columnspan=2)

button_show = tk.Button(root, text="Показать исходное изображение", command=lambda: show(canvas, stack))
button_show.grid(column=1, row=12, sticky="nsew", columnspan=2)

root.mainloop()
