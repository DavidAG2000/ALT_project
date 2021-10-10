import numpy as np


def dp_levenshtein_backwards(x, y):
    tamX = len(x) + 1

    prev = np.zeros(tamX, dtype=np.uint64)
    current = np.arange(tamX, dtype=np.uint64)

    for j in range(1, len(y) + 1):
        prev, current = current, prev
        current[0] = prev[0] + 1

        for i in range(1, len(x) + 1):
            actualValue = current[i - 1] + 1
            isSame = prev[i - 1] + (x[i - 1] != y[j - 1])
            current[i] = min(actualValue, prev[i] + 1, isSame)

    return current[len(x)]


def dp_restricted_damerau_backwards(x, y):
    tamX = len(x) + 1

    prev1 = np.zeros(tamX, dtype=np.uint8)
    prev2 = np.zeros(tamX, dtype=np.uint8)
    current = np.arange(tamX, dtype=np.uint8)

    for j in range(1, len(y) + 1):
        prev1, current, prev2 = current, prev1, prev1
        current[0] = prev1[0] + 1

        for i in range(1, len(x) + 1):
            erase = current[i - 1] + 1
            ins = prev1[i] + 1
            mod = prev1[i - 1] + (x[i - 1] != y[j - 1])

            if i > 1 and j > 1 and x[i-2] == y[j-1] and x[i-1] == y[j-2]:
                current[i] = min(erase, ins, mod, prev2[i - 1])
            else:
                current[i] = min(erase, ins, mod)

    return current[len(x)]


def dp_intermediate_damerau_backwards(x, y):
    tamX = len(x) + 1

    prev1 = np.zeros(tamX, dtype=np.uint8)
    prev2 = np.zeros(tamX, dtype=np.uint8)
    prev3 = np.zeros(tamX, dtype=np.uint8)
    current = np.arange(tamX, dtype=np.uint8)

    for j in range(1, len(y) + 1):
        prev3, prev2, prev1, current = current, prev3, current, prev3
        current[0] = prev1[0] + 1

        for i in range(1, len(x) + 1):
            erase = current[i - 1] + 1
            ins = prev1[i] + 1
            mod = prev1[i - 1] + (x[i - 1] != y[j - 1])

            if i > 1 and j > 1 and x[i-2] == y[j-1] and x[i-1] == y[j-2]:
                current[i] = min(erase, ins, mod, prev2[i - 1])
            elif i > 1 and j > 2 and x[i-2] == y[j-1] and x[i-1] == y[j-3]:
                current[i] = min(erase, ins, mod, prev3[i - 1])
            elif i > 2 and j > 1 and x[i-3] == y[j-1] and x[i-1] == y[j-2]:
                current[i] = min(erase, ins, mod, prev3[i - 1])
            else:
                current[i] = min(erase, ins, mod)

    return current[len(x)]


test = [("algoritmo", "algortimo"),
        ("algoritmo", "algortximo"),
        ("algoritmo", "lagortimo"),
        ("algoritmo", "agaloritom"),
        ("algoritmo", "algormio"),
        ("acb", "ba")]

for x, y in test:
    print(f"{x:12} {y:12}", end="")
    for dist, name in ((dp_levenshtein_backwards, "levenshtein"),
                       (dp_restricted_damerau_backwards, "restricted"),
                       (dp_intermediate_damerau_backwards, "intermediate")):
        print(f" {name} {dist(x,y) }", end="")
    print()


"""
Salida del programa:

algoritmo    algortimo    levenshtein  2 restricted  1 intermediate  1
algoritmo    algortximo   levenshtein  3 restricted  3 intermediate  2
algoritmo    lagortimo    levenshtein  4 restricted  2 intermediate  2
algoritmo    agaloritom   levenshtein  5 restricted  4 intermediate  3
algoritmo    algormio     levenshtein  3 restricted  3 intermediate  2
acb          ba           levenshtein  3 restricted  3 intermediate  2
"""
