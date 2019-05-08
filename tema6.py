import random

_a = 0
_n = 1
precision = pow(10, -10)
solution_precision = pow(10, -3)
k_max = 100
delta_max = pow(10, 8)
tries_max = 1000


def read_input(file):
    poly_in = []
    lines = open(file).readlines()

    for line in lines:
        a_in, n_in = [int(num.strip()) for num in line.split('x^')]
        poly_in.append((a_in, n_in))

    return poly_in


def calculate_poly(poly, v, horner=True):
    result = 0

    if horner:
        result = poly[0][_a]
        for term in poly[1:]:
            result = term[_a] + result*v

    else:
        for term in poly:
            result += term[_a] * pow(v, term[_n])

    return result


def calculate_derivative(poly):
    derivative = []

    for term in poly:
        if term[_n] == 0:
            continue

        new_a = term[_a] * term[_n]
        new_n = term[_n] - 1

        derivative.append((new_a, new_n))

    return derivative


def calculate_range(poly):
    a0 = poly[0][_a]
    big_a = max([abs(term[_a]) for term in poly[1:]])
    return (abs(a0) + big_a) / abs(a0)#, big_a


def xk_new(poly, xk_old):

    der1 = calculate_derivative(poly)
    der2 = calculate_derivative(der1)

    dmp1 = calculate_poly(der1, xk_old)
    imp1 = calculate_poly(poly, xk_old)

    dmp2 = calculate_poly(der2, xk_old)
    imp2 = calculate_poly(der1, xk_old) * 2

    if imp1 == 0.0:
        imp1 = precision
    if imp2 == 0.0:
        imp2 = precision

    ak = dmp1 / imp1 - dmp2 / imp2

    return xk_old - 1/ak


def halley_method(poly):

    R = calculate_range(poly)
    x_current = random.random() * R * 2 - R
    xk = xk_new(poly, x_current)
    k = 1

    der1 = calculate_derivative(poly)
    der2 = calculate_derivative(der1)

    delta = delta_max

    while True:
        A = 2*pow(calculate_poly(der1, x_current), 2) - calculate_poly(poly, xk)*calculate_poly(der2, x_current)

        if abs(A) < precision:
            #print(f"A < precision ({A}) (x = {x_current})")
            break

        delta = calculate_poly(poly, x_current)*calculate_poly(der1, x_current) / A
        x_current = x_current - delta
        k += 1
        xk = xk_new(poly, xk)

        if (abs(delta) < precision) or k > k_max or abs(delta) > delta_max:
            break

    if abs(delta) < precision:
        #print(f"Found x = {x_current}")
        return x_current
    else:
        #print(f"Divergent")
        return None


P = read_input("input_extra.txt")
print(P)

solutions = []

for try_no in range(tries_max):

    x = halley_method(P)

    if x is not None:

        duplicate = False

        for r in solutions:
            if abs(r - x) < solution_precision:
                duplicate = True
                break

        if duplicate:
            continue
        else:
            solutions.append(x)

print(f"Solutions: {solutions}")
for s in solutions:
    print(f"P[{s:f}] = {calculate_poly(P, s):f}")
