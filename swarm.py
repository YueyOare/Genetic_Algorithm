import random

from scipy import optimize
import numpy as np

counter = 0
eps = 10 ** -6


def fitness_function(x):
    global counter
    counter += 1
    return 100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2
    # return x[0] ** 2 + x[1] ** 2


class Particle:
    def __init__(self, x0, min_v, max_v):
        self.position = []  # позиция частицы
        self.velocity = []  # скорость частицы
        self.pos_best = []  # лучшая позиция частицы
        self.val_best = -1  # лучшее значение частицы
        self.val = -1  # значение  частицы

        for i in range(len(x0)):
            self.velocity.append(random.uniform(min_v, max_v))
            self.position.append(x0[i])

    # обновление позиции частицы
    def update_position(self):
        for i in range(len(self.position)):
            self.position[i] = self.position[i] + self.velocity[i]

    # обновление скорости частицы
    def update_velocity(self, pos_best_g):
        w = 0.5  # инерционный вес
        c1 = 1  # когнитивный коэффициент
        c2 = 2  # социальный коэффициент

        for i in range(len(self.position)):
            r1 = random.random()
            r2 = random.random()

            vel_cognitive = c1 * r1 * (self.pos_best[i] - self.position[i])
            vel_social = c2 * r2 * (pos_best_g[i] - self.position[i])
            self.velocity[i] = w * self.velocity[i] + vel_cognitive + vel_social

    # вычисление значения частицы
    def evaluate(self, cost_function):
        self.val = cost_function(self.position)

        # обновление лучшей позиции и значения частицы
        if self.val < self.val_best or self.val_best == -1:
            self.pos_best = self.position
            self.val_best = self.val


class Swarm():
    def __init__(self, num_particles, left, right, min_v, max_v):

        self.val_best_g = -1  # лучшее значение глобально
        self.pos_best_g = []  # лучшая позиция глобально
        self.swarm = []
        self.num_particles = num_particles

        # создание частиц
        for i in range(0, num_particles):
            self.swarm.append(Particle([random.uniform(left, right) for _ in range(2)], min_v, max_v))

    def run(self, cost_function, maxiter):
        # запуск алгоритма
        i = 0
        output = []
        while i < maxiter:
            temp = np.zeros((self.num_particles + 1, 3))
            # вычисление значения для каждой частицы
            for j in range(0, self.num_particles):
                self.swarm[j].evaluate(cost_function)
                temp[j] = np.array(
                    [self.swarm[j].position[0], self.swarm[j].position[1], self.swarm[j].val])

            for j in range(self.num_particles):
                # обновление лучшей позиции и значения глобально
                if self.swarm[j].val < self.val_best_g or self.val_best_g == -1:
                    self.pos_best_g = list(self.swarm[j].position)
                    if abs(self.val_best_g - self.swarm[j].val) < eps:
                        self.val_best_g = float(self.swarm[j].val)
                        temp[self.num_particles] = np.array(
                            [self.pos_best_g[0], self.pos_best_g[1], self.val_best_g])
                        output.append(temp.T)
                        return output
                    self.val_best_g = float(self.swarm[j].val)

            # обновление скорости и позиции каждой частицы
            for j in range(0, self.num_particles):
                self.swarm[j].update_velocity(self.pos_best_g)
                self.swarm[j].update_position()

            temp[self.num_particles] = np.array(
                [self.pos_best_g[0], self.pos_best_g[1], self.val_best_g])
            output.append(temp.T)
            i += 1

        # вывод результатов
        print('Лучшая позиция: {}, Значение функции: {}'.format(self.pos_best_g, self.val_best_g))
        return output

