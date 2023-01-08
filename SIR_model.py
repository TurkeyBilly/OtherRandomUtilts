import matplotlib.pyplot as plt

float_list = list[float]

def simu(
    susceptible: int,
    infected: int,
    removed: int,
    recover_porpotion: float,
    average_contacts: int,
    growth_rate: float,
    death_rate: float,
    re_infected_rate: float,
    simu_range: int
) -> tuple[float_list, float_list, float_list, float_list, float_list]:
    """
    return lists of time, susceptible, infected, removed, dead
    """
    s, i, r = susceptible, infected, removed
    dead = 0
    infection_rate = average_contacts * recover_porpotion
    safe_rate = 1 - death_rate

    n = population = s + i + r
    susceptible_t, infected_t, removed_t, dead_t = [], [], [], []

    for _ in range(simu_range):
        susceptible_t.append(susceptible)
        infected_t.append(infected)
        removed_t.append(removed)
        dead_t.append(dead)

        susceptible_delta = - infection_rate * susceptible * infected / population
        infected_delta = - susceptible_delta - recover_porpotion * infected
        removed_delta = recover_porpotion * infected * safe_rate
        death_delta = recover_porpotion * infected * death_rate

        susceptible_delta += growth_rate * population / 365
        infected_delta += re_infected_rate * removed * average_contacts
        removed_delta -= re_infected_rate * removed * average_contacts

        susceptible += susceptible_delta
        infected += infected_delta
        removed += removed_delta
        dead += death_delta

    return (
        list(range(simu_range)),
        susceptible_t,
        infected_t,
        removed_t,
        dead_t
    )

T, S, I, R, D = simu(
    susceptible=50000,
    infected=1000,
    removed=0,
    recover_porpotion=1/14,
    average_contacts=1,
    growth_rate=0.0,
    death_rate=0.1,
    re_infected_rate=0.01,
    simu_range=200
)

plt.plot(T, S, label='Susceptible')
plt.plot(T, I, label='Infected')
plt.plot(T, R, label='Removed')
plt.plot(T, D, label='Dead')

plt.xlabel('time (days)')
plt.ylabel('people')
plt.legend()
plt.show()
