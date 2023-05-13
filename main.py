from swarm import *
import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

i = 0
work = False
validation = True


def display_window():
    def _quit():
        root.quit()  # остановка цикла
        root.destroy()  # закрытие приложения
        return

    def validate(entry, param, cond):
        global validation
        val = entry.get()
        try:
            value = param(val)
            if cond(value):
                entry.configure(bg='white')
                return value
            else:
                entry.configure(bg='red')
                validation = False
                return -1
        except ValueError:
            entry.configure(bg='red')
            validation = False
            return -1

    def update_plot(iters, a, b, data):
        global i
        i = 0
        while i < iters:
            ax1.clear()
            ax2.clear()
            a = min(a, min(data[i][0]), min(data[i][1]))
            b = max(b, max(data[i][0]), max(data[i][1]))
            x = np.arange(a, b, 1 / (b - a))
            y = np.arange(a, b, 1 / (b - a))
            xgrid, ygrid = np.meshgrid(x, y)
            zgrid = fitness_function((xgrid, ygrid))
            ax1.relim(visible_only=True)
            ax1.autoscale_view(True)
            ax2.relim(visible_only=True)
            ax2.autoscale_view(True)
            ax1.plot_surface(xgrid, ygrid, zgrid, cmap='summer')
            x = data[i][0][:-1]
            y = data[i][1][:-1]
            z = data[i][2][:-1]
            ax1.scatter(x, y, z, c='black', s=50, marker=r'$\varpi$')
            ax1.scatter(data[i][0][-1], data[i][1][-1], data[i][2][-1], c='red', s=100, marker='*')
            ax1.set_title("Итерация № " + str(i + 1))
            ax2.contourf(xgrid, ygrid, zgrid, cmap='Greens')
            ax2.scatter(x, y, c='black', s=50, marker=r'$\varpi$')
            ax2.scatter(data[i][0][-1], data[i][1][-1], c='red', s=100, marker='*')
            label2.configure(text="x1 = " + str("{:.6f}".format(data[i][0][-1])))
            label3.configure(text="x2 = " + str("{:.6f}".format(data[i][1][-1])))
            label4.configure(text="f(x1, x2) = " + str("{:.6f}".format(data[i][2][-1])))
            canvas.draw_idle()
            if not work:
                return
            root.update()
            i += 1
        return

    def stop():
        global work
        work = False

    def count():
        global work
        num_particles = validate(entry1, int, lambda x: x > 0)
        max_iterations = validate(entry2, int, lambda x: x > 0)
        min_v = validate(entry3, float, lambda x: x)
        max_v = validate(entry4, float, lambda x: x > min_v)
        left = validate(entry5, float, lambda x: x)
        right = validate(entry6, float, lambda x: x > left)
        if validation:
            swarm = Swarm(num_particles, left, right, min_v, max_v)
            output = swarm.run(fitness_function, max_iterations)
            work = True
            update_plot(min(max_iterations, len(output)), left, right, output)
        return 0

    root = tk.Tk()
    root.wm_title("Генетический алгоритм")

    frame1 = tk.LabelFrame(root, text="Параметры")
    frame2 = tk.LabelFrame(root, text="График функции")
    frame3 = tk.LabelFrame(root, text="Хромосомы 1 поколения")
    frame4 = tk.LabelFrame(root, text="Полученные решения")

    # frame1
    frame1.columnconfigure(index=0, weight=1)
    frame1.columnconfigure(index=1, weight=1)
    entry1 = tk.Entry(master=frame1)
    entry2 = tk.Entry(master=frame1)
    entry3 = tk.Entry(master=frame1)
    entry4 = tk.Entry(master=frame1)
    entry5 = tk.Entry(master=frame1)
    entry6 = tk.Entry(master=frame1)
    entry1.insert(0, "30")
    entry2.insert(0, "100")
    entry3.insert(0, "-1")
    entry4.insert(0, "1")
    entry5.insert(0, "-5")
    entry6.insert(0, "5")
    tk.Label(text="Функция", master=frame1).grid(row=0, column=1, padx=15, sticky=tk.NSEW)
    tk.Label(text="100(x2 - x1^2)^2 + (1 - x1)^2", master=frame1).grid(row=0, column=2, padx=15, sticky=tk.NSEW)
    tk.Label(text="Количество частиц", master=frame1).grid(row=1, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="Максимальное количество итераций", master=frame1).grid(row=1, column=2, padx=15, sticky=tk.NSEW)
    tk.Label(text="Минимальная скорость особи", master=frame1).grid(row=2, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="Максимальная скорость особи", master=frame1).grid(row=2, column=2, padx=15, sticky=tk.NSEW)
    tk.Label(text="Минимальное значение особи", master=frame1).grid(row=3, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="Максимальное значение особи", master=frame1).grid(row=3, column=2, padx=15, sticky=tk.NSEW)
    entry1.grid(row=1, column=1, padx=15, sticky=tk.NSEW)
    entry2.grid(row=1, column=3, padx=15, sticky=tk.NSEW)
    entry3.grid(row=2, column=1, padx=15, sticky=tk.NSEW)
    entry4.grid(row=2, column=3, padx=15, sticky=tk.NSEW)
    entry5.grid(row=3, column=1, padx=15, sticky=tk.NSEW)
    entry6.grid(row=3, column=3, padx=15, sticky=tk.NSEW)

    # frame2
    a, b = -5, 5
    x = np.arange(a, b, 0.2)
    y = np.arange(a, b, 0.2)
    xgrid, ygrid = np.meshgrid(x, y)
    zgrid = fitness_function((xgrid, ygrid))

    fig = Figure(figsize=(10, 4), dpi=100)
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(xgrid, ygrid, zgrid, cmap='inferno')
    ax1.set_xlabel('x1')
    ax1.set_ylabel('x2')
    ax1.set_zlabel('f(x1, x2)')
    ax2 = fig.add_subplot(122)
    ax2.contourf(xgrid, ygrid, zgrid, cmap='Greens')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')

    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, frame2)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # frame3

    button1 = tk.Button(master=frame3, text="Рассчитать", command=count)
    button2 = tk.Button(master=frame3, text="Прервать", command=stop)
    button1.pack(side=tk.LEFT, fill="x", expand=tk.TRUE)
    button2.pack(side=tk.LEFT, fill="x", expand=tk.TRUE)

    frame4.columnconfigure(index=0, weight=1)
    label1 = tk.Label(text="Лучшее решение:", master=frame4)
    label2 = tk.Label(text="x1 = неизвестно", master=frame4)
    label3 = tk.Label(text="x2 = неизвестно", master=frame4)
    label4 = tk.Label(text="f(x1, x2) = неизвестно", master=frame4)
    label1.grid(row=0, column=0, padx=5, sticky=tk.NSEW)
    label2.grid(row=1, column=0, padx=5, sticky=tk.NSEW)
    label3.grid(row=2, column=0, padx=5, sticky=tk.NSEW)
    label4.grid(row=3, column=0, padx=5, sticky=tk.NSEW)

    root.columnconfigure(index=0, weight=3)
    root.columnconfigure(index=1, weight=1)
    root.rowconfigure(index=0, weight=10)
    root.rowconfigure(index=1, weight=1)
    root.rowconfigure(index=2, weight=2)
    frame1.grid(row=2, column=0, padx=5, pady=1, sticky=tk.NSEW)
    frame2.grid(row=0, column=0, columnspan=2, padx=5, pady=1, sticky=tk.NSEW)
    frame3.grid(row=1, column=0, columnspan=2, padx=5, pady=1, sticky=tk.NSEW)
    frame4.grid(row=2, column=1, padx=5, pady=1, sticky=tk.NSEW)

    tk.mainloop()


if __name__ == "__main__":
    display_window()
