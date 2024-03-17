import numpy as np
import matplotlib.pyplot as plt

X = np.array([
    [1],
    [2],
    [4],
    [3]
])

y = X * 3.35 + 7
data = np.concatenate((X, y), axis=1)


def loss_function(m, b, data):
    total_error = 0
    for i in range(len(data)):
        x = data[i][0]
        y = data[i][1]
        total_error += (y - (m * x + b)) ** 2
    return total_error / float(2 * len(data))


def gradient_desc(m_now, b_now, data, L):
    m_gradient = 0
    b_gradient = 0
    n = len(data)
    for i in range(n):
        x = data[i][0]
        y = data[i][1]
        m_gradient += (((m_now * x + b_now) - y) * x) / n
        b_gradient += ((m_now * x + b_now) - y) / n
    m = m_now - L * m_gradient
    b = b_now - L * b_gradient
    return m, b


m = 0
b = 0
L = 0.001
epochs = 10000

for i in range(epochs):
    m, b = gradient_desc(m, b, data, L)
print(m, b)

plt.scatter(data[:, 0], data[:, 1])
plt.plot(data[:, 0], m * data[:, 0] + b, color='red')
plt.show()

"""
def y_function(x):
    return x ** 2


def dm_derivative(x):
    return 2 * x


new_x = 100
old_x = 0
x = np.arange(-100, 100, 0.1)
y = y_function(x)

current_position = (-80, y_function(-80))
learning_rate = 0.01

for _ in range(1000):
    new_x = current_position[0] - learning_rate * derivative(current_position[0])
    new_y = y_function(new_x)
    current_position = (new_x, new_y)
    plt.plot(x, y)
    plt.scatter(current_position[0], current_position[1], color='red')
    plt.pause(0.001)
    plt.clf()
    print("Локальний мінімум має місце в", new_x)

# while abs(new_x - old_x) > learning_rate:
#     old_x = new_x
#     new_x = current_position[0] - learning_rate * derivative(current_position[0])
#     new_y = y_function(new_x)
#     current_position = (new_x, new_y)
#     plt.plot(x, y)
#     plt.scatter(current_position[0], current_position[1], color='red')
#     plt.pause(0.000001)
#     plt.clf()
#     print("Локальний мінімум має місце в", new_x)
"""
