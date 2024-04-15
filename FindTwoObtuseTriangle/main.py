import tkinter as tk
from points_func import *

root = tk.Tk()
root.title("Графический вывод точек")

maxsize = 500
color1 = "blue"
color2 = "red"

label = tk.Label(root, text="Введите координаты точек первой группы(x, y):")
label.grid(column=0, row=0)

label2 = tk.Label(root, text="Введите координаты точек второй группы(x, y):")
label2.grid(column=1, row=0)

entry1 = tk.Entry(root)
entry1.grid(column=0, row=1)

entry2 = tk.Entry(root)
entry2.grid(column=1, row=1)

canvas = tk.Canvas(root, width=maxsize, height=maxsize, bg="white")
canvas.grid(column=0, row=5, columnspan=2)

entry = tk.Entry(root)
entry.grid(column=3, row=1)

points1_listbox = tk.Listbox(listvariable=tk.Variable(value=points1))
points1_listbox.bind("<ButtonRelease-1>", lambda event: on_select_points1_listbox(points1_listbox, entry))
points1_listbox.grid(column=0, row=3)

points2_listbox = tk.Listbox(listvariable=tk.Variable(value=points2))
points2_listbox.bind("<ButtonRelease-1>", lambda event: on_select_points2_listbox(points2_listbox, entry))
points2_listbox.grid(column=1, row=3)

plot_button = tk.Button(root, text="Добавить точку", command=lambda: plot_point(points1_listbox, entry1, entry2, canvas,\
                                                                                maxsize, color1, color2, 1))
plot_button.grid(column=0, row=2)

plot_button2 = tk.Button(root, text="Добавить точку", command=lambda: plot_point(points2_listbox, entry1, entry2, canvas,\
                                                                                 maxsize, color1, color2, 2))
plot_button2.grid(column=1, row=2)

delete_button1 = tk.Button(root, text="Удалить выбранную точку", command=lambda: delete_point(points1_listbox,
                                                                                              canvas, coef, 1, color1,\
                                                                                              color2, maxsize))
delete_button1.grid(column=0, row=4)
delete_all_button = tk.Button(root, text="Удалить все точки", command=lambda: delete_all_point(points1_listbox, points2_listbox,
                                                                                              canvas, coef, 1, color1,\
                                                                                              color2, maxsize))
delete_all_button.grid(column=3, row=3)

delete_button2 = tk.Button(root, text="Удалить выбранную точку", command=lambda: delete_point(points2_listbox,
                                                                                              canvas, coef, 2, color1,\
                                                                                              color2, maxsize))
delete_button2.grid(column=1, row=4)

label = tk.Label(root, text="Точки синего цвета - первая группа точек\nТочки красного цвета - вторая группа точек")
label.grid(row=4, column=3)

label = tk.Label(root, text="Здесь будет выводиться результат")
label.grid(row=5, column=3)

triangle_plot_button = tk.Button(root, text="Показать результат", command=lambda: triangles_and_line_plot(label, canvas, maxsize, color1, color2))
triangle_plot_button.grid(column=0, row=6, columnspan=2)


edit_button = tk.Button(root, text="Редактировать", command=lambda: edit_item(points1_listbox, points2_listbox, entry, color1, color2, canvas, maxsize))
edit_button.grid(column=3, row=2)



root.mainloop()
