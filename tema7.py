def read_input(path):

    lines = open(path).readlines()

    x_list = [float(x) for x in lines[0].split()]
    y_list = [float(y) for y in lines[1].split()]

    x = float(lines[2])
    result = float(lines[3])

    return x_list, y_list, x, result


def calculate_aitken(x_list, y_list):

    n = len(x_list)
    table = [x_list, y_list]

    for step in range(n - 1):

        table.append([0 for x in range(n)])

        for k in range(step, n - 1):

            # print(table)
            # print(step + 2, k + 1)

            v1 = table[1 + step][k + 1]
            v2 = table[1 + step][k + 0]
            v3 = table[0][k + 1]
            v4 = table[0][k - step]

            table[2 + step][k + 1] = (v1 - v2) / (v3 - v4)
            # (table[1 + step][k + 1] - table[1 + step][k + 0]) / (table[0][k + 1] - table[0][k - step])

    return table


def calculate_newton(x, x_list, y_list, aitken):

    sum = y_list[0]
    n = len(x_list)

    for k in range(1, n):

        prod = (x - x_list[0])
        for i in range(1, k):
            prod *= (x - x_list[i])
        prod *= aitken[1 + k][k]
        sum += prod

    return sum


x_list, y_list, x, result = read_input('input.txt')

n = len(x_list)

print(f"x  |  {''.join(['{: <10}'.format(x) for x in x_list])}")
print(f"f  |  {''.join(['{: <10}'.format(x) for x in y_list])}")
print("")
print(f"x = {x}")
print(f"f(x) = {result}")

aitken = calculate_aitken(x_list, y_list)

print("")
print("Aitken:")

print("".join([f'{"x": <10}', f'{"y": <10}'] + [f'{"Pas "+str(i+1): <10}' for i in range(n-1)]) + "\n")
for i in range(n):
    print("".join([f"{x[i]: <10}" for x in aitken]) + "\n")

print(f"f(x) ~ {calculate_newton(x, x_list, y_list, aitken)}")