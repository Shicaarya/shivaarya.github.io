from math import sqrt, exp

print("Choose a function:")
print("1 = Parabola")
print("2 = Exponential")
choice = input("Enter 1 or 2: ")

if choice == "1":
    A = float(input("Enter A: "))
    B = float(input("Enter B: "))
    C = float(input("Enter C: "))

    def f(x):
        return A*x**2 + B*x + C

elif choice == "2":

    def f(x):
        return exp(x)

else:
    print("Invalid choice")
    exit()

t = float(input("Enter x-coordinate of point: "))
z = float(input("Enter y-coordinate of point: "))

left = float(input("Enter left side of interval: "))
right = float(input("Enter right side of interval: "))

def distance_squared(x):
    y = f(x)
    return (x - t)**2 + (y - z)**2

phi = (1 + sqrt(5)) / 2
resphi = 2 - phi

x1 = left + resphi * (right - left)
x2 = right - resphi * (right - left)

d1 = distance_squared(x1)
d2 = distance_squared(x2)

iteration = 0

while abs(right - left) > 0.0001:
    print("iteration", iteration, "interval =", left, right)

    if d1 < d2:
        right = x2
        x2 = x1
        d2 = d1

        x1 = left + resphi * (right - left)
        d1 = distance_squared(x1)

    else:
        left = x1
        x1 = x2
        d1 = d2

        x2 = right - resphi * (right - left)
        d2 = distance_squared(x2)

    iteration += 1

best_x = (left + right) / 2
best_y = f(best_x)
distance = sqrt(distance_squared(best_x))

print("\nFinal result")
print("x =", best_x)
print("y =", best_y)
print("distance =", distance)
