from genetic import genetic_algorithm, fitness_function
import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def display_window():
    def _quit():
        root.quit()  # остановка цикла
        root.destroy()  # закрытие приложения

    X = []
    Y = []
    OUTPUT = []
    current_generation = 0
    validation = True

    def update_treeview(tree, df):
        tree.delete(*tree.get_children())
        tree['columns'] = tuple(df.columns)
        for column in tree['columns']:
            tree.heading(column, text=column)
        for i, row in df.iterrows():
            tree.insert('', 'end', values=tuple(row))

    def validate(entry, param):
        global validation
        text = entry.get()
        try:
            param(text)
            entry.configure(bg='white')
            return param(text)
        except ValueError:
            try:
                if float(text).is_integer():
                    entry.configure(bg='white')
                    return int(float(text))
                else:
                    entry.configure(bg='red')
                    validation = False
                    return -1
            except ValueError:
                entry.configure(bg='red')
                validation = False
                return -1

    def count():
        global X, Y, OUTPUT, validation, current_generation
        validation = True
        mutation_rate = validate(entry1, float) / 100
        crossover_rate = validate(entry2, float) / 100
        elitism_k = validate(entry3, int)
        pop_size = validate(entry4, int)
        low = validate(entry5, float)
        high = validate(entry6, float)
        num_generations = validate(entry7, int)
        if validation:
            X, Y, OUTPUT, counter = genetic_algorithm(pop_size=pop_size, num_generations=num_generations, elitism_k=elitism_k,
                                             crossover_rate=crossover_rate, mutation_rate=mutation_rate, low=low, high=high)
            print('Точка минимума:', X, '\nМинимум функции:', Y)
            current_generation = 0
            frame3.configure(text="Хромосомы " + str(current_generation+1) + " поколения")
            label1.configure(text="x1 = " + str(X[0]))
            label2.configure(text="x2 = " + str(X[1]))
            label3.configure(text="f(x1, x2) = " + str(Y))
            label4.configure(text="КВЦФ - " + str(counter))
            update_treeview(tree, OUTPUT[current_generation].round(decimals=5))
            # for generation in OUTPUT:
            #     print(generation)
        validation = True
        return 0

    root = tk.Tk()
    root.wm_title("Генетический алгоритм")

    frame1 = tk.LabelFrame(root, text="Параметры")
    frame2 = tk.LabelFrame(root, text="График функции")
    frame3 = tk.LabelFrame(root, text="Хромосомы 1 поколения")
    frame4 = tk.LabelFrame(root, text="Полученные решения")

    # frame1
    button1 = tk.Button(master=frame1, text="Рассчитать", command=count)
    frame1.columnconfigure(index=0, weight=1)
    frame1.columnconfigure(index=1, weight=1)
    entry1 = tk.Entry(master=frame1)
    entry2 = tk.Entry(master=frame1)
    entry3 = tk.Entry(master=frame1)
    entry4 = tk.Entry(master=frame1)
    entry5 = tk.Entry(master=frame1)
    entry6 = tk.Entry(master=frame1)
    entry7 = tk.Entry(master=frame1)
    entry1.insert(0, "10")
    entry2.insert(0, "80")
    entry3.insert(0, "10")
    entry4.insert(0, "100")
    entry5.insert(0, "-5")
    entry6.insert(0, "5")
    entry7.insert(0, "100")
    tk.Label(text="Функция", master=frame1).grid(row=0, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="100(x2 - x1^2)^2 + (1 - x1)^2", master=frame1).grid(row=0, column=1, padx=15,
                                                                       sticky=tk.NSEW)
    tk.Label(text="Вероятность мутации, %", master=frame1).grid(row=1, column=0, padx=15,
                                                                sticky=tk.NSEW)
    tk.Label(text="Вероятность кроссинговера, %", master=frame1).grid(row=2, column=0, padx=15,
                                                                      sticky=tk.NSEW)
    tk.Label(text="Элитизм", master=frame1).grid(row=3, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="Количество хромосом", master=frame1).grid(row=4, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="Минимальное значение гена", master=frame1).grid(row=5, column=0, padx=15,
                                                                   sticky=tk.NSEW)
    tk.Label(text="Максимальное значение гена", master=frame1).grid(row=6, column=0, padx=15,
                                                                    sticky=tk.NSEW)
    tk.Label(text="Количество поколений", master=frame1).grid(row=7, column=0, padx=15,
                                                              sticky=tk.NSEW)
    entry1.grid(row=1, column=1, padx=15, sticky=tk.NSEW)
    entry2.grid(row=2, column=1, padx=15, sticky=tk.NSEW)
    entry3.grid(row=3, column=1, padx=15, sticky=tk.NSEW)
    entry4.grid(row=4, column=1, padx=15, sticky=tk.NSEW)
    entry5.grid(row=5, column=1, padx=15, sticky=tk.NSEW)
    entry6.grid(row=6, column=1, padx=15, sticky=tk.NSEW)
    entry7.grid(row=7, column=1, padx=15, sticky=tk.NSEW)
    button1.grid(row=8, column=0, columnspan=2, pady=2)

    # frame2
    a, b = -100, 100
    x, y = np.mgrid[a:b:10j, a:b:10j]
    z = fitness_function((x, y))

    fig = Figure(figsize=(6, 3.5), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, cmap='inferno')
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('f(x1, x2)')

    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, frame2)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # frame3
    def prev_generation():
        global OUTPUT, current_generation
        if current_generation > 0:
            current_generation -= 1
            frame3.configure(text="Хромосомы " + str(current_generation+1) + " поколения")
            update_treeview(tree, OUTPUT[current_generation].round(decimals=5))

    def next_generation():
        global OUTPUT, current_generation
        if current_generation < int(entry7.get())-1:
            current_generation += 1
            frame3.configure(text="Хромосомы " + str(current_generation+1) + " поколения")
            update_treeview(tree, OUTPUT[current_generation].round(decimals=5))

    def first_generation():
        global OUTPUT, current_generation
        current_generation = 0
        frame3.configure(text="Хромосомы " + str(current_generation+1) + " поколения")
        update_treeview(tree, OUTPUT[current_generation].round(decimals=5))

    def last_generation():
        global OUTPUT, current_generation
        current_generation = int(entry7.get())-1
        frame3.configure(text="Хромосомы " + str(current_generation+1) + " поколения")
        update_treeview(tree, OUTPUT[current_generation].round(decimals=5))

    parent = frame3
    tree = ttk.Treeview(parent, show="headings")
    vsb = tk.Scrollbar(parent, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    tree.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
    button2 = tk.Button(master=parent, text="Следующее поколение", command=next_generation)
    button3 = tk.Button(master=parent, text="Предыдущее поколение", command=prev_generation)
    button4 = tk.Button(master=parent, text="Первое поколение", command=first_generation)
    button5 = tk.Button(master=parent, text="Последнее поколение", command=last_generation)
    button4.pack(side=tk.LEFT, fill="x", expand=tk.TRUE)
    button3.pack(side=tk.LEFT, fill="x", expand=tk.TRUE)
    button5.pack(side=tk.RIGHT, fill="x", expand=tk.TRUE)
    button2.pack(side=tk.RIGHT, fill="x", expand=tk.TRUE)

    # frame4
    for i in range(4):
        frame4.rowconfigure(index=i, weight=1)
    frame4.columnconfigure(index=0, weight=1)
    tk.Label(text="Лучшее решение:", master=frame4).grid(row=0, column=0, padx=15, sticky=tk.NSEW)

    label1 = tk.Label(text="x1 = неизвестно", master=frame4)
    label2 = tk.Label(text="x2 = неизвестно", master=frame4)
    label3 = tk.Label(text="f(x1, x2) = неизвестно", master=frame4)
    label4 = tk.Label(text="КВЦФ - неизвестно", master=frame4)

    label1.grid(row=1, column=0, padx=15, sticky=tk.NSEW)
    label2.grid(row=2, column=0, padx=15, sticky=tk.NSEW)
    label3.grid(row=3, column=0, padx=15, sticky=tk.NSEW)
    label4.grid(row=4, column=0, padx=15, sticky=tk.NSEW)
    root.columnconfigure(index=0, weight=1)
    root.columnconfigure(index=1, weight=1)
    for i in range(9):
        root.rowconfigure(index=i, weight=1)
    frame1.grid(row=0, column=0, rowspan=4, padx=5, pady=5, sticky=tk.NSEW)
    frame2.grid(row=4, column=0, rowspan=6, padx=5, pady=5, sticky=tk.NSEW)
    frame3.grid(row=0, column=1, rowspan=9, padx=5, pady=5, sticky=tk.NSEW)
    frame4.grid(row=9, column=1, rowspan=1, padx=5, pady=5, sticky=tk.NSEW)

    tk.mainloop()


if __name__ == "__main__":
    display_window()
