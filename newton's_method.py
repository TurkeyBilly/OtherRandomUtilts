"""
Approximate a possible zero for an input function
"""

g_x = lambda x: x**3 + x - 1
# NOTE: g_prime_x needs to be determined before-hand!
g_prime_x = lambda x: 3*x**2 + 1
starting_point = 1
n_max = 5

rand_mode = False
if rand_mode:
    import random
    starting_point = random.randint()

####################################
x_n = [starting_point]
g_xn = [g_x(starting_point)]
k_n = [(x_n[0] * g_prime_x(x_n[0]) - g_xn[0]) / g_prime_x(x_n[0])]

print(f"n = {1}: x_n = {starting_point}, g(x_n) = {g_xn[0]}, g' = {g_prime_x(starting_point)}")

for i in range(1, n_max):
    x_new = k_n[i - 1]
    g_x_new = g_x(x_new)
    k_new = (x_new * g_prime_x(x_new) - g_x_new) / g_prime_x(x_new)
    x_n.append(x_new)
    g_xn.append(g_x_new)
    k_n.append(k_new)
    print(f"n = {i + 1}: x_n = {x_new}, g(x_n) = {g_x_new}, g' = {g_prime_x(x_new)}")