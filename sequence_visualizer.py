import matplotlib.pyplot as plt
from typing import Callable

def interate_sequence(func: Callable, start_value: float, interations: int) -> list[float]:
    """
    plot a sequence given the recursive definition
    Input:
        - func: Callable
        - start_value: float
        - iterations: int
    Example
        >>> func = lambda x: abs(x ** 2 - 1)
        >>> x_initial = 0.5
        >>> iterations = 3
        >>> interate_sequence(lambda x: abs(x ** 2 - 1), 0.5, 3)
        [0.5, 0.75, 0.4375, 0.80859375]
    """
    x_prev = start_value
    result = []
    for i in range(interations + 1):
        result.append(x_prev)
        x_prev = func(x_prev)
    return result

if __name__ == "__main__":
    import math

    x_min = 0
    x_max = 15
    func = lambda x: 2.2 * (x - x**2)
    initial_values = [0.4]

    x1 = list(range(x_min, x_max + 1))
    y = [interate_sequence(func, initial_value, x_max) for initial_value in initial_values]
    for i in range(len(y[0])): 
        print(f"iter {i}: {y[0][i]}")
    for i in y:
        plt.plot(i)
    # axis labeling
    plt.xlabel('iterations')
    plt.ylabel('output')
    # figure name
    plt.title('Dot Plot : output vs iterations')
    plt.show()