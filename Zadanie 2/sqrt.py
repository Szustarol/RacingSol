#!/usr/bin/python3

import numpy as np
import math
import matplotlib.pyplot as plt
import time

# Szukamy takiej wartości y, że y = sqrt(x)
# Czyli: y^2 = x
# Mamy więc:
# f(y) = y^2 - x, trzeba teraz znaleźć pierwiastek tej funkcji.
# f'(y) = 2y

def newton_sqrt(x, n = None, eps = None):
    """
    Returns a square root of @x in @n iterations 
    of the Newton's method, or when @eps - change in value is less than eps.
    If both n and eps is given, both conditions need to be satisfied.
    """

    assert (not n == eps == None) and (not n == 0 or eps == 0) , "At least one of n or esp must be set."
    
    # Dla ujemnego wejścia zdecydowałem sie na obsługę w postaci zwrócenia pierwiastka
    # wartości bezwzględnej ze znakiem

    sign = 1 if x >=0 else -1
    x = abs(x)

    # Relatywnie szybkim i dobrym sposobem na wybranie punktu początkowego 
    # dla tej metody jest konwersja zmiennej na int, a następnie przesunięcie bitowe
    # w prawo o połowę znaczących bitów liczby (chyba, że wychodzi zero).
    # Jest to moje rozwiązanie autorskie, nie ma tego raczej w internecie,
    # ale dość dobrze przybliża kwadrat, bowiem binarnie kwadrat liczby ma około dwukrotnie
    # więcej bitów.
    # Do takich optymalizacji C sie bardziej nadaje, bo na niektórych architekturach
    # znalezienie wiodącego bitu to jedna instrukcja (raczej CISC), ewentualnie 
    # __builtin_clz w GCC, ale w py też się da.

    asInt = int(round(x))
    if x != 0:
        #niestety trzeba robić log, bo operacje na bitach są w py wolne
        nMeaningBits = round(math.log(x)) 
        y = asInt >> (nMeaningBits//2+1)
    else:
        return 0

    error = abs(x-y)
    nIter = 0

    # Maksymalny błąd i iteracje można ogarniczyć przez inf
    maxError = eps if eps else float("inf")
    maxIter = n if n else float("inf")

    while error >= maxError or nIter < maxIter:
        prevValue = y
        if y == 0:
            break
        # Z "wzoru" na metodę Newtona
        y = y - (y*y-x)/(2*y)
        eps = abs(y-prevValue)

        nIter+=1

    return y*sign

def calculateTime(function, nIterations, *params):
    """Oblicza czas wykonania @nIterations funkcji @function z parametrami @params"""

    startTime = time.time()
    
    for _ in range(nIterations):
        function(*params)

    totalTime = time.time() - startTime

    return totalTime


# STAŁE DO OBLICZEŃ STATYSTYCZNYCH

N_EXECUTIONS = 10000
N_TESTS = 25

# RYSOWANIE WYKRESÓW

fig, axs = plt.subplots(1, 3)

x = np.linspace(2, 1e6, 10)

# LICZBA OPERACJI A DOKŁADNOŚĆ

yLibrary = [np.sqrt(v) for v in x]
axs[0].plot(x, yLibrary, label="Library function", linewidth = 4)
axs[0].set_xlabel("x")
axs[0].set_ylabel("sqrt(x)")
axs[0].set_title("Value of sqrt(x) for numpy vs Newton method.")

# LICZBA OPERACJI A WZGLĘDNA RÓŻNICA WARTOŚCI

axs[1].set_title("Relative difference of sqrt(x) \n between library and Newton method.")
axs[1].set_xlabel("x")
axs[1].set_ylabel("|np.sqrt(x)-newton_sqrt(x, n)|/np.sqrt(x)")

# CZAS WYKONANIA FUNKCJI BIBLIOTECZNEJ (UŚREDNIONE Z N_TESTS WYKONAŃ)
libraryExecTime = np.mean([calculateTime(np.sqrt, N_EXECUTIONS, 3) for _ in range(N_TESTS)])
implExecTime = []
implExecN = []

for nIter in range(1, 8):

    # Czas obliczania 10k iteracji
    implExecN.append(nIter)
    implExecTime.append( # Uśrednione N_TESTS wykonań
        np.mean([calculateTime(newton_sqrt, N_EXECUTIONS, 3, nIter) for _ in range(N_TESTS)])
    )

    # Wartość dla danego x i określonego n
    yImpl = [newton_sqrt(v, nIter) for v in x]

    # Błąd względny
    yDiff = [abs(lib - new)/(lib+1e-13) for lib, new in zip(yLibrary, yImpl)]

    axs[0].plot(x, yImpl, label="Newton method (n = {})".format(nIter), alpha = 0.1*nIter)
    axs[1].plot(x, yDiff, label="Newton method (n = {})".format(nIter), alpha = 0.1*nIter)

axs[2].bar(implExecN, implExecTime, label = "Newton's method of size n.")
axs[2].plot([implExecN[0], implExecN[-1]], [libraryExecTime, libraryExecTime],
    c = "red", label="Time of library executions", linewidth = 4)
axs[2].set_xlabel("N")
axs[2].set_ylabel("Time of {} executions".format(N_EXECUTIONS))
axs[2].legend()
axs[2].set_title("Time of {} sqrt executions.".format(N_EXECUTIONS))

axs[0].legend()
axs[1].legend()
print("done")


plt.show()
